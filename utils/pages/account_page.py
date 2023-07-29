from taipy.gui import Markdown

account_page = Markdown("""
<|part|render={not gh._Github__requester.auth}|class_name=mb1|
<center>
<|Authorize to view accounts.|text|>
</center>
|>

<|part|render={gh._Github__requester.auth}|class_name=mb1|
<center>
<|{username}|input|label=Username|class_name=mb1|on_action=handle_username_keypress|><br/>
<|View account|button|class_name=plain mb1|on_action=handle_view_account_click|><br/>
<|{msg}|text|>
</center>
|>

<|part|render={user}|class_name=mb1|
<center>
<|{user.avatar_url if user else ""}|image|width=50px|label=Avatar|hover_text=Pay {user.login if user else ''}|on_action=handle_avatar_click|><br/>
<|{user.name if user and user.name else ""}|text|>
</center>
|>

<|part|render={transact_data is not None}|class_name=mb1|
<center>
<|Balance: {transact_data['Balance'].iat[-1] if transact_data is not None else ''}|text|>&emsp;
<|Credit: {transact_data['Credit'].iat[-1] if transact_data is not None else ''}|text|>&emsp;
<|Debt: {transact_data['Debt'].iat[-1] if transact_data is not None else ''}|text|><br/><br/>
<|{transact_data if transact_data is not None else pd.DataFrame()}|table|columns={["Datetime", "Froto", "Coins", "Description"] if transact_data is not None else []}|date_format=yyyy-MM-dd HH:mm:ss|rebuild|>
</center>
|>
""")

def handle_avatar_click(state, id, action):
  pass
