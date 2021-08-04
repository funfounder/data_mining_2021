from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['users2907']

persons = db.persons
# try:
#     persons.insert_one({
#                         "_id": 65498135181651,
#                        "author": "Peter2",
#                        "age": 56,
#                        "text": "is cool! Wildberry",
#                        "tags": ['cool', 'hot', 'ice'],
#                        "date": '14.06.1983'})
# except:
#     pass


# persons.insert_many([{"author": "John",
#                "age" : 29,
#                "text": "Too bad! Strawberry",
#                "tags": ['ice'],
#                "date": '04.08.1971'},
#                     {"author": "Anna",
#                "age" : 36,
#                "title": "Hot Cool!!!",
#                "text": "easy too!",
#                "date": '26.01.1995'},
#                    {"author": "Jane",
#                "age" : 43,
#                "title": "Nice book",
#                "text": "Pretty text not long",
#                "date": '08.08.1975',
#                "tags":['fantastic','criminal']}
#       ])


# for doc in persons.find({'author': 'Peter2', 'age': 55}):
#     pprint(doc)

# for doc in persons.find({'$or': [{'author': 'Peter2'},
#                                  {'age': 29}
#                                  ]
#                          }):
#     pprint(doc)


# for doc in persons.find({'age': {'$gt': 30}}):
#      pprint(doc)

#
# for doc in persons.find({'age': {'$gt': 30}}, {'author': 1, 'age': 1, '_id': 0}).limit(3):
#      pprint(doc)


# pprint(list(persons.find({'age': {'$gt': 30}}))[-1])

# for doc in persons.find({}).sort('age', -1):
#     pprint(doc)

# persons.update_one({'author': 'Peter2'}, {'$set': {'age': 46}})
# persons.update_many({'author': 'Peter2'}, {'$set': {'age': 46}})

# doc = {
#     "author": "Petya",
#                "age" : 28,
#                "text": "is hot!",
#                "date": '11.09.1991'}

# persons.update_one({'author': 'Peter2'}, {'$set': doc})
# persons.replace_one({'author': 'Petya'}, doc)


# persons.find(doc)
#
# persons.delete_many({})
#
# for doc in persons.find({}).sort('age', -1):
#     pprint(doc)

count = persons.count_documents({''})
print(count)