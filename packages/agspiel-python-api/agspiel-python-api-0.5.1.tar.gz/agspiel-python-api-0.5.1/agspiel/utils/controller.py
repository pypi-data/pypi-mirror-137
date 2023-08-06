#  Copyright (c) 2021 | KingKevin23 (@kingkevin023)

from decimal import Decimal
from requests import post, get
from datetime import datetime
from re import search

from bs4 import BeautifulSoup

from agspiel.utils.errors import OrderCreationException, OrderDeletionException, OrderException

class Controller:
    def __init__(self, phpsessid:str):
        self._phpsessid = phpsessid
        soup = BeautifulSoup(get("https://www.ag-spiel.de/index.php?section=agorderbuch",
                                 cookies={"PHPSESSID": self._phpsessid}).content, "html.parser")
        self._token = soup.find("input", attrs={"type":"hidden", "name":"token"}).get("value")

    def create_order(self, wkn:int, buy:bool, limit:float, anzahl:int, tage_gueltig:float=14.00, gueltig_ab:datetime=datetime.now(), **kwargs) -> int:
        orderwert = str(Decimal(str(limit)) * anzahl)
        body = {
            "privat": 0,
            "aktie": wkn,
            "limit": limit,
            "anzahl": anzahl,
            "orderwert": orderwert,
            "gab_tag": gueltig_ab.day,
            "gab_monat": gueltig_ab.month,
            "gab_jahr": gueltig_ab.year,
            "gab_stunde": gueltig_ab.hour,
            "gab_minute": gueltig_ab.minute,
            "gueltigkeit": tage_gueltig,
            "token": self._token
        }

        if buy:
            body["order"] = "buy"
        else:
            body["order"] = "sell"

        if "aenderung" in kwargs:
            body["aenderung"] = kwargs.get("aenderung")
            body["aendern"] = 1
            if "stop" in kwargs:
                body["aenderung_stop"] = kwargs.get("stop")
                body["aendern2"] = 1
            else:
                body["aenderung_stop"] = limit
        else:
            body["aenderung"] = 0.0005

        response = post("https://www.ag-spiel.de/index.php?section=agorderbuch&action=create&ele=", body, cookies={"PHPSESSID": self._phpsessid})
        soup = BeautifulSoup(response.content, "html.parser")
        result = self._get_infobox_text(soup)

        if result != "Ordererstellung beauftragt.":
            raise OrderCreationException(result)

        cross = soup.find("a", attrs={"class": "button cross notext", "title": "Order löschen/bearbeiten"},
                          href=lambda x: f"&action=delete&aktie={wkn}&limit={'%.2f' % limit}&anzahl={anzahl}" in x)
        orderid = search("index\.php\?section=agorderbuch&orderid=(\d*)&", cross.get("href"))
        if not orderid:
            raise OrderException("Order wurde erstellt, jedoch wurde die OrderID nicht gefunden.")

        return int(orderid.group(1))


    def delete_order(self, orderid:int) -> bool:
        # Get link by orderid is not needed cause we only need the orderid
        # soup = BeautifulSoup(get("https://www.ag-spiel.de/index.php?section=agorderbuch",
        #                          cookies={"PHPSESSID": self._phpsessid}).content, "html.parser")
        # cross = soup.find("a", attrs={"class":"button cross notext", "title":"Order löschen/bearbeiten"}, href=lambda x: f"index.php?section=agorderbuch&orderid={orderid}&action=delete&aktie=" in x)
        # link = "https://www.ag-spiel.de/" + cross.get("href")
        response = get(f"https://www.ag-spiel.de/index.php?section=agorderbuch&orderid={orderid}&action=delete", cookies={"PHPSESSID": self._phpsessid})
        result = self._get_infobox_text(BeautifulSoup(response.content, "html.parser"))
        if result != "Order wurde gelöscht.":
            raise OrderDeletionException(result)

        return True

    @classmethod
    def _get_infobox_text(cls, soup:BeautifulSoup) -> str:
        infobox = soup.find("div", attrs={"class": "infobox"})
        result = str()
        for child in infobox.children:
            if child.name is None:
                if result != "":
                    result += " "

                result += child.strip()

        return result