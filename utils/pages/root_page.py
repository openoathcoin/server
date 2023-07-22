import os
from datetime import datetime

from taipy.gui import Markdown, Icon, navigate
from github import Github

root_page = Markdown("""
<|layout|columns=auto 1 auto auto|class_name=align-columns-bottom mb2|
<|{Icon(os.environ["LOGO_FILE"])}|button|on_action=handle_logo_click|>

<|navbar|lov={[("/account", "Account"), ("/pay", "Pay")]}|>

<center>
<|{"Authorize" if not is_authed else gh.get_user().login}|button|class_name={"" if not is_authed else "success"}|hover_text={"" if not is_authed else "Revoke access"}|on_action=handle_authorize_click|>
</center>

<center>
<|{orgname}|input|label=Currency|>
</center>
|>

<|part|class_name=mb2|
<|content|>
|>

<|part|class_name=text-small|
<center>
[Docs]()&emsp;
[About]()&emsp;
[Support]()&emsp;
[Terms]()&emsp;
[Privacy]()<br/>
<|© {datetime.now().year} {os.environ['APPNAME']}|text|class_name=text-small|>
</center>
|>
""")

def handle_logo_click(state, id, action):
  navigate(state)

def handle_authorize_click(state, id, action):
  if not state.is_authed:
    # authenticate user
    url = f"https://github.com/login/oauth/authorize?client_id={os.environ['CLIENT_ID']}&state={os.environ['STATE']}"
    navigate(state, to=url, tab="_self")
  else:
    # revoke access
    state.gh = Github()
    state.is_authed = False
