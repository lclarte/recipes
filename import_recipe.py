#!/usr/bin/env python3
"""
Import a recipe from a .txt file.
Usage: python import_recipe.py <username> <recipe.txt>

File format:
    Title: My Recipe
    Description: Optional one-liner

    Ingredients:
    200g pasta
    2 eggs

    Instructions:
    1. Boil water
    2. Cook pasta
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal, Base, engine
from app.models import User, Recipe

Base.metadata.create_all(bind=engine)


def parse_recipe(text: str) -> dict:
    data = {"title": "", "description": "", "ingredients": "", "instructions": ""}
    current_section = None
    buffer = []

    for line in text.splitlines():
        stripped = line.strip()
        lower = stripped.lower()

        if lower.startswith("title:"):
            data["title"] = stripped[6:].strip()
        elif lower.startswith("description:"):
            data["description"] = stripped[12:].strip()
        elif lower == "ingredients:":
            if current_section:
                data[current_section] = "\n".join(buffer).strip()
            current_section = "ingredients"
            buffer = []
        elif lower == "instructions:":
            if current_section:
                data[current_section] = "\n".join(buffer).strip()
            current_section = "instructions"
            buffer = []
        elif current_section:
            buffer.append(line)

    if current_section:
        data[current_section] = "\n".join(buffer).strip()

    return data


def import_recipe(username: str, filepath: str) -> None:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: file '{filepath}' not found.")
        sys.exit(1)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"Error: user '{username}' not found.")
            sys.exit(1)

        data = parse_recipe(path.read_text(encoding="utf-8"))

        missing = [f for f in ("title", "ingredients", "instructions") if not data[f]]
        if missing:
            print(f"Error: missing required section(s): {', '.join(missing)}")
            sys.exit(1)

        recipe = Recipe(
            title=data["title"],
            description=data["description"],
            ingredients=data["ingredients"],
            instructions=data["instructions"],
            author_id=user.id,
        )
        db.add(recipe)
        db.commit()
        print(f"Imported '{data['title']}' (id={recipe.id}).")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python import_recipe.py <username> <recipe.txt>")
        sys.exit(1)
    import_recipe(sys.argv[1], sys.argv[2])
