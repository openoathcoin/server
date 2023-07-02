from taipy.gui import Markdown

account_page = Markdown("""
<|part|render={show_login}|
<center>
<|{username}|input|label=Username|><br/>
<|{password}|input|password=True|label=Password|><br/><br/>
<|Log in to GitHub account|button|class_name=plain|><br/>
or<br/>
[CREATE GITHUB ACCOUNT](https://github.com/signup?source=login)
</center>
|>
""")

show_login = True
username = ""
password = ""
