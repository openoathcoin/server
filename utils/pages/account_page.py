from taipy.gui import Markdown, notify
import pandas as pd
from urllib.error import HTTPError
from http.client import InvalidURL

account_page = Markdown("""
<|part|class_name=mb1|
<center>
<|{username}|input|label=GitHub username|on_action=handle_press_enter|><br/><br/>
<|View account|button|class_name=plain|on_action=handle_view_account_click|>
</center>
|>

<|part|render={show_balance}|
<|Balance: {balance} Credit: {credit} Debt: {debt}|text|><br/><br/>
<|{transact_data}|table|columns={columns}|date_format=yyyy-MM-dd HH:mm:ss|rebuild|>
|>
""")

username = ""
show_balance = False
columns = ["datetime", "froto", "coins", "description"]  # columns to display
transact_data = pd.DataFrame(columns=columns)
balance = credit = debt = ""

def handle_view_account_click(state, id, action, payload):
  # retrieve transaction data
  url = f"https://raw.githubusercontent.com/{state.orgname}/{state.username}/main/transmits.csv"
  with state as s:
    try:
      # s.transact_data = pd.read_csv(url, comment="#")
      s.transact_data = pd.read_csv(url, parse_dates=["datetime"], comment="#")
    except HTTPError as e:
      if state.username and state.orgname:
        notify(state, "error", "No data found for user in given currency")
      else:
        notify(state, "error", "Enter both username and currency to view account")
      
      return
    except InvalidURL as e:
      notify(state, "error", "Invalid username or currency")
      return
    
    s.balance = s.transact_data["balance"].iat[-1]
    s.credit = s.transact_data["credit"].iat[-1]
    s.debt = s.transact_data["debt"].iat[-1]
    s.show_balance = True

handle_press_enter = handle_view_account_click

# def handle_username_change(state, varname, value):
#   # reset data
#   with state as s:
#     if s.show_balance:
#       s.show_balance = False
    
#     # if not s.transact_data.empty:
#     #   s.transact_data = pd.DataFrame(columns=state.columns)
    
#     # if not s.balance == s.credit == s.debt == "":
#     #   s.balance = s.credit = s.debt = ""
