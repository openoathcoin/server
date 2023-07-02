from taipy.gui import Markdown, navigate
from datetime import datetime

year = datetime.now().year

root_page = Markdown("""
<|layout|columns=1 auto 1|class_name=container align_columns_center|
<|images/logo.jpg|image|width=55px|hover_text=One More Coin|on_action=handle_logo_click|>

<|navbar|lov={[("/account", "Account"), ("/pay", "Pay")]}|>

<|toggle|theme|class_name=nolabel|>
|>

<|content|>

<center>
[Docs]()&emsp;[About]()&emsp;[Support]()&emsp;[Terms]()&emsp;[Privacy]()<br />
<|© {year} One More Coin|text|>
</center>
""")

def handle_logo_click(state, id, action):
  navigate(state)
