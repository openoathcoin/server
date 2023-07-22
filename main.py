#!/usr/bin/env python3

# note: don't name main script __main__.py or gunicorn not find app in __main__

import os

import taipy as tp
from flask import Flask, request, session, redirect
from github import Github

from utils.pages.root_page import root_page
from utils.pages.account_page import account_page
from utils.pages.pay_page import pay_page

flask_app = Flask(__name__)
flask_app.secret_key = os.environ["SECRET_KEY"]

@flask_app.route("/handle-auth-code")
def handle_auth_code():
  """
  get and store authorization code from github callback
  """

  session["code"] = request.args.get("code")

  return redirect("/account")

# bound variables shared by pages
orgname = os.environ["ORGNAME"]  # currency
gh = Github()  # unauthenticated user
is_authed = False  # user authenticated or not

pages = {"/": root_page,
         "account": account_page,
         "pay": pay_page}

def on_navigate(state, pagename):
  # authenticate user with authorization code
  if pagename == "account" and not state.is_authed and "code" in session:
    gh_app = Github().get_oauth_application(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])
    token = gh_app.get_access_token(session["code"])
    auth = gh_app.get_app_user_auth(token)
    state.gh = Github(auth=auth)  # authenticated user
    state.is_authed = True
    
    session.pop("code")  # delete authorization code
  
  return pagename

# def on_init(state):
#   if "code" in session:
#     gh_app = Github().get_oauth_application(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])
#     token = gh_app.get_access_token(session["code"])
#     auth = gh_app.get_app_user_auth(token)
#     state.gh = Github(auth=auth)  # authenticated user
#     state.is_authed = True

#     session.pop("code")  # delete authorization code

gui = tp.Gui(pages=pages, flask=flask_app)

if __name__ == "__main__":
  # for development
  # run source env/bin/activate to activate virtual environment
  # run python main.py in virtual environment

  tp.run(gui, host="localhost", port=8000, title=os.environ["TITLE"], favicon=os.environ["LOGO_FILE"], watermark="", debug=True, use_reloader=True, flask_log=True)  # default host:port 127.0.0.1:5000
  # tp.run(gui, host="localhost", port=8000, title=os.environ["TITLE"], favicon=os.environ["LOGO_FILE"], watermark="")  # run in notebook
else:
  # for production
  # run source env/bin/activate to activate virtual environment
  # run gunicorn --bind localhost:8000 --worker-class gevent --worker-connections 1000 --workers $(nproc) --threads 1 main:app in virtual environment, adjust nproc and threads when more memory available
  # run uwsgi --http localhost:8000 --http-websockets --master --gevent 1000 --processes $(nproc) --threads 1 --module main:app in virtual environment, adjust nproc and threads when more memory available

  app = tp.run(gui, host="localhost", port=8000, title=os.environ["TITLE"], favicon=os.environ["LOGO_FILE"], watermark="", run_server=False)
