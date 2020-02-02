import airbnb
from pprint import pprint
from statistics import median
import time
from concurrent import futures
import json

class AirBnBFinder:
    def __init__(self):
        self.api = airbnb.Api(randomize=True)

    def findCheapest(self, city, start, end):
        """
        city: "City, State" or "City, Country"\n
        start and end: "yyyy-mm-dd"
        """
        def getContainer(info):
            canHaveListings = info["explore_tabs"][0]["sections"]
            for section in canHaveListings:
                if "listings" in section.keys():
                    index = canHaveListings.index(section)
                    break
            return canHaveListings[index]["listings"]

        def getPrices(rateContainList):
            return [{"price":unit["pricing_quote"]["price"]["total"]["amount"],"id":unit["listing"]["id"]} for unit in rateContainList]

        looked = []
        i = 0
        # info = self.api.get_homes(city, items_per_grid=306, offset=i,checkin=start,checkout=end)
        
        info = json.load(open("/Users/curtthedirt/Desktop/Code/CABL/info.json", 'r'))

        rateContainList = getContainer(info)
        prices = getPrices(rateContainList)

        # while prices not in looked:
        #     looked.append(prices)
        #     i += len(looked[-1])
        #     info = self.api.get_homes(city, items_per_grid=306, offset=i,checkin=start,checkout=end)
        #     rateContainList = getContainer(info)
        #     prices = getPrices(rateContainList)

        # looked[-1] = looked[-1][len(sum(looked, []))-306:]
        # fullPrices = sum(looked, [])
        fullPrices = prices
        fullPrices.sort(key=lambda x:x["price"])
        return {"prices":fullPrices, "dates":f"{start}:{end}"}

    def findBest(self,listOfPrices):
        if len(listOfPrices) == 1:
            return listOfPrices
        
        meds = {i["dates"]:(median([p["price"] for p in i["prices"]])) for i in listOfPrices}
        lowestMed = min(meds.values())
        bestDates = [i[0] for i in meds.items() if i[1] == lowestMed]
        return [opt for opt in listOfPrices if opt["dates"] in bestDates]


if __name__=="__main__":
    t = time.perf_counter()
    prices = []
    finder = AirBnBFinder()

    def exe(start, end):
        prices.append(finder.findCheapest("Tampa, Florida", start, end))

    starts = [f"2020-04-{i}" for i in range(10,21)]
    ends = [f"2020-04-{i}" for i in range(20,31)]

    # for start, end, i in zip(starts,ends, range(len(starts))):
    #     exe(start, end)
    #     print(i)
    
    info = finder.findCheapest("Tampa, Florida", starts[0], ends[0])

    print(info)

    with open("info2.json", 'w') as j:
        js = json.dumps(info, indent=2)
        j.write(js)

    # with futures.ThreadPoolExecutor() as executor:
    #     res = executor.map(exe, starts, ends)
    #     futures.wait(res)

    # print(finder.findBest(prices))
    print(f"{time.perf_counter()-t} Seconds")