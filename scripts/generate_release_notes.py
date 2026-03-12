#!/usr/bin/env python3
"""
generate_release_notes.py — ConsentWise Release Notes Generator

Reconciles Jira and Git data to produce audit-grade release artefacts:
  - release-notes/vX.Y.Z.md          Human-readable release notes (markdown)
  - release-notes/audit/vX.Y.Z.json  ISO 27001 / SOC1 machine-readable audit log

Reconciliation categories:
  TRACED     — Jira fixVersion set AND git commit references the ticket   ✅ Fully traced
  JIRA_ONLY  — Jira fixVersion set but no matching git commit ref         ⚠️  No commit evidence
  GIT_ONLY   — Git references ticket but Jira fixVersion not set          ⚠️  Version field missing
  UNTRACKED  — Git commit has no ticket reference at all                  🔴 Zero traceability

Usage:
  python3 scripts/generate_release_notes.py --version 1.0.0

Options:
  --version VERSION       Release version (must match Jira fixVersion, e.g. 1.0.0)
  --from-ref REF          Git start ref (default: auto-detect previous tag or initial commit)
  --to-ref REF            Git end ref (default: tag vVERSION)
  --jira-url URL          Jira base URL (default: https://open-banking.atlassian.net)
  --jira-project KEY      Jira project key (default: CWPD)
  --jira-user EMAIL       Jira email (default: JIRA_USER env var or simon.hewins@gmail.com)
  --jira-token TOKEN      Jira API token (default: JIRA_TOKEN env var)
  --output-dir DIR        Output directory (default: release-notes)
  --jira-jql JQL          Override Jira query with custom JQL (default: project=X AND fixVersion=Y)
                          Useful for initiative-based releases, e.g.:
                            'project = SD AND issue in issuelinksOf("SD-3850")'
  --skip-jira             Skip Jira queries (git-only mode, useful offline)
  --dry-run               Print output to stdout without writing files
"""

import argparse
import base64
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_JIRA_URL  = "https://open-banking.atlassian.net"
DEFAULT_JIRA_PROJECT = "CWPD"
DEFAULT_JIRA_USER = "simon.hewins@gmail.com"
DEFAULT_OUTPUT_DIR = "release-notes"

CONVENTIONAL_COMMIT_RE = re.compile(
    r"^(feat|fix|docs|style|refactor|test|chore|ci|perf)(!?)"
    r"(?:\(([^)]+)\))?:\s+(.+)$"
)
MERGE_COMMIT_RE = re.compile(r"^Merge (pull request|branch) ")


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def run_git(*args):
    result = subprocess.run(["git"] + list(args), capture_output=True, text=True, cwd=Path.cwd())
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def get_initial_commit():
    return run_git("rev-list", "--max-parents=0", "HEAD")


def get_previous_tag(tag):
    """Return the tag immediately before the given tag, or None."""
    out = run_git("describe", "--tags", "--abbrev=0", f"{tag}^")
    return out if out else None


def resolve_ref(ref):
    return run_git("rev-parse", "--verify", ref)


def get_commits(from_ref, to_ref, project_key):
    """
    Return list of commit dicts in the range from_ref..to_ref.
    If from_ref is None, returns all commits up to to_ref.
    """
    SEP = "\x1f"
    REC = "\x1e"
    fmt = f"%H{SEP}%an{SEP}%ae{SEP}%ai{SEP}%s{REC}"
    range_spec = f"{from_ref}..{to_ref}" if from_ref else to_ref

    raw = run_git("log", f"--format={fmt}", range_spec)

    commits = []
    ticket_re = re.compile(rf"\b({re.escape(project_key)}-\d+)\b")

    for entry in raw.split(REC):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split(SEP)
        if len(parts) < 5:
            continue
        sha, author, email, date, subject = parts[0], parts[1], parts[2], parts[3], parts[4]

        ticket_refs = list(set(ticket_re.findall(subject)))
        parsed = CONVENTIONAL_COMMIT_RE.match(subject)
        is_merge = bool(MERGE_COMMIT_RE.match(subject))

        commits.append({
            "sha": sha,
            "sha_short": sha[:8],
            "author": author,
            "email": email,
            "date": date,
            "subject": subject,
            "ticket_refs": ticket_refs,
            "is_merge": is_merge,
            "conv_type": parsed.group(1) if parsed else None,
            "conv_breaking": parsed.group(2) == "!" if parsed else False,
            "conv_scope": parsed.group(3) if parsed else None,
            "conv_description": parsed.group(4) if parsed else None,
        })

    return commits


