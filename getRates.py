import datetime

from variables.fastApiModules import *
from variables.mongoDbConnection import *


class GoldSilverRatesByDate(BaseModel):
    date_in_YYYY_MM_DD: str


@app.get("/goldSliver/getAllRates")
def getAllRates():
    rates = list(goldCollection.find({}, {"_id": 0}))
    responseObject = {"goldSilverRates": rates}

    return responseObject


@app.get("/Silver/getSilverRates")
def getSilverRates():
    rates = list(goldCollection.find({}, {"_id": 0, "Silver": 1, "dateTime": 1}))
    responseObject = {"SilverRates": rates}

    return responseObject


@app.post("/getGoldSilverRatesByDate")
def getGoldSilverRatesByDate(jsonReq: GoldSilverRatesByDate):
    """
    This is an API to fetch the gold and silver rates based on the date passed
    :param jsonReq:
    :return: returns the dateTime, Gold rate, silver rate - example -
    {'dateTime': datetime.datetime(2022, 11, 28, 15, 45, 39, 213000), 'Gold 22K': 4860.0, 'Silver': 65.0}
    """
    cursor = goldCollection.find_one({"dateTime":
                                     {"$gte": datetime.strptime(jsonReq.date_in_YYYY_MM_DD, '%Y-%m-%d')}}, {"_id": 0})
    for rates in [cursor]:
        responseObject = {"Rates for Requested date": rates}

        return responseObject
