from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.staticfiles import StaticFiles

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session

from routes import account
from database import DB, Session


templates = Jinja2Templates(directory="templates")

app = FastAPI()

session: Session = DB.get_session()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
account.addAccountRoutes(app, session, templates)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


# @app.post("/add")
# def add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
#     new_todo = models.Todo(title=title)
#     db.add(new_todo)
#     db.commit()

#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


# @app.get("/update/{todo_id}")
# def update(request: Request, todo_id: int, db: Session = Depends(get_db)):
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     todo.complete = not todo.complete
#     db.commit()

#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


# @app.get("/delete/{todo_id}")
# def delete(request: Request, todo_id: int, db: Session = Depends(get_db)):
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     db.delete(todo)
#     db.commit()

#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
