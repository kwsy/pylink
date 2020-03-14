from pymongo import MongoClient

client = MongoClient(host='101.201.225.172', port=27019)
db = client.kwsy_db  # client['kwsy_db']        # 数据库的名字
collection = db.test  # db['test']              # collection的名字

collection.insert({'name': 'python'})