
from taipy.gui import Gui

text = "Original text"

page = """
# Getting started with Taipy GUI

My text: <|{text}|>

<|{text}|input|>
"""

if __name__ == "__main__":

  Gui(page).run(host="localhost", port=8000)
