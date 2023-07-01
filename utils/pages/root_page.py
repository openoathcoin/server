from taipy.gui import Markdown, navigate
from datetime import datime

root_page = Markdown("""
<|layout|columns=1fr auto 1fr|class_name=container align_columns_center|
<|images/logo.jpg|image|width=50px|hover_text=One More Coin|on_action=handle_logo_click|>

<|navbar|lov={[("/account", "Account"), ("/pay", "Pay")]}|>

<|toggle|theme|class_name=nolabel|>
|>

<|content|>

<center>
<|{datetime.now().year}|text|> © [One More Coin](/) | [About]() | [Contact]() | [Documentation]() | [MIT License]()
</center>
""")

def handle_logo_click(state, id, action):
  navigate(state)
