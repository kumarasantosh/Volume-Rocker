from .models import NSE_DATA
import math
import requests
import pandas as pd

URL = "https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
}

session = requests.Session()
r = session.get(url=URL, headers=header)
data = r.json()
raw_data = pd.DataFrame(data)
records = raw_data["records"]["data"]
Spot_Value = records[0]["CE"]["underlyingValue"]


def AddData(Strike_Price_List_Front, PE):
    one = "PE" if PE == "PE" else "CE"
    for i in Strike_Price_List_Front:
        for j in records:
            if PE in j:
                if i == int(j["strikePrice"]) and j["expiryDate"] == "05-Jan-2023":
                    print(int(j[PE]["strikePrice"]))
                    NSE_DATA_MODEL = NSE_DATA.objects.create(
                        name=one, underlying=j[PE]["underlying"] if "underlying" in j[PE] else 0,
                        strikePrice=int(j[PE]["strikePrice"]),
                        # expiryDate=j[PE]["expiryDate"]
                        openInterest=j[PE]["openInterest"] if "openInterest" in j[PE] else 0,
                        changeinOpenInterest=j[PE]["changeinOpenInterest"] if "changeinOpenInterest" in j[PE] else 0,
                        totalTradedVolume=j[PE]["totalTradedVolume"] if "totalTradedVolume" in j[PE] else 0,
                        underlyingValue=j[PE]["underlyingValue"] if "underlyingValue" in j[PE] else 0,
                    )
                    NSE_DATA_MODEL.save()


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


def GetAtmStrikesData():
    Spot_Price = roundup(Spot_Value)
    Strike_Price_Front = roundup(Spot_Value)
    Strike_Price_Back = roundup(Spot_Value)
    Strike_Prices = []
    Strike_Prices.append(Spot_Price)
    for i in range(10):
        Strike_Price_Back = Strike_Price_Back-100
        Strike_Prices.append(Strike_Price_Back)
        Strike_Price_Front = Strike_Price_Front + 100
        Strike_Prices.append(Strike_Price_Front)
    print(Strike_Prices)
    return Strike_Prices


def getData():
    # Get the Values
    AddData(GetAtmStrikesData(), "PE")
    AddData(GetAtmStrikesData(), "CE")


def RefrestData():
    NSE_DATA.objects.all().delete()
    AddData(GetAtmStrikesData(), "PE")
    AddData(GetAtmStrikesData(), "CE")
