#!/usr/bin/env python3

# notes:
  # don't name main script __main__.py or gunicorn won't find app in __main__
  # set production server to listen at localhost:5000, localhost:8000 won't work

import taipy as tp
from utils.pages import main_page_title, login_page, root_page


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

pages = {"/":root_page,
         "login":login_page}

gui = tp.Gui(pages=pages)

if __name__ == "__main__":
  # for development
  # run source env/bin/activate to activate virtual environment
  # run python main.py in virtual environment
  tp.run(gui, title=main_page_title, favicon="images/logo.jpg")  # listening at localhost:5000 by default
else:
  # for production
  # run source env/bin/activate to activate virtual environment
  # run gunicorn --bind localhost:5000 --worker-class gevent --worker-connections 1000 --workers $(nproc) --threads 1 main:app in virtual environment, adjust nproc and threads when more memory available
  # run uwsgi --http localhost:5000 --http-websockets --master --gevent 1000 --processes $(nproc) --threads 1 --module main:app in virtual environment, adjust nproc and threads when more memory available
  app = tp.run(gui, title=main_page_title, favicon="images/logo.jpg", run_server=False)
