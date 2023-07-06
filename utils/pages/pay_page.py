from taipy.gui import Markdown
from github import Auth, Github

pay_page = Markdown("""
<|part|render={show_login}|
<center>
<|{access_token}|input|password=True|label=Access token|><br/><br/>
<|Log in to GitHub account|button|class_name=plain|on_action=handle_login_click|><br/>
or<br/>
[CREATE GITHUB ACCOUNT](https://github.com/signup?source=login)
</center>
|>
""")

show_login = True
access_token = ""
github = None

def handle_login_click(state, id, action):
  auth = Auth.Token(state.access_token)
  state.github = Github(auth=auth)
  state.show_login = False

  print(state.github.get_user().login)
