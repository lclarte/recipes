import os
import uuid
from fastapi import APIRouter, Depends, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import decode_token
from app import models

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "app/static/uploads"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


def get_current_user(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return None
    username = decode_token(token)
    if not username:
        return None
    return db.query(models.User).filter(models.User.username == username).first()


@router.get("/", response_class=HTMLResponse)
async def list_recipes(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    recipes = db.query(models.Recipe).order_by(models.Recipe.created_at.desc()).all()
    return templates.TemplateResponse("recipes/list.html", {"request": request, "recipes": recipes, "user": user})


@router.get("/recipes/new", response_class=HTMLResponse)
async def new_recipe_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("recipes/form.html", {"request": request, "user": user, "recipe": None})


@router.post("/recipes/new")
async def create_recipe(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    ingredients: str = Form(...),
    instructions: str = Form(...),
    images: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    recipe = models.Recipe(
        title=title,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
        author_id=user.id,
    )
    db.add(recipe)
    db.flush()

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    for image in images:
        if not image.filename or image.content_type not in ALLOWED_TYPES:
            continue
        ext = os.path.splitext(image.filename)[1].lower()
        filename = f"{uuid.uuid4()}{ext}"
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
            f.write(await image.read())
        db.add(models.RecipeImage(recipe_id=recipe.id, filename=filename))

    db.commit()
    return RedirectResponse(url=f"/recipes/{recipe.id}", status_code=302)


@router.get("/recipes/{recipe_id}", response_class=HTMLResponse)
async def view_recipe(recipe_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("recipes/detail.html", {"request": request, "recipe": recipe, "user": user})
