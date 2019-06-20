from pymongo import MongoClient

def pushToMongoDB(jsonEntries):
    client = MongoClient("enter mongodb client here")
    db = client.get_database('champions')
    records = db.champion_runes

    records.insert_many(jsonEntries)

def getEntriesFromFile():
    jsonEntries = []
    with open ('championRunes.txt', 'r') as file:
        for line in file:
            lineArray = line.rstrip().split('\t')
            champRunes = {
                'name': lineArray[0],
                'primary_build': lineArray[1],
                'secondary_build': lineArray[2]
            }

            jsonEntries.append(champRunes)

    pushToMongoDB(jsonEntries)

getEntriesFromFile()
