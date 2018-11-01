import pandas as pd
from algorithm.item import MapItem
import json
import datetime
from algorithm import pymo_interface as mogoIn
import tushare as ts

def gain_data(db, indus = None):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')

    have_data = db['daily'].find_one({"date":now_time})
    if have_data is None:
        daily = ts.get_today_all()
        category = ts.get_stock_basics()

        daily['date'] = now_time
        category['date'] = now_time
        category['code'] = category.index

        db['daily'].insert_many(daily.to_dict(orient="records"))
        db['category'].insert_many(category.to_dict(orient="records"))
    else:
        daily = mogoIn.get_data_df(db['daily'].find({"date":now_time}))
        category = mogoIn.get_data_df(db['category'].find({"date":now_time}))

    if indus is not None:
        category = category[category["industry"] == indus]
    return daily, category


def gain_pic(daily, category):
    # daily = pd.read_excel("daily.xlsx", )
    # category = pd.read_excel("category.xlsx")

    # gain industry and clean data
    category = category[['code', 'industry']]
    daily = pd.merge(daily, category, on='code', how='right')
    daily = daily.dropna()

    # gain market
    market_code = {
        "60": "上证",
        "30": "创业",
        "00": "深圳",
    }
    daily["market"] = daily['code'].apply(lambda x: market_code[x[:2]])
    market = daily[['market', 'mktcap']].groupby('market').agg({"mktcap": sum})
    market["rate"] = market["mktcap"] / market["mktcap"].sum()
    market["name"] = market.index
    daily["market_mktcap"] = daily['market'].apply(lambda x: market['mktcap'][x])

    # gain industry rate
    industry = daily[['industry', 'mktcap', 'market']].groupby(['industry', 'market'], as_index=False).agg(
        {"mktcap": sum})
    industry["rate"] = industry["mktcap"] / industry["mktcap"].sum()
    industry['industry_mktcap'] = industry['mktcap']
    industry['name'] = industry['market'] + "|" + industry['industry']
    daily = pd.merge(daily, industry[['industry', 'market', 'industry_mktcap']], on=['industry', 'market'])
    daily['rate'] = daily['mktcap'] / daily['industry_mktcap']
    daily['market' + "|" + 'industry'] = daily['market'] + "|" + daily['industry']

    # gain total
    total_cap = daily['mktcap'].sum()
    total_cap_rate = daily['changepercent'] * (daily['mktcap'] / total_cap)
    total_cap_rate = sum(total_cap_rate.dropna())
    total_item = MapItem({
        "name": "全市场",
        "id": "全市场",
        "rate": 1,
        "changepercent": total_cap_rate,
    }, type_is='t')

    # gain rate for daily
    def gain_change_rate(daily_is, type_is):
        col = "market"
        if type_is == "market|industry":
            col = "industry"
        inter = daily_is[[type_is]].copy()
        inter['sum_is'] = daily_is['changepercent'] * (daily_is['mktcap'] / daily_is[col + "_mktcap"])
        inter = inter[[type_is, 'sum_is']].groupby([type_is]).agg({"sum_is": sum})
        inter = inter.rename(columns={"sum_is": "changepercent"})
        return inter

    market_rate = gain_change_rate(daily, "market")
    industry_rate = gain_change_rate(daily, "market|industry")
    market["changepercent"] = market["name"].apply(lambda x: market_rate['changepercent'][x])
    industry["changepercent"] = industry["name"].apply(lambda x: industry_rate['changepercent'][x])

    # gain all item, I'm lazy for writing a recursion
    daily_item = []
    for i in range(len(daily)):
        inter_row = daily.iloc[i]

        daily_item.append({
            "item": MapItem(inter_row),
            "market": inter_row['market'],
            "industry": inter_row['industry'],
        })
    daily_item = pd.DataFrame(daily_item)

    industry_item = []
    for i in range(len(industry)):
        inter_row = industry.iloc[i]
        inter_item = MapItem(inter_row, type_is='i')
        inter_daily_item = daily_item[(daily_item["market"] == inter_row['market']) &
                                      (daily_item["industry"] == inter_row['industry'])]

        for j in range(len(inter_daily_item)):
            inter_item.add_child(inter_daily_item["item"].iloc[j])

        industry_item.append({
            "item": inter_item,
            "market": inter_row['market'],
        })
    industry_item = pd.DataFrame(industry_item)

    for i in range(len(market)):
        inter_row = market.iloc[i]
        inter_item = MapItem(inter_row, type_is='m')
        inter_industry_item = industry_item[(industry_item["market"] == inter_row['name'])]

        for j in range(len(inter_industry_item)):
            inter_item.add_child(inter_industry_item["item"].iloc[j])

        total_item.add_child(inter_item)

    return json.dumps([total_item.return_json()])



# data = ts.get_today_all()
# category = ts.get_stock_basics()
# category['code'] = category.index

# data['code'] = data['code'] + "i"
# data.to_excel("daily.xlsx")
# category['code'] = category.index + "i"
# category.to_excel("category.xlsx")

# print(daily.head(100))
# print(total_cap_rate)
# print(total_cap)


# industry = daily[['industry', 'mktcap']].groupby(['industry']).agg({"mktcap": sum})
# industry["rate"] = industry["mktcap"] / industry["mktcap"].sum()
# daily = daily['industry'].apply(lambda x: industry['mktcap'][x])
#     daily.to_excel("daily_%s.xlsx" %str(now_time))
#     category.to_excel("category%s.xlsx" %str(now_time))