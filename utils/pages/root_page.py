from taipy.gui import Markdown, navigate
from datetime import datetime

root_page = Markdown("""
<|layout|columns=auto 1 auto|class_name=mb2|
<|images/logo.jpg|image|width=40px|hover_text=Open Oath Coin|on_action=handle_logo_click|>

<|navbar|lov={[("/account", "Account"), ("/pay", "Pay")]}|class_name=fullheight|>

<center>
<|{orgname}|input|label=Currency|>
</center>
|>

<|part|class_name=mb2|
<|content|>
|>

<|part|class_name=text-small|
<center>
[Docs]()&emsp;[About]()&emsp;[Support]()&emsp;[Terms]()&emsp;[Privacy]()<br/>
<|© {year} Open Oath Coin|text|class_name=text-small|>
</center>
|>
""")

year = datetime.now().year

def handle_logo_click(state, id, action):
  navigate(state)
