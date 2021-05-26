from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = [['R', 'N', 'Y', 'T'], ['T', 'O', 'G', 'P'], ['Y', 'A', 'N', 'A'], ['I', 'A', 'T', 'L']]

    def test_root(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertIn('<h2>Select Game Size</h2>', html)
            self.assertEqual(res.status_code, 200)
            

    def test_game_default_start(self):
        with app.test_client() as client:
            res = client.get('/game')
            html = res.get_data(as_text=True)
            self.assertIn('<button type="submit">restart</button>', html)
            self.assertIn('<div id="high-score">0</div>', html)
            self.assertIn('<div id="plays">0</div>', html)
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['size'], 5)
            self.assertEqual(len(session['board']), 5)
            self.assertEqual(session['scores'], [[],[],[],[],[]])
                             
            
    def test_game_size4(self):
        with app.test_client() as client:
            res = client.get('/game?size=4')
            
            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['size'], 4)
            self.assertEqual(len(session['board']), 4)
            
            
    def test_game_with_past_games(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['scores'] = [[],[],[],[4,16,12,0],[]]
                
            res = client.get('/game?size=4')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<div id="high-score">16</div>', html)
            self.assertIn('<div id="plays">4</div>', html)
            
            
    def test_guess_correct(self):
        with app.test_client() as client:
            client.get('/game?size=4')
            with client.session_transaction() as change_session:
                change_session['board'] = self.board
                
            res = client.post('/guess', json={'guess': "toga"})
            json = res.json
            self.assertEqual(json['result'], 'You got one!')
            self.assertEqual(res.status_code, 200)
            
            
    def test_guess_incorrect(self):
        with app.test_client() as client:
            client.get('/game?size=4')
            with client.session_transaction() as change_session:
                change_session['board'] = self.board
                
            res = client.post('/guess', json={'guess': "spice"})
            json = res.json
            self.assertEqual(json['result'], 'Not on board')
            self.assertEqual(res.status_code, 200)
            
            
    def test_guess_not_word(self):  
        with app.test_client() as client:
            client.get('/game?size=4')
            res = client.post('/guess', json={'guess': "yolo"})
            json = res.json
            self.assertEqual(json['result'], 'Not a word')
            self.assertEqual(res.status_code, 200)
            
            
    def test_game_over(self):
        with app.test_client() as client:
            client.get('/game?size=4')
            self.assertEqual(session['scores'], [[],[],[],[],[]])
            
            res = client.post('/game/over', json={'score': 4})
            json = res.get_data(as_text=True)
            self.assertIn('hi', json)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['scores'], [[],[],[],[4],[]])
            
            client.post('/game/over', json={'score': 16})
            self.assertEqual(session['scores'], [[],[],[],[4,16],[]])