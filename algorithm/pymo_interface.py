import pandas as pd

def get_data(pymo_re):
    result = []
    for i in pymo_re:
        i.pop("_id")
        result.append(i)
    return result

def get_data_df(pymo_re):
    result = []
    for i in pymo_re:
        result.append(i)
    result = pd.DataFrame(result)
    return result.drop("_id",axis=1)

# import pymongo as pymo
# import datetime
# client = pymo.MongoClient('mongodb://localhost:27017/')
# db = client['stock']
# now_time = datetime.datetime.now().strftime('%Y-%m-%d')
# have_data = db['daily'].find_one({"date":now_time})
# print(have_data is None)
# pd.DataFrame().to_dict(orient="records")