from time import localtime
import urllib
import urllib2
import json

#globally accessable dict that will contain the item_id and item_name pairings
itemNames = {}

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
        print "New item found accessing:"
        print theUrl
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
        currentUrl = theUrl + "page_size=200&page=" + str(page) + "&access_token=" + apiKey
        print currentUrl
        req = urllib2.Request(currentUrl)
        try:
            urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            status = e.reason
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
                                          str(json_parsed[i]["price"] / json_parsed[i]["quantity"]) + "," +
                                          json_parsed[i]["created"] + "," + json_parsed[i]["purchased"] + "\n")

            page += 1

        if status != "good":
            break

    fileObjectWrite.close()




# what would this GW2 APi actually need to do?
#
# query server for trades, print results to a .txt or .csv document
# filter results by time, by item, by flipping value
# extracts the item ID based off item name
# basic interface
# saves the key in a .txt file so that it can be loaded from memory, not entered every run
# could save the key for multiple characters/accounts and selected through the gui
# output file will be titled by the day and time, like trades8-22-830pm
#
#
#
#
openItemNames()
apiKey = "0C2436EC-41F1-6744-83D0-BBC3657770BAFDF990B1-954E-4B20-8A7C-DD423CE8E906"

apiQuery(apiKey, "history", "sells")
apiQuery(apiKey, "history", "buys")
apiQuery(apiKey, "current", "sells")
apiQuery(apiKey, "current", "buys")




saveItemNames()



#json_parsed = json.loads(fileContents)
#
#fileObjectWrite = open("OutputTest.csv", "w")
#fileObjectWrite.write("item,price,quantity,created,purchased\n")

#i = 391
#fileObjectWrite.write(getItemId(json_parsed[i]['item_id'], apiKey) + "," + str(json_parsed[i]["price"]) + "," + str(json_parsed[i]["quantity"]) + "," + json_parsed[i]["created"] + "," + json_parsed[i]["purchased"])

# for i in range(0, len(json_parsed)):
#     fileObjectWrite.write(str(json_parsed[i]['item_id']) + "," + str(json_parsed[i]["price"]) + "," + str(json_parsed[i]["quantity"]) + "," + json_parsed[i]["created"] + "," + json_parsed[i]["purchased"] + "\n")
#     print str(i)
# fileObjectWrite.close()
#
# print len(json_parsed)


#print response.read()

# fileName = raw_input("Enter the name of the file to be read: ")
#
# fileObjectRead = open(fileName, "r")
#
# fileContents = fileObjectRead.read()
#
# print fileContents
#
# fileObjectRead.close()


# fileObjectWrite = open(fileName, "w")
#
# fileObjectWrite.write(fileContents + raw_input("Now enter some text to add to the file: "))
#
# fileObjectWrite.close()





# write a filename containing the current timestamp

#nowTime = localtime()

#print nowTime

# month-day-time
#formattedTime = str(nowTime[1]) + "-" + str(nowTime[2]) + "-" + str(nowTime[3]) + str(nowTime[4])

#print formattedTime

#fileObjectWrite = open(formattedTime, "w")

#fileObjectWrite.write(formattedTime)

#fileObjectWrite.close()




