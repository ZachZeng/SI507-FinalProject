import requests
import sqlite3
from sqlite3 import Error

DBNAME = 'game.db'

class Game(object):
    def __init__(self, name, date, desc, platform):
        self.name = name
        self.date = date
        self.desc = desc
        self.platform = platform
    
    def __str__(self):
        return self.name

def create_connection(db_filename):
    conn = None
    try:
        conn = sqlite3.connect(db_filename)
        return conn
    except Error as e:
        print(e)

    return conn

def get_platform_percentage():
    conn = create_connection(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT Name, AVG(Game_count) FROM Platforms
        GROUP BY platform_id
    '''
    try:
        cur.execute(statement)
    except Error as e:
        print(e)
    result = cur.fetchall()
    conn.close()
    return result

def get_platform_ratings():
    conn = create_connection(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT p.Name, AVG(Rating) FROM 
        Platforms AS p JOIN Games as g ON p.Game_id = g.Game_id
        GROUP BY p.Name
        ORDER BY AVG(Rating) DESC
    '''
    try:
        cur.execute(statement)
    except Error as e:
        print(e)
    result = cur.fetchall()
    #print(result)
    conn.close()
    return result


def get_platform_top():
    conn = create_connection(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT g.Name, g.Released_date, g.Description, MAX(g.Rating), p.Name 
        FROM Games as g JOIN Platforms AS p ON  g.Game_id = p.Game_id
        GROUP BY g.platform_id
    '''
    try:
        cur.execute(statement)
    except Error as e:
        print(e)
    result = cur.fetchall()
    games = []
    for i in result:
        game = Game(i[0],i[1],i[2],i[4])
        games.append(game)
    #print(result)
    conn.close()
    return games

def get_game_detail(game_name):
    conn = create_connection(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT g.Name, g.Released_date, g.Description, p.Name 
        FROM Games as g  JOIN Platforms AS p ON  g.Game_id = p.Game_id
        ''' + 'WHERE g.Name = "'+game_name+'"'+ '''
        GROUP BY p.Name
        '''
    try:
        cur.execute(statement)
    except Error as e:
        print(e)
    result = cur.fetchall()
    games = []
    for i in result:
        game = Game(i[0],i[1],i[2],i[3])
        games.append(game)
    #print(result)
    conn.close()
    return games