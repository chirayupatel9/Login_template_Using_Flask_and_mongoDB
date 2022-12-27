import pymongo

# DB connection config
username = "admin"
password = " "

# DB URL formed in URI
URI = "mongodb+srv://" + username + ":" + password + "@cluster0.gnwyvcr.mongodb.net/?retryWrites=true&w=majority"

# DB Connect
client = pymongo.MongoClient(URI)

# DB Connect Collection and Table
db = client.get_database('total_records')
records = db.register
