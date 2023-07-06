from taipy.gui import Markdown
import pandas as pd
from urllib.error import HTTPError

account_page = Markdown("""
<|part|
<center>
<|{username}|input|label=Username|on_action=handle_press_enter|><br/><br/>
<|View account|button|class_name=plain|on_action=handle_view_account_click|><br/><br/>
</center>
|>

<|part|
<|{transact_data}|table|date_format=yyyy-MM-dd HH:mm:ss|rebuild|>
|>
""")

username = ""
transact_data = pd.DataFrame()

def handle_view_account_click(state, id, action, payload):
  url = f"https://raw.githubusercontent.com/{state.orgname}/{state.username}/main/transmits.csv"
  try:
    state.transact_data = pd.read_csv(url, parse_dates=["datetime"], comment="#")
  except HTTPError as e:
    state.transact_data = pd.DataFrame()

handle_press_enter = handle_view_account_click
