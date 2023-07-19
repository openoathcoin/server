from taipy.gui import Markdown, notify
import pandas as pd
from urllib.error import HTTPError
from http.client import InvalidURL

from utils.pages.timezones import timezones

account_page = Markdown("""
<|layout|columns=auto 1|
<|part|class_name=mb1|
<center>
<|{username}|input|label=GitHub username|class_name=mb1|on_action=handle_username_keypress_enter|>
<|{tz}|selector|lov={timezones}|value_by_id|dropdown|label=Timezone|class_name=mb1|on_change=handle_tz_change|>
<|View account|button|class_name=plain|on_action=handle_view_account_click|>
</center>
|>

<|part|class_name=mb1|
<|layout|columns=auto 1|class_name=mb1 pt-half|
<|https://avatars.githubusercontent.com/u/108220667?v=4|image|width=45px|hover_text=Open Oath Coin|>

<|Name: {name}|text|>&emsp;<|Membership: {role}|text|><br/>
<|Balance: {balance}|text|>&emsp;<|Credit: {credit}|text|>&emsp;<|Debt: {debt}|text|>
|>

<|part|
<|{transact_data}|table|columns={columns}|date_format=yyyy-MM-dd HH:mm:ss|rebuild|>
|>
|>
|>
""")

username = ""
name = ""
role = ""
tz = timezones[0][0]
# show_balance = False
columns = ["Datetime", "Froto", "Coins", "Description"]  # columns to display
transact_data = pd.DataFrame(columns=columns)
balance = credit = debt = ""

def handle_view_account_click(state, id, action, payload):
  # retrieve transaction data
  url = f"https://raw.githubusercontent.com/{state.orgname}/{state.username}/main/transmits.csv"
  with state as s:
    try:
      transact_data = pd.read_csv(url, parse_dates=["Datetime"], comment="#")
      transact_data["Datetime"] = transact_data["Datetime"].dt.tz_convert(s.tz)  # transaction data not empty if url exist
      s.transact_data = transact_data
    except HTTPError as e:
      if s.username and s.orgname:
        notify(s, "error", "No data found for user in given currency")
      else:
        notify(s, "error", "Enter both username and currency to view account")
      
      return
    except InvalidURL as e:
      notify(s, "error", "Invalid username or currency")
      return
    
    s.balance = s.transact_data["Balance"].iat[-1]
    s.credit = s.transact_data["Credit"].iat[-1]
    s.debt = s.transact_data["Debt"].iat[-1]
    # s.show_balance = True

handle_username_keypress_enter = handle_view_account_click

def handle_tz_change(state, varname, value):
  transact_data = state.transact_data
  
  # update datetime to new timezone
  if transact_data["Datetime"].empty:
    return
  transact_data["Datetime"] = transact_data["Datetime"].dt.tz_convert(state.tz)  # direct update on state.transact_data["Datetime"] not work
  state.transact_data = transact_data

# def handle_username_change(state, varname, value):
#   # reset data
#   with state as s:
#     if s.show_balance:
#       s.show_balance = False
    
#     # if not s.transact_data.empty:
#     #   s.transact_data = pd.DataFrame(columns=s.columns)
    
#     # if not s.balance == s.credit == s.debt == "":
#     #   s.balance = s.credit = s.debt = ""
