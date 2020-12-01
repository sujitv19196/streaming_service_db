from flask import Flask 
from flask_mysqldb import MySQL 
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo
import pymongo
import pandas as pd 



app = Flask(__name__)

app.config['MYSQL_DB'] = 'movies'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
db = client.database1
collection = db.streamingServices
mysql = MySQL(app)
mongo = PyMongo(app)


CORS(app)


@app.route("/list/", methods=['GET'])
def test():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM movies LIMIT 10''')
    results = cur.fetchall()
    # print(results)
    return {"data":[x for x in results]}

@app.route('/search')
def serach():
    name = request.args.get('name', None)
    # print(name)

    cur = mysql.connection.cursor()
    query = '''SELECT * FROM movies WHERE movie_title = "{}"'''.format(name) 
    cur.execute(query)
    result = cur.fetchall()
    return {"data":[x for x in result]}

@app.route('/insert')
def insert():
    params = ['name', 'year', 'genre', 'director']
    columns = ['movie_title', 'year', 'genre', 'director']
    data = [request.args.get(param, None) for param in params]
    data = ["NULL" if x is None else "'" + x + "'" for x in data]

    cur = mysql.connection.cursor()
    query = "INSERT INTO movies({}) VALUES({})".format(",".join(columns), ",".join(data))
    cur.execute(query)
    mysql.connection.commit()
    print(query)
    return "inserted: {}".format(data[0])


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    name = request.args.get('name', None)
    print(name)
    cur = mysql.connection.cursor()
    query = '''DELETE FROM movies WHERE movie_title = "{}"'''.format(name)
    cur.execute(query)
    mysql.connection.commit()

    return "deleted {}".format(name)

@app.route('/update')
def update():
    movie_id = request.args.get('id', None)
    params = ['name', 'year', 'genre', 'director']
    columns = ['movie_title', 'year', 'genre', 'director']
    data = [request.args.get(param, None) for param in params]
    data = ["NULL" if x is None else "'" + x + "'" for x in data]
    
    cur = mysql.connection.cursor()
    query = '''UPDATE movies SET {} WHERE imdb_title_id = "{}"'''.format(",".join(['{} = {}'.format(columns[i], x) for i, x in enumerate(data) if x != "NULL"]), movie_id)
    
    cur.execute(query)
    mysql.connection.commit()
    print(query)
    return "Updated id: {}".format(movie_id)

@app.route('/most_genre', methods=['POST', 'GET'])
def most_genre():
    user = request.args.get('user_id', None)
    cur = mysql.connection.cursor()
    query = "call test({})".format(user)
    cur.execute(query)
    result = cur.fetchall()
    result = result[0].values()
    return {"data":[x for x in result]}

@app.route('/movie_list', methods=['POST', 'GET'])
def movie_list():
    user = request.args.get('user_id', None)
    cur = mysql.connection.cursor()
    query = "call movie_list({})".format(user)
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    return {"data":[x for x in result]}

mongo = PyMongo(app)
@app.route("/mongo/list")
def mongo_list():
    # print("here")
    result = list(mongo.db.streamingServices.find())
    for r in result:
        del r['_id']
    return {"data": [x for x in result]}

@app.route("/mongo/insert")
def mongo_insert():
    platform = request.args.get('platform', "None")
    title = request.args.get('name', "None")
    imdb_id = request.args.get('id', "None")
    doc = {"platform": platform, "title": title, "imdb_title_id": imdb_id}
    mongo.db.streamingServices.insert_one(doc)
    return "inserted {}".format(doc)

@app.route('/mongo/search')
def mongo_serach():
    name = request.args.get('name', None)
    result = list(mongo.db.streamingServices.find({"title": name}))
    for r in result:
        del r['_id']
    return {"data": [x for x in result]}


@app.route('/mongo/delete', methods=['POST', 'GET'])
def mongo_delete():
    name = request.args.get('name', None)
    platform = request.args.get('platform', "None")
   
    mongo.db.streamingServices.remove({"title": name, "platform": platform}, True)

    return "deleted {} on {}".format(name, platform)

# @app.route("/list/", methods=['GET'])
# def test():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT * FROM movies''')
#     results = cur.fetchall()
#     # print(results)
#     return {"data":[x for x in results]}

@app.route('/platformranking')
def platform_ranking():
    user_id = request.args.get('id', None)
    print(user_id)
    cur = mysql.connection.cursor()
    query = "select movie_id, user_rating from user_ratings where user_id = {}".format(user_id)
    
    cur.execute(query)
    mysql.connection.commit()
    
    user_data = list(cur.fetchall())

    user_data = list(zip(*[list(user_data[i].values()) for i in range(len(user_data))]))
    user_data_dict = {"imdb_title_id": list(user_data[0]), "user_rating": list(user_data[1])}
    user_data_df = pd.DataFrame.from_dict(user_data_dict)
    
    platform = list(mongo.db.streamingServices.find())
    platform = list(zip(*[list(platform[i].values())[1:] for i in range(len(platform))]))
    platform_dict = {'platform': list(platform[0]), 'title': list(platform[1]), 'imdb_title_id': list(platform[2])}
    platform_df = pd.DataFrame.from_dict(platform_dict)
    final_df = user_data_df.merge(platform_df)
    
    platform_list = ["Netflix", "Prime Video", "Hulu", "Disney+"]
    result = []
    #test = []

    for p in platform_list:
        temp = final_df[final_df["platform"] == p]["user_rating"]
        avg = sum(temp)/len(temp) if len(temp) > 0 else 0
        weighted = avg + len(temp)**0.2
        result.append((p, round(weighted, 2)))
        #test.append((p, round(avg, 2)))
    result = sorted(result, key=lambda x: x[1], reverse=True)
    return {"data": result}




# f = '''
# CREATE PROCEDURE AF1(
#     in user VARCHAR(255)
# )
# BEGIN 
#     select m.mo
#     from movies m join netflix n on m.movie_title = n.movie_title, user_ratings u 
#     where user
#     select m.genre 
#     from user_ratings u join movies m on u.movie_id = m.movie_id
#     where user_id = user 
#     group by m.genre 
#     having count = (select max(count(m.genre))
#     from user_ratings u join movies m on u.movie_id = m.movie_id
#     where user_id = user
#     group by m.genre) 
# END 
# '''