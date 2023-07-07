from taipy.gui import Markdown, navigate
from datetime import datetime

root_page = Markdown("""
<|layout|columns=auto 1 auto|class_name=mb2|
<|images/logo.jpg|image|width=40px|hover_text=One More Coin|on_action=handle_logo_click|>

<|navbar|lov={[("/account", "Account"), ("/pay", "Pay")]}|class_name=fullheight|>

<|{orgname}|input|label=Currency|>
|>

<|part|class_name=mb3|
<|content|>
|>

<|part|class_name=text-small|
<center>
[Docs]()&emsp;[About]()&emsp;[Support]()&emsp;[Terms]()&emsp;[Privacy]()<br/>
<|© {year} One More Coin|text|class_name=text-small|>
</center>
|>
""")

year = datetime.now().year

def handle_logo_click(state, id, action):
  navigate(state)
