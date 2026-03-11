---
title: Promo Videos
order: 5
slug: promo-videos
hero_image: matthew-kwong-qJgW5ewKCO8-unsplash-e1664978813403.jpg
summary: Produce a video of your Open Banking journey that you can use for marketing, training, or any other purpose.
related_services:
  - consent-for-rent
  - payment-testing
---

Produce a video of your Open Banking journey that you can use for marketing, training, or any other purpose.

---

## Open Banking Video Library

{% assign sorted_videos = site.videos | sort: "order" %}
<div class="video-tile-grid">
  {% for video in sorted_videos %}
  <div class="flex-wrap-bottom-div">
    {% if video.youtube_id != "TBD" %}
    <a class="m-0" href="{{ video.url }}">
      <img src="https://img.youtube.com/vi/{{ video.youtube_id }}/mqdefault.jpg"
           class="projects-img mb-q br-5 img-hover"
           alt="{{ video.title }}"
           title="{{ video.title }}"
           loading="lazy">
      <h4>{{ video.title }}</h4>
      <p class="fs-14">{{ video.summary }}</p>
    </a>
    {% else %}
    <div class="video-tile-placeholder">
      <div class="video-tile-placeholder-img mb-q br-5"></div>
      <h4>{{ video.title }}</h4>
      <p class="fs-14">{{ video.summary }}</p>
      <span class="video-tag">Coming soon</span>
    </div>
    {% endif %}
  </div>
  {% endfor %}
</div>
