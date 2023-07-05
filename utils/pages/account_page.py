from taipy.gui import Markdown

account_page = Markdown("""
<|part|render={show_login}|
<center>
<|{password}|input|password=True|label=Access token|><br/><br/>
<|Log in to GitHub account|button|class_name=plain|><br/>
or<br/>
[CREATE GITHUB ACCOUNT](https://github.com/signup?source=login)
</center>
|>
""")

show_login = True
username = ""
password = ""
