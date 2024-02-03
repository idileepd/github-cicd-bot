from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models import Account, Repository


def addAccountRoutes(app: FastAPI, session: Session, templates: Jinja2Templates):

    @app.get("/accounts")
    def accounts(request: Request):
        accounts = session.query(Account).all()
        return templates.TemplateResponse(
            "/accounts.html",
            {"request": request, "accounts": accounts},
        )

    @app.post("/accounts")
    def createAccount(request: Request, form: dict = Form(...)):
        # accounts = session.query(Account).all()
        print(form)
        # account_id = request.form["account_id"]
        # name = request.form["name"]
        # git_token = Secure.encrypt(request.form["git_token"])

        # # Create new Account instance
        # new_account = Account(accountId=account_id, name=name, gitToken=git_token)

        # # Add to the database
        # self.session.add(new_account)
        # self.session.commit()

        # # refresh if any user listening
        # accounts = session.query(Account).all()
        # socketio.emit(
        #     "refresh_accounts", {"accounts": [acc.get_json() for acc in accounts]}
        # )

        # return redirect("/accounts")

        url = app.url_path_for("home")
        return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

    @app.get("/accounts/{accountId}")
    def home(request: Request, accountId: str):
        try:
            account = session.query(Account).filter_by(accountId=accountId).first()
            if account == None:
                raise Exception("Account not found")

            repos = session.query(Repository).filter_by(accountId=accountId).all()
            return templates.TemplateResponse(
                "repos.html",
                {
                    "request": request,
                    "repos": repos,
                    "account": account,
                },
            )
        except Exception as e:
            print(e)
            return templates.TemplateResponse(
                "/404.html", {"request": request, "message": "Account Not Found"}
            )
