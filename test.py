import utils
import unittest
import os
import sqlite3

class TestUtils(unittest.TestCase):
    def test_get_data_csv_path(self):
        self.assertEqual(utils.get_data_csv_path(), 'data/data.csv')
        
    def test_get_data_db_path(self):
        self.assertEqual(utils.get_data_db_path(), 'data/data.db')            
        
    def test_create_db(self):
        utils.create_db('data/test.db', 'test', ['id', 'name', 'age', 'gender', 'city', 'state', 'country', 'zip_code', 'email', 'phone_number'])
        
        conn = sqlite3.connect('data/test.db')        
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test'")
        result = cursor.fetchone()
        self.assertEqual(result is not None, True)        
        conn.close()
        os.remove('data/test.db')
        
    def test_insert_data(self):
        utils.create_db('data/test.db', 'test', ['id', 'name', 'age', 'gender', 'city', 'state', 'country', 'zip_code', 'email', 'phone_number'])
        utils.insert_data('data/test.db', 'test', [(1, 'John Doe', 25, 'Male', 'New York', 'NY', 'USA', '10001', 'john@example.com', '123-456-7890')])
        
        conn = sqlite3.connect('data/test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test")
        data = cursor.fetchall()
        self.assertEqual(data, [(1, 'John Doe', 25, 'Male', 'New York', 'NY', 'USA', '10001', 'john@example.com', '123-456-7890')])
        conn.close()
        os.remove('data/test.db')

    def test_read_data(self):
        utils.create_db('data/test.db', 'test', ['id', 'name', 'age', 'gender', 'city', 'state', 'country', 'zip_code', 'email', 'phone_number'])
        utils.insert_data('data/test.db', 'test', [(1, 'John Doe', 25, 'Male', 'New York', 'NY', 'USA', '10001', 'john@example.com', '123-456-7890')])
        
        data = utils.read_data('data/test.db', 'test')
        self.assertEqual(data, [(1, 'John Doe', 25, 'Male', 'New York', 'NY', 'USA', '10001', 'john@example.com', '123-456-7890')])
        os.remove('data/test.db')

    def test_read_dataframe(self):
        utils.create_db('data/test.db', 'test', ['id', 'name', 'age', 'gender', 'city', 'state', 'country', 'zip_code', 'email', 'phone_number'])
        utils.insert_data('data/test.db', 'test', [(1, 'John Doe', 25, 'Male', 'New York', 'NY', 'USA', '10001', 'john@example.com', '123-456-7890')])
        
        df = utils.read_dataframe('data/test.db', 'test')
        self.assertEqual(df.iloc[0]['name'], 'John Doe')
        os.remove('data/test.db')                    
        
    def test_update_data(self):
        utils.create_db('data/test.db', 'test', ['id', 'name', 'age', 'gender', 'city', 'state', 'country', 'zip_code', 'email', 'phone_number'])
        utils.insert_data('data/test.db', 'test', [(1, 'John Doe', 25, 'Male', 'New York', 'NY', 'USA', '10001', 'john@example.com', '123-456-7890')])
        
        utils.update_data('data/test.db', 'test', [(1, 'John Doe', 25, 'Male', 'New York', 'NY', 'USA', '10001', 'john@example.com', '123-456-7890')])
        
        conn = sqlite3.connect('data/test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test")
        data = cursor.fetchall()
        self.assertEqual(data, [(1, 'John Doe', 25, 'Male', 'New York', 'NY', 'USA', '10001', 'john@example.com', '123-456-7890')])
        conn.close()
        os.remove('data/test.db')

    def test_delete_data(self):        
        utils.create_db('data/test.db', 'test', ['id', 'name', 'age', 'gender', 'city', 'state', 'country', 'zip_code', 'email', 'phone_number'])
        utils.insert_data('data/test.db', 'test', [(1, 'John Doe', 25, 'Male', 'New York', 'NY', 'USA', '10001', 'john@example.com', '123-456-7890')])
        
        utils.delete_data('data/test.db', 'test', [(1,)])
        
        conn = sqlite3.connect('data/test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test")
        data = cursor.fetchall()
        self.assertEqual(data, [])
        conn.close()
        os.remove('data/test.db')

if __name__ == '__main__':
    unittest.main()