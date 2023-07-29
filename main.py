#!/usr/bin/env python3

# note: don't name main script __main__.py or gunicorn not find app in __main__

import os
from operator import attrgetter
from io import BytesIO

import taipy as tp
from taipy.gui import navigate
from flask import Flask, request, session, redirect
from github import Github, UnknownObjectException
import pandas as pd

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

  session["code"] = request.args["code"]
  session["state"] = request.args["state"]

  return redirect("/account")

pages = {"/": root_page,
         "account": account_page,
         "pay": pay_page}

gui = tp.Gui(pages=pages, flask=flask_app)

# variables shared by pages
gh = Github()  # unauthenticated
orgs = []  # list of currencies to choose from
org = None  # selected currency
username = ""
user = None
transact_data = None
msg = ""

def on_navigate(state, pagename):
  if pagename == "account" and not state.gh._Github__requester.auth and "code" in session and "state" in session and session["state"] == os.environ["STATE"]:
    # authenticate with authorization code
    gh_app = Github().get_oauth_application(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])
    token = gh_app.get_access_token(session["code"])
    auth = gh_app.get_app_user_auth(token)
    with state as s:
      s.gh = Github(auth=auth)  # authenticated
      session.pop("code")  # delete authorization code
      session.pop("state")

      s.orgs = sorted(s.gh.get_user().get_orgs(), key=attrgetter("login"))
      s.org = s.orgs[0] if s.orgs else None
      s.username = s.gh.get_user().login
    
    handle_view_account_click(state, "", "", {})
  
  return pagename

def handle_logo_click(state, id, action):
  navigate(state)
  
  if state.gh._Github__requester.auth:
    state.username = state.gh.get_user().login
    handle_view_account_click(state, "", "", {})

def handle_view_account_click(state, id, action, payload):
  # reset
  with state as s:
    s.user = None
    s.transact_data = None
  
  if not state.username:
    return
  
  if not state.org:
    state.msg = "You don't have access to any currencies."
    return
  
  state.msg = "Fetching data..."

  try:
    user = state.gh.get_user(state.username)
    memship = user.get_organization_membership(state.org.login)
  except UnknownObjectException:
    state.msg = "Couldn't find user in given currency."
    return
  
  try:
    repo = state.org.get_repo(user.login)
    transact_file = repo.get_contents("transmits.csv")
  except UnknownObjectException:
    state.msg = "User doesn't have any transaction records."
    return
  
  try:
    transact_data = pd.read_csv(BytesIO(transact_file.decoded_content), parse_dates=["Datetime"], comment="#")
  except:
    state.msg = "Couldn't read transaction file."
    return
  
  with state as s:
    s.user = user
    s.transact_data = transact_data
  
  state.msg = ""

handle_username_keypress = handle_view_account_click

if __name__ == "__main__":
  # for development
  # run source env/bin/activate to activate virtual environment
  # run python main.py in virtual environment

  tp.run(gui, host="localhost", port=8000, title=os.environ["TITLE"], favicon=os.environ["LOGO_FILE"], watermark="", debug=True, use_reloader=True)  # default host:port 127.0.0.1:5000
  # tp.run(gui, host="localhost", port=8000, title=os.environ["TITLE"], favicon=os.environ["LOGO_FILE"], watermark="")  # run in notebook
else:
  # for production
  # run source env/bin/activate to activate virtual environment
  # run gunicorn --bind localhost:8000 --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker --worker-connections 1000 --workers $(nproc) --threads 1 main:app in virtual environment, adjust nproc and threads when more cpus and memory available
  # run gunicorn --bind localhost:8000 --worker-class gevent --worker-connections 1000 --workers $(nproc) --threads 1 main:app in virtual environment, adjust nproc and threads when more cpus and memory available
  # run uwsgi --http localhost:8000 --http-websockets --master --gevent 1000 --processes $(nproc) --threads 1 --module main:app in virtual environment, adjust nproc and threads when more cpus and memory available

  app = tp.run(gui, host="localhost", port=8000, title=os.environ["TITLE"], favicon=os.environ["LOGO_FILE"], watermark="", run_server=False)