# ---------------------------------------------------------------------------
# Jira helpers
# ---------------------------------------------------------------------------

def make_jira_headers(user, token):
    creds = base64.b64encode(f"{user}:{token}".encode()).decode()
    return {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def jira_get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    # macOS often lacks the CA bundle; create an unverified context as fallback
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            return json.loads(resp.read()), None
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return None, f"HTTP {e.code}: {body[:200]}"
    except Exception as e:
        return None, str(e)


def get_jira_tickets_by_version(jira_url, project, version, headers,
                                jql_override=None, max_tickets=2000):
    """Query Jira for all tickets in the release scope, paginating until complete.

    Jira Cloud REST API v3 uses cursor-based pagination (nextPageToken).
    Falls back to offset-based (startAt) if nextPageToken is absent.
    max_tickets caps the total fetch to prevent runaway queries.
    """
    if jql_override:
        jql = jql_override
    else:
        jql = f'project = {project} AND fixVersion = "{version}" ORDER BY issuetype ASC, key ASC'

    PAGE_SIZE = 100
    all_issues = []
    seen_keys = set()
    next_page_token = None
    start_at = 0
    total = None

    while True:
        # Prefer cursor-based pagination (nextPageToken) over offset-based (startAt)
        base_params = {
            "jql": jql,
            "fields": "summary,status,issuetype,fixVersions,priority",
            "maxResults": PAGE_SIZE,
        }
        if next_page_token:
            base_params["nextPageToken"] = next_page_token
        else:
            base_params["startAt"] = start_at

        url = f"{jira_url}/rest/api/3/search/jql?{urllib.parse.urlencode(base_params)}"
        data, err = jira_get(url, headers)
        if err:
            print(f"  [WARN] Jira query failed: {err}", file=sys.stderr)
            break

        if total is None and data.get("total"):
            total = data["total"]

        page = data.get("issues", [])

        # Deduplicate — guards against APIs that repeat results when startAt is ignored
        new_issues = [i for i in page if i["key"] not in seen_keys]
        for i in new_issues:
            seen_keys.add(i["key"])
        all_issues.extend(new_issues)

        fetched = len(all_issues)
        total_str = str(total) if total else "?"
        print(f"  [Jira] Fetched {fetched}/{total_str} tickets...", file=sys.stderr)

        # Stop conditions
        if not page or len(page) < PAGE_SIZE:
            break  # Last page
        if total and fetched >= total:
            break
        if fetched >= max_tickets:
            print(f"  [WARN] max_tickets limit ({max_tickets}) reached — "
                  f"{total_str} total in Jira. Narrow JQL or raise --max-tickets.",
                  file=sys.stderr)
            break
        if not new_issues:
            # All results on this page were duplicates — API is looping, stop
            print(f"  [WARN] Pagination stalled (duplicate results). "
                  f"This API endpoint may not support offset pagination.", file=sys.stderr)
            break

        # Advance cursor
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            start_at += PAGE_SIZE

    return all_issues


def get_jira_ticket_details(jira_url, ticket_key, headers):
    """Fetch a single ticket's details."""
    url = f"{jira_url}/rest/api/3/issue/{ticket_key}?fields=summary,status,issuetype,fixVersions,priority"
    data, err = jira_get(url, headers)
    if err:
        return None
    return data


def enrich_git_only_tickets(jira_url, ticket_keys, headers):
    """Fetch Jira details for tickets referenced in git but without fixVersion."""
    result = {}
    for key in ticket_keys:
        ticket = get_jira_ticket_details(jira_url, key, headers)
        if ticket:
            result[key] = ticket
    return result


# ---------------------------------------------------------------------------
# Reconciliation
# ---------------------------------------------------------------------------

def reconcile(jira_version_issues, commits, project_key):
    """
    Produce four reconciliation categories.

    Returns:
      traced     — list of {jira_issue, commits[]}
      jira_only  — list of {jira_issue, commits: []}
      git_only   — list of {key, jira_issue_or_None, commits[]}
      untracked  — list of commit dicts (no ticket ref, non-merge)
    """
    jira_by_key = {i["key"]: i for i in jira_version_issues}
    jira_keys = set(jira_by_key.keys())

    # Build map: ticket_key -> list of commits that reference it
    commits_by_ticket = {}
    for c in commits:
        for ref in c["ticket_refs"]:
            if ref.startswith(project_key + "-"):
                commits_by_ticket.setdefault(ref, []).append(c)

    git_keys = set(commits_by_ticket.keys())

    traced = []
    for key in sorted(jira_keys & git_keys):
        traced.append({"key": key, "jira": jira_by_key[key], "commits": commits_by_ticket[key]})

    jira_only = []
    for key in sorted(jira_keys - git_keys):
        jira_only.append({"key": key, "jira": jira_by_key[key], "commits": []})

    git_only_keys = sorted(git_keys - jira_keys)
    git_only = []
    for key in git_only_keys:
        git_only.append({"key": key, "jira": None, "commits": commits_by_ticket[key]})

    untracked = [
        c for c in commits
        if not c["ticket_refs"] and not c["is_merge"]
    ]

    return traced, jira_only, git_only, untracked


def traceability_score(commits, untracked, git_only):
    """
    % of non-merge commits that are fully traced (have a Jira ticket + in version).
    TRACED / (TRACED + GIT_ONLY_commits + UNTRACKED)
    """
    total_meaningful = sum(1 for c in commits if not c["is_merge"])
    untraced_count = len(untracked) + sum(len(g["commits"]) for g in git_only)
    traced_count = total_meaningful - untraced_count
    if total_meaningful == 0:
        return 100.0
    return round((traced_count / total_meaningful) * 100, 1)


# ---------------------------------------------------------------------------
# Jira issue formatting helpers
# ---------------------------------------------------------------------------

def issue_type_icon(issue_type):
    icons = {
        "Initiative": "🎯",
        "Epic": "📦",
        "Story": "📖",
        "Bug": "🐛",
        "Task": "✅",
        "Sub-task": "↪",
    }
    return icons.get(issue_type, "•")


def issue_status_badge(status):
    badges = {
        "Done": "✅",
        "In Progress": "🔄",
        "Backlog": "📋",
        "To Do": "📋",
        "Selected for Development": "🎯",
    }
    return badges.get(status, "❓")


def format_jira_line(issue):
    key = issue["key"]
    fields = issue["fields"]
    summary = fields["summary"]
    status = fields["status"]["name"]
    issue_type = fields["issuetype"]["name"]
    icon = issue_type_icon(issue_type)
    badge = issue_status_badge(status)
    return f"- {icon} **[{key}]** {summary} {badge}"


def format_commit_line(commit):
    sha = commit["sha_short"]
    subject = commit["subject"]
    date = commit["date"][:10]
    return f"  - `{sha}` {subject} _(_{date}_)_"


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

TYPE_SECTION_ORDER = ["feat", "fix", "ci", "docs", "style", "refactor", "chore", "test", "perf"]
TYPE_SECTION_LABELS = {
    "feat": "New Features",
    "fix": "Bug Fixes",
    "ci": "CI / Automation",
    "docs": "Documentation",
    "style": "Style & UI",
    "refactor": "Refactoring",
    "chore": "Chores",
    "test": "Tests",
    "perf": "Performance",
}


def group_traced_by_type(traced):
    """Group traced tickets by their primary commit type."""
    groups = {}
    for item in traced:
        # Use the first feat/fix commit type; skip merge commits in type detection
        primary_type = None
        for c in item["commits"]:
            if c["is_merge"] or not c["conv_type"]:
                continue
            if c["conv_type"] in ("feat", "fix") or primary_type is None:
                primary_type = c["conv_type"]
                if c["conv_type"] in ("feat", "fix"):
                    break
        primary_type = primary_type or "chore"
        groups.setdefault(primary_type, []).append(item)
    return groups


def generate_markdown(version, from_ref, to_ref, traced, jira_only, git_only, untracked,
                       commits, score, generated_at):
    lines = []

    lines.append(f"# Release Notes — v{version}")
    lines.append("")
    lines.append(f"> Generated: {generated_at}  ")
    lines.append(f"> Git range: `{from_ref or 'initial'}..{to_ref}`  ")
    lines.append(f"> Traceability score: **{score}%**")
    lines.append("")

    # --- Summary table ---
    total_commits = sum(1 for c in commits if not c["is_merge"])
    lines.append("## Summary")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---|")
    lines.append(f"| ✅ Fully traced (Jira + Git) | {len(traced)} tickets |")
    lines.append(f"| ⚠️  Jira only (no git commit ref) | {len(jira_only)} tickets |")
    lines.append(f"| ⚠️  Git only (no Jira fixVersion) | {len(git_only)} tickets |")
    lines.append(f"| 🔴 Untracked commits (no ticket) | {len(untracked)} commits |")
    lines.append(f"| **Total commits** | **{total_commits}** (excl. merges) |")
    lines.append("")

    # --- Breaking changes callout ---
    breaking = [item for item in traced for c in item["commits"] if c["conv_breaking"]]
    if breaking:
        lines.append("## ⚠️ Breaking Changes")
        lines.append("")
        for item in breaking:
            bc_commits = [c for c in item["commits"] if c["conv_breaking"]]
            for c in bc_commits:
                lines.append(f"- `{c['sha_short']}` **{c['subject']}**")
        lines.append("")

    # --- Traced: grouped by type ---
    if traced:
        lines.append("## Changes (Fully Traced)")
        lines.append("")
        groups = group_traced_by_type(traced)
        for conv_type in TYPE_SECTION_ORDER:
            if conv_type not in groups:
                continue
            label = TYPE_SECTION_LABELS.get(conv_type, conv_type.title())
            lines.append(f"### {label}")
            lines.append("")
            for item in groups[conv_type]:
                if item["jira"]:
                    lines.append(format_jira_line(item["jira"]))
                else:
                    lines.append(f"- **[{item['key']}]**")
                for c in item["commits"]:
                    lines.append(format_commit_line(c))
            lines.append("")

    # --- Jira only ---
    if jira_only:
        lines.append("## ⚠️ Jira Tickets with No Commit Reference")
        lines.append("")
        lines.append("> These tickets are assigned fixVersion in Jira but no git commit references them.")
        lines.append("> Action: verify implementation evidence or link commits manually.")
        lines.append("")
        for item in jira_only:
            lines.append(format_jira_line(item["jira"]))
        lines.append("")

    # --- Git only ---
    if git_only:
        lines.append("## ⚠️ Committed Work with Missing Jira fixVersion")
        lines.append("")
        lines.append("> Commits reference these tickets but the Jira fixVersion field is not set.")
        lines.append("> Action: set fixVersion in Jira to include in version traceability.")
        lines.append("")
        for item in git_only:
            key = item["key"]
            if item["jira"]:
                fields = item["jira"]["fields"]
                summary = fields["summary"]
                status = fields["status"]["name"]
                badge = issue_status_badge(status)
                lines.append(f"- **[{key}]** {summary} {badge} _(fixVersion not set)_")
            else:
                lines.append(f"- **[{key}]** _(Jira details unavailable)_")
            for c in item["commits"]:
                lines.append(format_commit_line(c))
        lines.append("")

    # --- Untracked ---
    if untracked:
        lines.append("## 🔴 Untracked Commits (No Ticket Reference)")
        lines.append("")
        lines.append("> These commits contain no Jira ticket reference.")
        lines.append("> Action: create retrospective tickets or annotate with ticket refs.")
        lines.append("")
        for c in untracked:
            lines.append(f"- `{c['sha_short']}` {c['subject']} _({c['date'][:10]})_")
        lines.append("")

    # --- All commits log ---
    lines.append("## Full Commit Log")
    lines.append("")
    lines.append("| SHA | Date | Author | Subject |")
    lines.append("|---|---|---|---|")
    for c in commits:
        sha = c["sha_short"]
        date = c["date"][:10]
        author = c["author"]
        subject = c["subject"].replace("|", "\\|")
        lines.append(f"| `{sha}` | {date} | {author} | {subject} |")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON audit log generation
# ---------------------------------------------------------------------------

def generate_audit_log(version, from_ref, to_ref, traced, jira_only, git_only, untracked,
                        commits, score, generated_at, jira_url, jira_project, script_sha,
                        jira_jql_used=None):

    def jira_summary(issue):
        if not issue:
            return None
        f = issue["fields"]
        return {
            "key": issue["key"],
            "summary": f["summary"],
            "status": f["status"]["name"],
            "issue_type": f["issuetype"]["name"],
            "fix_versions": [v["name"] for v in f.get("fixVersions", [])],
        }

    def commit_summary(c):
        return {
            "sha": c["sha"],
            "sha_short": c["sha_short"],
            "author": c["author"],
            "email": c["email"],
            "date": c["date"],
            "subject": c["subject"],
            "ticket_refs": c["ticket_refs"],
            "is_merge": c["is_merge"],
            "conv_type": c["conv_type"],
            "conv_breaking": c["conv_breaking"],
        }

    return {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "generator": "scripts/generate_release_notes.py",
        "generator_sha": script_sha,
        "release": {
            "version": version,
            "git_tag": f"v{version}",
            "git_range": {
                "from_ref": from_ref or "initial_commit",
                "to_ref": to_ref,
            },
        },
        "data_sources": {
            "jira": {
                "url": jira_url,
                "project": jira_project,
                "query": jira_jql_used or f'project = {jira_project} AND fixVersion = "{version}"',
            },
            "git": {
                "range": f"{from_ref or 'initial'}..{to_ref}",
                "total_commits": len(commits),
                "merge_commits_excluded_from_analysis": sum(1 for c in commits if c["is_merge"]),
            },
        },
        "traceability": {
            "score_percent": score,
            "fully_traced_tickets": len(traced),
            "jira_only_tickets": len(jira_only),
            "git_only_tickets": len(git_only),
            "untracked_commits": len(untracked),
            "total_meaningful_commits": sum(1 for c in commits if not c["is_merge"]),
        },
        "reconciliation": {
            "traced": [
                {
                    "key": item["key"],
                    "jira": jira_summary(item["jira"]),
                    "commits": [commit_summary(c) for c in item["commits"]],
                }
                for item in traced
            ],
            "jira_only": [
                {
                    "key": item["key"],
                    "jira": jira_summary(item["jira"]),
                    "note": "Jira fixVersion set but no git commit references this ticket",
                }
                for item in jira_only
            ],
            "git_only": [
                {
                    "key": item["key"],
                    "jira": jira_summary(item["jira"]),
                    "commits": [commit_summary(c) for c in item["commits"]],
                    "note": "Git commit references ticket but Jira fixVersion not set",
                }
                for item in git_only
            ],
            "untracked": [
                {
                    **commit_summary(c),
                    "note": "Commit has no ticket reference",
                }
                for c in untracked
            ],
        },
        "all_commits": [commit_summary(c) for c in commits],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="Generate release notes from Jira + Git")
    p.add_argument("--version", required=True, help="Release version, e.g. 1.0.0")
    p.add_argument("--from-ref", default=None,
                   help="Git start ref (default: auto-detect previous tag). "
                        "Use 'initial' to include all commits from the very first commit.")
    p.add_argument("--to-ref", default=None, help="Git end ref (default: vVERSION tag)")
    p.add_argument("--jira-url", default=DEFAULT_JIRA_URL)
    p.add_argument("--jira-project", default=DEFAULT_JIRA_PROJECT)
    p.add_argument("--jira-user", default=os.environ.get("JIRA_USER", DEFAULT_JIRA_USER))
    p.add_argument("--jira-token", default=os.environ.get("JIRA_TOKEN", ""))
    p.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    p.add_argument("--max-tickets", type=int, default=2000,
                   help="Safety cap on total Jira tickets fetched (default: 2000). "
                        "Jira Cloud hard-limits offset pagination at 10,000.")
    p.add_argument("--jira-jql", default=None,
                   help="Override Jira query with custom JQL (default: project=X AND fixVersion=Y)")
    p.add_argument("--skip-jira", action="store_true", help="Skip Jira queries")
    p.add_argument("--dry-run", action="store_true", help="Print to stdout, do not write files")
    return p.parse_args()


def main():
    args = parse_args()
    version = args.version
    tag = f"v{version}"

    print(f"[release-notes] Generating notes for {tag}", file=sys.stderr)

    # --- Resolve git range ---
    to_ref = args.to_ref or tag
    if not resolve_ref(to_ref):
        if args.to_ref:
            # Explicit ref was given but not found — hard error
            print(f"[ERROR] Git ref '{to_ref}' not found.", file=sys.stderr)
            sys.exit(1)
        else:
            # Tag doesn't exist yet — fall back to HEAD (useful for repos without tags)
            print(f"[WARN] Tag '{tag}' not found — falling back to HEAD", file=sys.stderr)
            to_ref = "HEAD"

    if args.from_ref == "initial":
        from_ref = None
        print(f"[release-notes] Git range: initial commit..{to_ref}", file=sys.stderr)
    elif args.from_ref:
        from_ref = args.from_ref
        print(f"[release-notes] Git range: {from_ref}..{to_ref}", file=sys.stderr)
    else:
        prev_tag = get_previous_tag(tag)
        if prev_tag:
            from_ref = prev_tag
            print(f"[release-notes] Git range: {from_ref}..{to_ref}", file=sys.stderr)
        else:
            from_ref = None
            print(f"[release-notes] Git range: initial commit..{to_ref}", file=sys.stderr)

    # --- Collect git commits ---
    print(f"[release-notes] Collecting commits...", file=sys.stderr)
    commits = get_commits(from_ref, to_ref, args.jira_project)
    print(f"[release-notes] Found {len(commits)} commits ({sum(1 for c in commits if not c['is_merge'])} non-merge)", file=sys.stderr)

    # --- Collect Jira tickets ---
    jira_version_issues = []
    git_only_enriched = {}

    if not args.skip_jira:
        if not args.jira_token:
            print("[WARN] JIRA_TOKEN not set — skipping Jira queries", file=sys.stderr)
            args.skip_jira = True

    if not args.skip_jira:
        print(f"[release-notes] Querying Jira fixVersion={version}...", file=sys.stderr)
        headers = make_jira_headers(args.jira_user, args.jira_token)
        jira_version_issues = get_jira_tickets_by_version(
            args.jira_url, args.jira_project, version, headers,
            jql_override=args.jira_jql, max_tickets=args.max_tickets
        )
        print(f"[release-notes] Found {len(jira_version_issues)} Jira tickets with fixVersion={version}", file=sys.stderr)

        # Enrich git_only tickets with Jira details
        all_git_ticket_refs = set()
        for c in commits:
            all_git_ticket_refs.update(c["ticket_refs"])
        jira_version_keys = {i["key"] for i in jira_version_issues}
        git_only_keys = all_git_ticket_refs - jira_version_keys
        if git_only_keys:
            print(f"[release-notes] Fetching Jira details for {len(git_only_keys)} git-only tickets...", file=sys.stderr)
            git_only_enriched = enrich_git_only_tickets(args.jira_url, sorted(git_only_keys), headers)

    # --- Reconcile ---
    traced, jira_only, git_only, untracked = reconcile(jira_version_issues, commits, args.jira_project)

    # Attach enriched Jira details to git_only items
    for item in git_only:
        item["jira"] = git_only_enriched.get(item["key"])

    score = traceability_score(commits, untracked, git_only)

    print(f"[release-notes] Traceability score: {score}%", file=sys.stderr)
    print(f"[release-notes]   TRACED:     {len(traced)} tickets", file=sys.stderr)
    print(f"[release-notes]   JIRA_ONLY:  {len(jira_only)} tickets", file=sys.stderr)
    print(f"[release-notes]   GIT_ONLY:   {len(git_only)} tickets", file=sys.stderr)
    print(f"[release-notes]   UNTRACKED:  {len(untracked)} commits", file=sys.stderr)

    # --- Generate timestamp and script SHA ---
    generated_at = datetime.now(timezone.utc).isoformat()
    script_sha = run_git("rev-parse", "HEAD")

    # --- Generate outputs ---
    md = generate_markdown(
        version, from_ref, to_ref, traced, jira_only, git_only, untracked,
        commits, score, generated_at
    )
    audit = generate_audit_log(
        version, from_ref, to_ref, traced, jira_only, git_only, untracked,
        commits, score, generated_at, args.jira_url, args.jira_project, script_sha,
        jira_jql_used=args.jira_jql
    )
    audit_json = json.dumps(audit, indent=2)

    if args.dry_run:
        print(md)
        print("\n\n--- AUDIT LOG ---\n")
        print(audit_json)
        return

    # --- Write files ---
    output_dir = Path(args.output_dir)
    audit_dir = output_dir / "audit"
    output_dir.mkdir(parents=True, exist_ok=True)
    audit_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / f"v{version}.md"
    audit_path = audit_dir / f"v{version}.json"

    md_path.write_text(md, encoding="utf-8")
    audit_path.write_text(audit_json, encoding="utf-8")

    print(f"[release-notes] Written: {md_path}", file=sys.stderr)
    print(f"[release-notes] Written: {audit_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
