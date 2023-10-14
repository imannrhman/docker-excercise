import time
import random
import requests
import json
import re
from sqlalchemy import text
from sqlalchemy import create_engine


db_name = 'dibimbing'
db_user = 'dibimbing-user'
db_pass = 'dibimbing.id'
db_host = 'database'
db_port = '5432'


def clean_string(string):
    tmp = re.sub(r'\&\w*;', '', string)
    tmp = re.sub(r'@(\w+)', '', tmp)
    tmp = re.sub(r'(http|https|ftp)://[a-zA-Z0-9\\./]+', '', tmp)
    tmp = re.sub(r'#(\w+)', '', tmp)
    tmp = re.sub(r'(.)\1{1,}', r'\1\1', tmp)
    tmp = re.sub("[^a-zA-Z]", " ", tmp)
    tmp = re.sub(r'\b\w{1,2}\b', '', tmp)
    tmp = re.sub(r'\s\s+', ' ', tmp)
    return tmp 
        
try:

    db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
    engine = create_engine(db_string)
    db = engine.connect()
    print("<======> CONNECTED <======>")

    print("<======> Fetch Data From API <======>")
    url = "https://api-berita-indonesia.vercel.app/cnn/terbaru"

    response = requests.get(url)
    print("<======> Success ! <======>")

    print("<======> Response <======>")
    print (json.dumps(response.json(), indent=4, sort_keys=True))
    print("<========================>")
    
    query = 'CREATE TABLE IF NOT EXISTS news (' +\
    'id SERIAL PRIMARY KEY,' +\
     'title VARCHAR(200),' +\
     'description TEXT,' +\
     'thumbnail TEXT,' +\
     'link TEXT,' +\
     'source VARCHAR(50),' +\
     'publish_date DATE,' +\
     'timestamps BIGINT);' 
    
    db.execute(text(query))


    for data in response.json()['data']['posts']:
        query = "INSERT INTO news (title, description, thumbnail, link, source, publish_date, timestamps)" +\
                     " VALUES ('" +\
                    clean_string(data['title']) + "', '" +\
                    clean_string( data['description']) + "', '" +\
                    data['thumbnail'] + "', '" +\
                    data['link'] + "', '" +\
                    "CNN Indonesia', '" +\
                    data['pubDate'] + "', " +\
                    str(int(round(time.time() * 1000))) + ");"
        db.execute(text(query))

except Exception as e:
     print("The error is: ", e)



