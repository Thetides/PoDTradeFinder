import requests
import json
import time
from bs4 import BeautifulSoup

account = json.load(open("account.json"))

url = "https://pathofdiablo.com/p/"
trade_url = "?trade"

body = {"login": "", "pw": "{}".format(account["password"]), "user": "{}".format(account["username"])}
r = requests.session()
resp = r.post(url, data=body)
# End Auth


def update_trades(r):
    trade_resp = r.get(url+trade_url)
    trade_content = trade_resp.content
    soup = BeautifulSoup(trade_content, 'html.parser')

    # Pull all trades
    trade_find = soup.find("table", {"id":"trades"})
    # Build list of trades
    return trade_find.find_all("tr")


# Parse Trades
def format_trades(trades):
    all_trades = []
    for trade in trades:
        data = {}
        if trade is not None:
            new_item = trade.find("strong")
            if new_item is not None:
                data["item"] = new_item.getText()
            new_type = trade.find("span", {"class":"label label-default"})
            if new_type is not None:
                data["type"] = new_type.getText()
            new_user = trade.find("span", {"class": "username"})
            if new_user is not None:
                data["username"] = new_user.getText()
            if len(data) > 0:
                all_trades.append(data)
    return all_trades

def create_properties(trade):
    pass

def property_definer(trade_item):
    properties = trade_item.split()

    pass

if __name__== "__main__":

    trades = update_trades(r)
    clean_trades = format_trades(trades)
    for trade in clean_trades:
        with open("property_dict", "a") as f:
            f.write(trade["item"]+"\n")

    #while 1:
    #    trades = update_trades(r)
    #    x = format_trades(trades)
    #    print(x)
    #    print(len(x))
    #    time.sleep(5)