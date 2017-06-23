import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds127842.mlab.com:27842/supervehacker
host = "ds127842.mlab.com"
port = 27842
db_name = "supervehacker"
user_name = "admin"
password = "admin"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())