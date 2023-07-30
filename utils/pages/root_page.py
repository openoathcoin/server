import os
from datetime import datetime

from taipy.gui import Markdown, Icon, navigate
from github import Github

root_page = Markdown("""
<|layout|columns=auto 1 auto auto|class_name=align-columns-bottom mb2|
<|{Icon(os.environ["LOGO_FILE"])}|button|on_action=handle_logo_click|>

<|navbar|lov={[("/account", "Account"), ("/pay", "Pay")]}|>

<center>
<|{"Authorize" if not gh._Github__requester.auth else gh.get_user().login}|button|class_name={"" if not gh._Github__requester.auth else "success"}|hover_text={"" if not gh._Github__requester.auth else "Revoke access"}|on_action=handle_authorize_click|>
</center>

<|part|render={gh._Github__requester.auth}|
<center>
<|{org}|selector|lov={orgs}|type=Organization|adapter={lambda o: (o.login, Icon(o.avatar_url, o.login))}|dropdown|label=Currency|>
</center>
|>
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

def handle_authorize_click(state, id, action):
  if not state.gh._Github__requester.auth:
    navigate(state, to="/authorize", tab="_self")
  else:
    # revoke access
    with state as s:
      s.gh = Github()
      s.orgs = []
      s.org = None
      s.username = ""
      s.user = None
      s.transact_data = None
      s.msg = ""
