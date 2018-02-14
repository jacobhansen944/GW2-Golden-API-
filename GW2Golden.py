from time import localtime
from Tkinter import *
import urllib2
import json

#globally accessable dict that will contain the item_id and item_name pairings
itemNames = {}
error_encountered=False

#attempts to open a local file that contains the names of all encountered items in a dict format
# {95: "Berserker's Reinforced Scale Boots", 96:"Rampager's Sneakthief Mask of the Citadel"}

def openItemNames():
    try:
        fileObjectItems = open("itemNames.txt", "r")
    except IOError as e:
        fileObjectItems = open("itemNames.txt", "w")
        fileObjectItems.close()
    else:
        fileObjectItems.close()
        with open("itemNames.txt", "r") as f:
            for line in f:
                splitLine = line.split(":")
                itemNames[int(splitLine[0])] = splitLine[1]

#saves the itemNames dict in case there were any additions
def saveItemNames():
    fileObjectItems = open("itemNames.txt", "w")
    for key in itemNames:
        fileObjectItems.write(str(key) + ":" + itemNames[key] + ":\n")
    fileObjectItems.close()


def getItemId(item_id, authKey):
    #checks the itemNames dict for the id, if not found, query's api and adds it
    if item_id in itemNames:
        return itemNames[item_id]
    else:
        theUrl = "https://api.guildwars2.com/v2/items/" + str(item_id)
        print "New item found! accessing:"
        #print theUrl
        req = urllib2.Request(theUrl)
        request = urllib2.urlopen(req)
        json_parsed = json.loads(request.read())
        itemNames[item_id] = json_parsed['name']
        return itemNames[item_id]


def apiQuery( authKey, timing, buySell ):
    theUrl = "https://api.guildwars2.com/v2/commerce/transactions/"
    status = "good"
    page = 0
    nowTime = localtime()
    filename = ""

    if timing == "history":
        theUrl += timing
        filename = "history_"
    elif timing == "current":
        theUrl += timing
        filename = "current_"
    else:
        return "Bad Input"

    if buySell == "buys":
        theUrl += "/" + buySell + "?"
        filename += "buys_"
    elif buySell == "sells":
        theUrl += "/" + buySell +"?"
        filename += "sells_"
    else:
        return "Bad Input"

    # month-day-time
    formattedTime = str(nowTime[1]) + "-" + str(nowTime[2]) + "-" + str(nowTime[3])
    if nowTime[4] < 10:
        formattedTime += "0" + str(nowTime[4])
    else:
        formattedTime += str(nowTime[4])

    fileObjectWrite = open(filename + formattedTime + ".csv", "w")
    fileObjectWrite.write("item,price,quantity,price/unit,created")
    if timing == "history":
        fileObjectWrite.write(",purchased\n")
    else:
        fileObjectWrite.write("\n")


    while True:
        #do something
        currentUrl = theUrl + "page_size=200&page=" + str(page) + "&access_token=" + authKey
        #print currentUrl
        req = urllib2.Request(currentUrl)
        try:
            urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            status = e.reason
            error_encountered=True
        else:
            request = urllib2.urlopen(req)
            json_parsed = json.loads(request.read())

            if timing == "current":
                for i in range(0, len(json_parsed)):
                    fileObjectWrite.write(getItemId(json_parsed[i]['item_id'], authKey) + "," + str(json_parsed[i]["price"]) + "," +
                                          str(json_parsed[i]["quantity"]) + "," +
                                          str(json_parsed[i]["price"]/json_parsed[i]["quantity"]) + "," +
                                          json_parsed[i]["created"] + "\n")

            else:
                for i in range(0, len(json_parsed)):
                    fileObjectWrite.write(getItemId(json_parsed[i]['item_id'], authKey) + "," + str(json_parsed[i]["price"]) + "," +
                                          str(json_parsed[i]["quantity"]) + "," +
                                          str(json_parsed[i]["price"]/json_parsed[i]["quantity"]) + "," +
                                          json_parsed[i]["created"] + "," + json_parsed[i]["purchased"] + "\n")

            page += 1

        if status != "good":
            break

    fileObjectWrite.close()



class Application(Frame):
    """The actual GUI interface for using this program"""
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()


    def create_widgets(self):
        Label(self, text="Copy/Paste the API key (Generated per account at https://account.arena.net/applications").grid(row=0, column=0, sticky=W)
        self.textbox = Entry(self, width=80)
        self.textbox.grid(row=1, column=0, sticky=W)
        Label(self, text="Select which trade records you wish to download (history is limited to 3 months old)").grid(row=2, column=0, sticky=W)
        self.bought=BooleanVar()
        Checkbutton(self, text="History: Bought", variable=self.bought).grid(row=3, column=0, sticky=W)
        self.sold=BooleanVar()
        Checkbutton(self, text="History: Sold", variable=self.sold).grid(row=4, column=0, sticky=W)
        self.buying=BooleanVar()
        Checkbutton(self, text="Present: Buying", variable=self.buying).grid(row=5, column=0, sticky=W)
        self.selling=BooleanVar()
        Checkbutton(self, text="Present: Selling", variable=self.selling).grid(row=6, column=0, sticky=W)
        self.submit_button=Button(self, text="Get trades!", command=self.call_trades).grid(row=7, column=0, sticky=W)

    def call_trades(self):
        apiKey=self.textbox.get()
        if self.sold.get():
            apiQuery(apiKey, "history", "sells")
        if self.bought.get():
            apiQuery(apiKey, "history", "buys")
        if self.selling.get():
            apiQuery(apiKey, "current", "sells")
        if self.buying.get():
            apiQuery(apiKey, "current", "buys")
        self.master.destroy()



openItemNames()

root = Tk()
root.title("GW2 Golden")
root.geometry("500x300")
app=Application(root)
root.mainloop()




saveItemNames()
