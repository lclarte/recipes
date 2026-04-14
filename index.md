---
layout: default
title: Recipes
---

# All recipes

{% assign sorted = site.recipes | sort: "date" | reverse %}
{% if sorted.size > 0 %}
<ul class="recipe-list">
  {% for recipe in sorted %}
  <li>
    <a href="{{ recipe.url | relative_url }}">{{ recipe.title }}</a>
    <span class="meta">by {{ recipe.author }} · {{ recipe.date | date: "%b %-d, %Y" }}</span>
    {% if recipe.description %}<p>{{ recipe.description }}</p>{% endif %}
  </li>
  {% endfor %}
</ul>
{% else %}
<p>No recipes yet.</p>
{% endif %}
