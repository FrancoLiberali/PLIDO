from pymongo import MongoClient

client = MongoClient()
db = client["meteo-data"]
measure = db.measure

sensor_location = "Room 122"

found_item = measure.find_one ({"Location" : sensor_location })
if found_item == None:
    raise ValueError ("{} not found".format(sensor_location))
else:
    sensor_id = found_item["_id"]

print (sensor_id)

res = measure.aggregate([
    {"$match" : {"SensorCharacteristics" : sensor_id }},
    {"$group" : {
        "_id": None, # equivalent to null in MongoDB
        "count": {"$sum": 1},
        "temp_min": {"$min": "$Temperature"},
        "temp_max": {"$max": "$Temperature"}
        }
    }
])

print (res)

for r in res:
    print (r)