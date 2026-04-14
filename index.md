---
layout: default
title: Recipes
---

# All recipes

{% assign sorted = site.recipes | sort: "date" | reverse %}

{% assign all_tags = "" | split: "" %}
{% for recipe in sorted %}
  {% for tag in recipe.tags %}
    {% unless all_tags contains tag %}
      {% assign all_tags = all_tags | push: tag %}
    {% endunless %}
  {% endfor %}
{% endfor %}

{% if all_tags.size > 0 %}
<div class="tag-filters">
  <button class="tag-btn active" data-tag="all">All</button>
  {% for tag in all_tags %}
  <button class="tag-btn" data-tag="{{ tag }}">{{ tag }}</button>
  {% endfor %}
</div>
{% endif %}

{% if sorted.size > 0 %}
<ul class="recipe-list">
  {% for recipe in sorted %}
  <li data-tags="{{ recipe.tags | join: ' ' }}">
    <a href="{{ recipe.url | relative_url }}">{{ recipe.title }}</a>
    <span class="meta">by {{ recipe.author }} · {{ recipe.date | date: "%b %-d, %Y" }}</span>
    {% if recipe.description %}<p>{{ recipe.description }}</p>{% endif %}
  </li>
  {% endfor %}
</ul>
{% else %}
<p>No recipes yet.</p>
{% endif %}

<script>
document.querySelectorAll('.tag-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tag-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const tag = btn.dataset.tag;
    document.querySelectorAll('.recipe-list li').forEach(li => {
      li.hidden = tag !== 'all' && !li.dataset.tags.split(' ').includes(tag);
    });
  });
});
</script>
