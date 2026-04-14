# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project

Personal recipe website for Baru & Lulu. Jekyll static site hosted on GitHub Pages.

## Stack

- **Jekyll** with GitHub Pages native build (no local build step required)
- Recipes: Markdown files in `recipes/` with YAML frontmatter
- Styles: `assets/css/style.css`
- Images: `assets/images/recipes/<slug>/`

## Adding a recipe

1. Create `recipes/my-dish.md` with this format:

```markdown
---
title: My Dish
description: Optional one-liner
author: Baru
date: 2026-04-14
images:          # optional
  - photo.jpg
---

## Ingredients

- item 1
- item 2

## Instructions

1. Step one
2. Step two
```

2. If the recipe has photos, add them to `assets/images/recipes/my-dish/`
3. `git add . && git commit -m "add my-dish" && git push`
4. GitHub Pages builds and deploys in ~30 seconds

Or use GitHub's web editor (no local git needed).

## Local preview (optional)

```bash
bundle install
bundle exec jekyll serve
# open http://localhost:4000
```

## GitHub Pages setup

Settings > Pages > Source: Deploy from branch `main` / `/ (root)`

The repo must be **public** for GitHub Pages on a free GitHub account.

## Structure

- `_config.yml` — Jekyll configuration, collection definition
- `_layouts/default.html` — base HTML layout
- `_layouts/recipe.html` — individual recipe page layout
- `_includes/nav.html` — shared nav
- `index.md` — home page (recipe list)
- `recipes/*.md` — one file per recipe
- `assets/css/style.css` — all styles
- `assets/images/recipes/<slug>/` — recipe photos
