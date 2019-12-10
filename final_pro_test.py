import unittest
import json
from app import *
from model  import *
from store_data import *
import sqlite3


class TestStore(unittest.TestCase):
    def test_platform_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        
        sql = 'SELECT Name FROM Platforms'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('PC',), result_list)
        self.assertEqual(len(result_list), 294)

        sql = '''
            SELECT Name, Game_count FROM Platforms
            WHERE Name = "PC"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 6)
        self.assertEqual(result_list[0][1], 193944)

        conn.close()

    def test_game_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        
        sql = 'SELECT Name FROM Games'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Archon: The Light and the Dark',), result_list)
        self.assertEqual(len(result_list), 294)

        sql = '''
            SELECT Name, Rating FROM Games
            WHERE Name = "Bastion"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 2)
        self.assertEqual(result_list[0][1], 4.24)

        conn.close()


class TestModel(unittest.TestCase):
    def test_get_platform_percentage(self):
        result = get_platform_percentage()
        self.assertEqual(len(result),49)

    def test_get_platform_ratings(self):
        result = get_platform_ratings()
        self.assertEqual(result[0][1],4.392692307692306)
        self.assertEqual(len(result),49)

    def test_get_platform_top(self):
        result = get_platform_top()
        self.assertEqual(result[0][0],'The Witcher 3: Wild Hunt')
        self.assertEqual(len(result),49)
    
    def test_get_game_detail(self):
        result = get_game_detail('The Witcher 3: Wild Hunt')
        self.assertEqual(len(result),4)
        result_ = get_game_detail('Minecraft')
        self.assertEqual(result_[0][3],'Nintendo 3DS')

        
if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   unittest.main()

