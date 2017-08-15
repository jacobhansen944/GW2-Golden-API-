from time import localtime

print "Hello World"


# what would this GW2 APi actually need to do?
#
# query server for trades, print results to a .txt or .csv document
# filter results by time, by item, by flipping value
# basic interface
# saves the key in a .txt file so that it can be loaded from memory, not entered every run
# output file will be titled by the day and time, like trades8-22-830pm
#
#
#
#


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

nowTime = localtime()

print nowTime

# month-day-time
formattedTime = str(nowTime[1]) + "-" + str(nowTime[2]) + "-" + str(nowTime[3]) + str(nowTime[4])

print formattedTime

fileObjectWrite = open(formattedTime, "w")

fileObjectWrite.write(formattedTime)

fileObjectWrite.close()

# write a filename containing the current timestamp