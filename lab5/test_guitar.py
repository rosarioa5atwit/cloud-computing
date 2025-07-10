import unittest 
from unittest.mock import patch, MagicMock
import mysql.connector
from guitar_queries import connect_to_db, query1, query2, query3, query4, query5, query6, query7

class TestGuitarQueries(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_connect_to_db(self, mock_connect):
        mock_connect.return_value = MagicMock()
        db = connect_to_db()
        self.assertIsNotNone(db)
        mock_connect.assert_called_once_with(
            host="localhost",
            user="root",
            password="C@t23321",
            database="my_guitar_shop"
        )

    @patch('mysql.connector.connect')
    def test_query1(self, mock_connect):
        mock_db = MagicMock()
        mock_connect.return_value = mock_db
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        
        expected_results = [
             ("sg", "Gibson SG", 2517.00, 52.00),
            ("les_paul", "Gibson Les Paul", 1199.00, 30.00),
            ("precision", "Fender Precision", 799.99, 30.00),
            ("tama", "Tama 5-Piece Drum Set with Cymbals", 799.99, 15.00),
            ("ludwig", "Ludwig 5-piece Drum Set with Cymbals", 699.99, 30.00),
            ("strat", "Fender Stratocaster", 699.00, 30.00),
            ("hofner", "Hofner Icon", 499.99, 25.00),
            ("fg700s", "Yamaha FG700S", 489.99, 38.00),
            ("rodriguez", "Rodriguez Caballero 11", 415.00, 39.00),
            ("washburn", "Washburn D10S", 299.00, 0.00)
        ]
        mock_cursor.fetchall.return_value = expected_results
        
        actual_results = query1(mock_db)
        
        self.assertEqual(actual_results, expected_results)
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_query2(self, mock_connect):    
        mock_db = MagicMock()
        mock_connect.return_value = mock_db
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        
        expected_results = [
            ('Allan', 'Sherwood', 'Sherwood, Allan'),
            ('Erin', 'Valentino', 'Valentino, Erin'),
            ('Frank Lee', 'Wilson', 'Wilson, Frank Lee'),
            ('Barry', 'Zimmer', 'Zimmer, Barry')
        ]
        mock_cursor.fetchall.return_value = expected_results
        
        actual_results = query2(mock_db)
        
        self.assertEqual(actual_results, expected_results)
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_query3(self, mock_connect):    
        mock_db = MagicMock()
        mock_connect.return_value = mock_db
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        
        expected_results = [
            ('Tama 5-Piece Drum Set with Cymbals', 799.99, '2018-07-30 13:14:15'),
            ('Ludwig 5-piece Drum Set with Cymbals', 699.99, '2018-07-30 12:46:40'),
            ('Fender Precision', 799.99, '2018-06-01 11:29:35'),
            ('Gibson Les Paul', 1199.00, '2017-12-05 16:33:13'),
            ('Fender Stratocaster', 699.00, '2017-10-30 09:32:40')
        ]
        mock_cursor.fetchall.return_value = expected_results
        
        actual_results = query3(mock_db)
        
        self.assertEqual(actual_results, expected_results)
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_query4(self, mock_connect):    
        mock_db = MagicMock()
        mock_connect.return_value = mock_db
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        
        expected_results = [
            (5, 1199.00, 359.70, 2, 2398.00, 719.40, 1678.60),
            (3, 2517.00, 1308.84, 1, 2517.00, 1308.84, 1208.16),
            (1, 1199.00, 359.70, 1, 1199.00, 359.70, 839.30),
            (11, 799.99, 120.00, 1, 799.99, 120.00, 679.99),
            (9, 799.99, 240.00, 1, 799.99, 240.00, 559.99)
        ]
        mock_cursor.fetchall.return_value = expected_results
        
        actual_results = query4(mock_db)
        
        self.assertEqual(actual_results, expected_results)
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_query5(self, mock_connect):    
        mock_db = MagicMock()
        mock_connect.return_value = mock_db
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        
        expected_results = [
            ('Basses', 'Fender Precision', 799.99),
            ('Basses', 'Hofner Icon', 499.99),
            ('Drums', 'Ludwig 5-piece Drum Set with Cymbals', 699.99),
            ('Drums', 'Tama 5-Piece Drum Set with Cymbals', 799.99),
            ('Guitars', 'Fender Stratocaster', 699.00),
            ('Guitars', 'Gibson Les Paul', 1199.00),
            ('Guitars', 'Gibson SG', 2517.00),
            ('Guitars', 'Rodriguez Caballero 11', 415.00),
            ('Guitars', 'Washburn D10S', 299.00),
            ('Guitars', 'Yamaha FG700S', 489.99)
        ]
        mock_cursor.fetchall.return_value = expected_results
        
        actual_results = query5(mock_db)
        
        self.assertEqual(actual_results, expected_results)
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_query6(self, mock_connect):    
        mock_db = MagicMock()
        mock_connect.return_value = mock_db
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        
        expected_results = [
            ('Allan', 'Sherwood', '100 East Ridgewood Ave.', 'Paramus', 'NJ', '07652'),
            ('Allan', 'Sherwood', '21 Rosewood Rd.', 'Woodcliff Lake', 'NJ', '07677')
        ]
        mock_cursor.fetchall.return_value = expected_results
        
        actual_results = query6(mock_db)
        
        self.assertEqual(actual_results, expected_results)
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_query7(self, mock_connect):    
        mock_db = MagicMock()
        mock_connect.return_value = mock_db
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        
        expected_results = [
            ('Allan', 'Sherwood', '100 East Ridgewood Ave.', 'Paramus', 'NJ', '07652'),
            ('Gary', 'Hernandez', '7361 N. 41st St.', 'New York', 'NY', '10012'),
            ('Barry', 'Zimmer', '16285 Wendell St.', 'Omaha', 'NE', '68135'),
            ('Frank Lee', 'Wilson', '23 Mountain View St.', 'Denver', 'CO', '80208'),
            ('Heather', 'Esway', '2381 Buena Vista St.', 'Los Angeles', 'CA', '90023'),
            ('Erin', 'Valentino', '6982 Palm Ave.', 'Fresno', 'CA', '93711'),
            ('David', 'Goldstein', '186 Vermont St.', 'San Francisco', 'CA', '94110'),
            ('Christine', 'Brown', '19270 NW Cornell Rd.', 'Beaverton', 'OR', '97006')
        ]
        mock_cursor.fetchall.return_value = expected_results
        
        actual_results = query7(mock_db)
        
        self.assertEqual(actual_results, expected_results)
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
