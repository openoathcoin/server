from taipy.gui import Markdown
import pandas as pd
from urllib.error import HTTPError

account_page = Markdown("""
<|part|
<center>
<|{username}|input|label=GitHub username|on_action=handle_press_enter|on_change=handle_username_change|><br/><br/>
<|View account|button|class_name=plain|on_action=handle_view_account_click|><br/><br/>
<|{nodata_msg}|text|>
</center>
|>

<|part|
<|Balance: {balance} Credit: {credit} Debt: {debt}|text|><br/><br/>
<|{transact_data}|table|columns={columns}|date_format=yyyy-MM-dd HH:mm:ss|rebuild|>
|>
""")

username = ""
nodata_msg = ""
columns = ["datetime", "froto", "coins", "description"]  # columns to display
transact_data = pd.DataFrame(columns=columns)
balance = credit = debt = pd.NA

def handle_view_account_click(state, id, action, payload):
  url = f"https://raw.githubusercontent.com/{state.orgname}/{state.username}/main/transmits.csv"
  try:
    state.transact_data = pd.read_csv(url, parse_dates=["datetime"], comment="#")
  except HTTPError as e:
    if state.username:
      state.nodata_msg = "No data found for user in given currency"
    else:
      state.nodata_msg = "Enter GitHub username to view account"
    
    return
  
  state.balance = state.transact_data["balance"].iat[-1]
  state.credit = state.transact_data["credit"].iat[-1]
  state.debt = state.transact_data["debt"].iat[-1]

handle_press_enter = handle_view_account_click

def handle_username_change(state, varname, value):
  # reset data
  if state.nodata_msg:
    state.nodata_msg = ""
  if not state.transact_data.empty:
    state.transact_data = pd.DataFrame(columns=state.columns)
  if not state.balance is state.credit is state.debt is pd.NA:
    state.balance = state.credit = state.debt = pd.NA
