#!/usr/bin/env python3

# note: don't name main script __main__.py or gunicorn won't find app in __main__

import taipy as tp
from utils.pages.root_page import root_page
from utils.pages.account_page import account_page
from utils.pages.pay_page import pay_page

# flask_app = Flask(__name__)

# @flask_app.route("/authorized", methods=["GET"])
# def github_callback():
#     """Authenticate the user and displays their data."""
#     args = request.args
#     request_token = args.get('code')

#     CLIENT_ID = app.config['CLIENT_ID']
#     CLIENT_SECRET = app.config['CLIENT_SECRET']
#     access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, request_token)

#     user_data = get_user_data(access_token)
#     return render_template('success.html', userData=user_data)

# @flask_app.route("/login")
# def login():
#     return "The home page."

# gui = tp.Gui(page="# Taipy application", flask=flask_app)

title = "One More Coin: A currency based on trust and transparency"  # text displayed on browser tab
logo_file = "images/logo.jpg"  # icon displayed on browser tab

# global bound variables shared by pages
orgname = "onemorecoin"

pages = {"/": root_page,
         "account": account_page,
         "pay": pay_page}

gui = tp.Gui(pages=pages)

if __name__ == "__main__":
  # for development
  # run source env/bin/activate to activate virtual environment
  # run python main.py in virtual environment

  tp.run(gui, host="localhost", port=8000, title=title, favicon=logo_file, watermark="", debug=True, use_reloader=True)  # default host:port 127.0.0.1:5000
  # tp.run(gui, host="localhost", port=8000, title=title, favicon=logo_file, watermark="")  # run in notebook
else:
  # for production
  # run source env/bin/activate to activate virtual environment
  # run gunicorn --bind localhost:8000 --worker-class gevent --worker-connections 1000 --workers $(nproc) --threads 1 main:app in virtual environment, adjust nproc and threads when more memory available
  # run uwsgi --http localhost:8000 --http-websockets --master --gevent 1000 --processes $(nproc) --threads 1 --module main:app in virtual environment, adjust nproc and threads when more memory available

  app = tp.run(gui, host="localhost", port=8000, title=title, favicon=logo_file, watermark="", run_server=False)
