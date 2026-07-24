#!/usr/bin/env bash
# Manages the Jekyll dev server as a background process with tailable logs.
# Port assignment: apisaurus docs/PORT-REGISTRY.md, ADR 0002 (project id 05, web).
set -euo pipefail

cd "$(dirname "$0")/.."

PORT="${PORT:-42005}"
START_CMD=(bundle exec jekyll serve --port "$PORT" --no-watch)

PID_FILE=".dev-server.pid"
LOG_FILE=".dev-server.log"

start() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Already running (pid $(cat "$PID_FILE")). Use restart to reload."
    exit 0
  fi
  : > "$LOG_FILE"
  nohup "${START_CMD[@]}" >> "$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"
  echo "Started on http://localhost:$PORT (pid $(cat "$PID_FILE")), logging to $LOG_FILE"
}

stop() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    kill "$(cat "$PID_FILE")"
    rm -f "$PID_FILE"
    echo "Stopped."
  else
    echo "Not running."
    rm -f "$PID_FILE"
  fi
}

restart() {
  stop || true
  sleep 1
  start
}

logs() {
  tail -n "${1:-80}" "$LOG_FILE"
}

status() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Running on http://localhost:$PORT (pid $(cat "$PID_FILE"))"
  else
    echo "Not running."
  fi
}

case "${1:-}" in
  start) start ;;
  stop) stop ;;
  restart) restart ;;
  logs) logs "${2:-80}" ;;
  status) status ;;
  *) echo "Usage: $0 {start|stop|restart|status|logs [n]}"; exit 1 ;;
esac
