from flask import Flask 
from flask_mysqldb import MySQL 
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo



app = Flask(__name__)

app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_HOST'] = 'database-2.cdvgrxwqeeka.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DB'] = 'movies'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
CORS(app)

@app.route("/list/", methods=['GET'])
def test():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM movies''')
    results = cur.fetchall()
    # print(results)
    return {"data":[x for x in results]}

@app.route('/search')
def serach():
    name = request.args.get('name', None)
    print(name)

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

mongo = PyMongo(app)

@app.route("/mongo/list")
def mongo_list():
    result = mongo.db.streamingServices.find()
    return {"data": list(result)}

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
    
    result = mongo.db.streamingServices.find({"title": name})
    
    return {"data": list(result)}


@app.route('/mongo/delete', methods=['POST', 'GET'])
def mongo_delete():
    name = request.args.get('name', None)
    platform = request.args.get('platform', "None")
   
    mongo.db.streamingServices.remove({"title": name, "platform": platform}, True)

    return "deleted {} on {}".format(name, platform)
