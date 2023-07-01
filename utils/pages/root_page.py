from taipy.gui import Markdown, navigate

root_page = Markdown("""
<|layout|columns=1fr auto 1fr|class_name=container align_columns_center|
<|images/logo.jpg|image|width=50px|hover_text=One More Coin|on_action=handle_logo_click|>

<|navbar|lov={[("/account", "Account"), ("/pay", "Pay")]}|>

<|toggle|theme|class_name=nolabel|>
|>

<|content|>

<center>
<font size="4">[One More Coin](/)</font>  
Always open and free  
[About]()  [Documentation]()  [Contact]()  [MIT License]()
</center>
""")

def handle_logo_click(state, id, action):
  navigate(state)
