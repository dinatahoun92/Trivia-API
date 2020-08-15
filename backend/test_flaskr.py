import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://Dina:1992@localhost:5432/trivia'
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # test get categories
    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    # test get questions (pages)
    def test_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['success'], True)

     #test delete question
    def test_delete_question(self):
        res = self.client().delete('/questions/17')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'],True)


    #test create a question
    def test_create_question(self):
        self.question = {
        'question': 'question1',
        'answer': 'answer1',
        'category': 1,
        'difficulty': 1
        }
        res = self.client().post('/questions', json= self.question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # test search question
    def test_search(self):
        search_term = {"search_term": "is"}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test get question by category
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)
        questions = Question.query.filter(Question.category == str(1)).all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
    
    #Test random quiz
    def test_random_quiz(self):
        quiz = {
            'previous_questions': [],
            'category': {'id': '1', 'category': '4'}
        }
        res = self.client().post('/random_quiz', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()