#from pymongo import MongoClient

#client = MongoClient('localhost', 27017)
#db = client.pymongo_test

#posts = db.posts

#result = posts.insert_one({
#        "address": {
#            "street": "2 Avenue",
#            "zipcode": "10075",
#            "building": "1480",
#            "coord": [-73.9557413, 40.7720266]
#        },
#        "borough": "Manhattan",
#        "cuisine": "Italian",
#        "grades": [
#            {
#                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
#                "grade": "A",
#                "score": 11
#            },
#            {
#                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
#                "grade": "B",
#                "score": 17
#            }
#        ],
#        "name": "Vella",
#        "restaurant_id": "41704620"
#    }
#)

#posts.drop()
#posts.delete_many({})

#print('One post: {0}'.format(result.inserted_id))
#bills_post = posts.find_one({'borough':'Manhattan'})
#print(bills_post)