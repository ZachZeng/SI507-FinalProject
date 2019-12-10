import sqlite3
import csv
import json
from sqlite3 import Error
from bs4 import BeautifulSoup
import urllib.parse
import requests

DBNAME = 'game.db'


def create_connection(db_filename):
    conn = None
    try:
        conn = sqlite3.connect(db_filename)
        return conn
    except Error as e:
        print(e)

    return conn


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_" + "_".join(res)

def get_data_with_cache(baseurl,params,filename):

    # on startup, try to load the cache from file
    try:
        cache_file = open(filename, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

    # if there was no file, no worries. There will be soon!
    except:
        CACHE_DICTION = {}

    unique_ident = params_unique_combination(baseurl,params)


    if unique_ident in CACHE_DICTION:
        #print("Fetching cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        response = requests.get(baseurl,params).text

        CACHE_DICTION[unique_ident] = json.loads(response)

        dumped_result = json.dumps(CACHE_DICTION,indent=4)

        fw = open(filename,"w")
        fw.write(dumped_result)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

def scraping_using_cache(url, filename):
    CACHE_FNAME = filename
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {} 
    unique_ident = url
    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        #print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(filename,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


        

def init_insert(conn):
    cur = conn.cursor()
    platform_baseurl = "https://api.rawg.io/api/platforms"
    params_dict = {
    }
    response = get_data_with_cache(platform_baseurl,params_dict,"platform_cache")
    results = response['results']
    for platform in results:
        for game in platform['games']:
            insertion = (None,platform['id'],platform['name'],platform['image_background'],platform['games_count'],game['id'])
            statement = 'INSERT INTO "Platforms" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?)'
            try:
                cur.execute(statement, insertion)
            except Error as e:
                print(e)
                print(statement)
            insert_game(game['id'],conn,platform['id'])
    conn.commit()

def insert_game(id,conn,platform_id):
    cur = conn.cursor()
    game_baseurl = 'https://api.rawg.io/api/games/'+str(id)
    params_dict = {
    }
    response = get_data_with_cache(game_baseurl,params_dict,"game_cache")

    game_name = response['name']

    game_desc = get_game_description(game_name)

    insertion = (None, response['id'],game_name,response['released'],response['rating'],game_desc,platform_id)
    statement = 'INSERT INTO "Games" '
    statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
    try:
        cur.execute(statement, insertion)
    except Error as e:
        print(e)
        print(statement)
    conn.commit()

def get_game_description(game_name):

    game_name = game_name.lower()

    if '(' in game_name:
        game_name = game_name[:-7]
    game_name = game_name.replace(':','')
    game_name = game_name.replace("'",'-')
    game_name = game_name.replace(".",'')
    game_name = game_name.replace(' ','-')
    

    

    game_detail_url = 'https://www.igdb.com/games/' + game_name
    
    #print(game_details)

    game_desc = None

    page_text = scraping_using_cache(game_detail_url, 'game_detail_cache')
    page_soup = BeautifulSoup(page_text, 'html.parser')
    try:
        game_desc = page_soup.find(class_ = 'gamepage-tabs').select('div > div')[1].find('div').text
    except:
        print(game_name)
        game_desc = None
    
    return game_desc

def init_db():
    conn = create_connection(DBNAME)
    cur = conn.cursor()

    #Drop table
    statement = '''
       DROP TABLE IF EXISTS 'Platforms';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Games';
    '''
    cur.execute(statement)

    conn.commit()

    #Create table Games
    create_games_table_sql = '''
            CREATE TABLE IF NOT EXISTS 'Games' (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Game_id INTEGER,
                Name TEXT,
                Released_date TEXT,
                Rating REAL,
                Description TEXT,
                Platform_id INTEGER,
                FOREIGN KEY (Platform_id) REFERENCES Platforms(platform_id)
            );
    '''
    try:
        cur.execute(create_games_table_sql)
    except Error as e:
        print(e)
        print(create_games_table_sql)
    
    conn.commit()

    #Create table Platforms
    create_platform_table_sql = '''
            CREATE TABLE IF NOT EXISTS 'Platforms' (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform_id INTEGER NOT NULL,
                Name TEXT,
                Image TEXT,
                Game_count INTEGER,
                Game_id INTEGER,
                FOREIGN KEY (Game_id) REFERENCES Games(Game_id)
            );
    '''
    try:
        cur.execute(create_platform_table_sql)
    except Error as e:
        print(e)
        print(create_platform_table_sql)
    
    conn.commit()

    init_insert(conn)

    conn.close()


if __name__ == "__main__":
    init_db()