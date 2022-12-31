import math
import requests
import pandas as pd
from .models import NseDataCoi
from api.VolumeRocker.models import VolumeRocker
import os
from twilio.rest import Client

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
date = raw_data["records"]["expiryDates"][0]


def AddData(Strike_Price_List_Front, PE):
    PE = "PE" if PE == "PE" else "CE"
    for i in Strike_Price_List_Front:
        for j in records:
            if PE in j:
                if i == int(j["strikePrice"]) and j["expiryDate"] == str(date):
                    print(str(j["strikePrice"])+" "+str(j["expiryDate"])+" "+str(j[PE]["changeinOpenInterest"])+" " +
                          str(j[PE]["changeinOpenInterest"])
                          )
                    NSE_DATA_MODEL = NseDataCoi.objects.all().create(
                        strikePrice=int(j[PE]["strikePrice"]),
                        underlying=j[PE]["underlying"],
                        changeinOpenInterestPE=j[PE]["changeinOpenInterest"],
                        changeinOpenInterestCE=j["CE"]["changeinOpenInterest"] if j["CE"] else 0,
                        Diffrence=j[PE]["changeinOpenInterest"] -
                        j["CE"]["changeinOpenInterest"],
                        SpotPrice=round(round(Spot_Value, -2))
                    )
                    NSE_DATA_MODEL.save()


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


def GetAtmStrikesData():
    Spot_Price = round(round(Spot_Value, -2))
    Strike_Price_Front = round(round(Spot_Value, -2))
    Strike_Price_Back = round(round(Spot_Value, -2))
    Strike_Prices = []
    Strike_Prices.append(Spot_Price)
    for i in range(10):
        Strike_Price_Back = Strike_Price_Back-100
        Strike_Prices.append(Strike_Price_Back)
        Strike_Price_Front = Strike_Price_Front + 100
        Strike_Prices.append(Strike_Price_Front)
    return Strike_Prices


def getData():
    # Get the Values
    AddData(GetAtmStrikesData(), "PE")


def RefrestData():
    print("hrerereerere")
    NseDataCoi.objects.all().delete()
    AddData(GetAtmStrikesData(), "PE")


def VolumeRockerData(Strike_Price_List_Front, PE):
    for StrikePrice in NseDataCoi.objects.all():
        PE = "PE" if PE == "PE" else "CE"
        for i in Strike_Price_List_Front:
            for j in records:
                if PE in j:
                    if i == int(j["strikePrice"]) and j["expiryDate"] == str(date) and int(j["strikePrice"]) == int(StrikePrice.strikePrice):
                        print(str(j["strikePrice"]) +
                              f" - { int(StrikePrice.strikePrice)}")
                        COIPE = (
                            (int(j[PE]["changeinOpenInterest"]))) - int(StrikePrice.changeinOpenInterestPE)
                        COICE = ((int(j["CE"]["changeinOpenInterest"])) -
                                 int(StrikePrice.changeinOpenInterestCE))
                        print(COIPE)
                        if COIPE > 20000 or COICE > 20000 or COIPE < -10000 or COICE < -10000:
                            print(f"{COIPE}"+f"-{COICE}")
                            coiP = COIPE if COIPE > 20000 else COIPE
                            coiN = COIPE if COIPE < -20000 else COICE
                            VolumeRockerModel = VolumeRocker.objects.all().create(
                                strikePrice=int(j[PE]["strikePrice"]),
                                underlying=j[PE]["underlying"],
                                changeinOpenInterestPE=j[PE]["changeinOpenInterest"],
                                changeinOpenInterestCE=j["CE"]["changeinOpenInterest"] if j["CE"] else 0,
                                Diffrence=j[PE]["changeinOpenInterest"] -
                                j["CE"]["changeinOpenInterest"],
                                Diffrence15Min=coiP if coiP > 20000 else coiN,
                                oldCE=StrikePrice.changeinOpenInterestCE,
                                oldPE=StrikePrice.changeinOpenInterestPE,
                                SpotPrice=round(round(Spot_Value, -2))
                            )
                            VolumeRockerModel.save()
                            if COIPE > 20000:
                                CurrentValuePe = int(
                                    j[PE]["changeinOpenInterest"])
                                message = f"{StrikePrice.strikePrice}PE has been incresed by {COIPE} and the current Value is {CurrentValuePe}"
                                SendWhatsAPPMEssage(message)
                            elif COICE > 20000:
                                CurrentValueCe = int(
                                    j["CE"]["changeinOpenInterest"])
                                message = f"{StrikePrice.strikePrice}PE has been incresed by {COICE} and the current Value is {CurrentValueCe}"
                                SendWhatsAPPMEssage(message)
                            elif COIPE < -10000:
                                CurrentValuePe = int(
                                    j[PE]["changeinOpenInterest"])
                                message = f"{StrikePrice.strikePrice}PE has been decresed by {COIPE} and the current Value is {CurrentValuePe}"
                                SendWhatsAPPMEssage(message)
                            else:
                                CurrentValueCe = int(
                                    j["CE"]["changeinOpenInterest"])
                                message = f"{StrikePrice.strikePrice}PE has been decresed by {COICE} and the current Value is {CurrentValueCe}"
                                SendWhatsAPPMEssage(message)


def refrestVolumeRockerData():
    print("hrerereerere")
    # VolumeRocker.objects.all().delete()
    VolumeRockerData(GetAtmStrikesData(), "PE")


def SendWhatsAPPMEssage(message):
    account_sid = "AC28e6d3517bb08c4b2608950d920555a7"
    auth_token = "e044ce94818739a7a03b61a3e09f81e0"
    client = Client(account_sid, auth_token)
    print("Heyyyyy")
    message = client.messages.create(
        body=message,
        from_="+15072644925",
        to="+919182285342"
    )


SendWhatsAPPMEssage("heyyyy")
