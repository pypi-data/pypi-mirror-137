import pymongo
import aiohttp


def show_collection() -> list:
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    database = db['miagobot']
    c = database.collection_names()
    return c


def rank(file: str) -> list:
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    database = db['miagobot']

    find_x = database[file].find().sort('count', -1)
    return find_x


def othersRank(file: str, key: str) -> list:
    database = pymongo.MongoClient("mongodb://localhost:27017")["miagobot_others"]
    sortItem = database[file].find().sort(key, -1)
    return sortItem


def server_link(file: str):
    """
    连接MongoDB数据库，
    自定义操作类型
    """
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    database = db["miagobot"]
    form = database[file]
    return form


def others_server_link(file: str):
    """
    连接到非物品数据库
    自定义操作类型
    """
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    database = db["miagobot_others"]
    form = database[file]
    return form


def read_doc(file, uid):
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = db["miagobot"]
    file_form = mydb[str(file)]
    data = file_form.find_one({"user_id": str(uid).strip()})['count']
    return data


def write_doc_add(file, uid, count):
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = db["miagobot"]
    form = mydb[str(file)]
    form.update_one({"user_id": str(uid)}, {"$inc": {"count": int(count)}})


def other_update(file: str, uid: str, ways: str, field: str, new: [str, int]):
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = db["miagobot_others"]
    form = mydb[file]
    form.update_one({"user_id": uid}, {ways: {field: new}})


def write_doc_subtract(file, uid, count):
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = db["miagobot"]
    form = mydb[str(file)]
    form.update_one({"user_id": str(uid)}, {"$inc": {"count": -int(count)}})


def buy_things(item: str, price: int, count: int, uid: str, baoshi: int, cunkuan: int):
    if count <= 0:
        return "err"
    if baoshi >= price * count:  # 物品价格*物品数量
        write_doc_subtract("宝石", uid, count * price)
        write_doc_add(item, uid, count)
        return 1
    elif baoshi < price * count + price * count * 0.1 <= cunkuan:  # 物品价格*物品数量+物品价格*物品数量*10%的手续费
        write_doc_subtract("存款", uid, price * count + price * count * 0.1)
        write_doc_add(item, uid, count)
        return 2
    else:
        return False


def set_file_count(file, uid, count):
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = db["miagobot"]
    form = mydb[str(file)]
    form.update_one({"user_id": str(uid)}, {"$set": {"count": int(count)}})


async def saveimg_session(url):
    async with aiohttp.ClientSession() as aio:
        async with aio.get(url) as get:
            save = await get.content.read()
            return save


async def savejson_session(url):
    async with aiohttp.ClientSession() as aio:
        async with aio.get(url) as get:
            save = await get.text()
            return save
