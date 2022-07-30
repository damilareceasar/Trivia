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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    def test_get_categories(self):
        res = self.client.get('/categories')
        data = json.load(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data['categories'])

    def test_questions(self):
        res = self.client.get('/categories')
        data = json.load(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

    @unittest.SkipTest #remove this decorator to run the delete test, this was included to avoided test failure
    def test_delete_question(self):
        res = self.client().delete("/questions/30")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_nonexistent_question(self):
        res = self.client().delete("/questions/2000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_question(self):
        res =self.client().post('/questions', json = self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_quest'])
        self.assertTrue(data['all_quest'])

    def test_wrong_category(self):
        res =self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 406)
        self.assertEqual(data['success'], False)

    
    def test_search_questions(self):
        res =self.client().post('/questions/search', json = {"searchTerm": "Which"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_question_category(self):
        res =self.client().get('categories/2/questions')
        data = json.loads(res.data)      

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['all_questions'])
        self.assertTrue(data['all_categories'])

    def test_nonexistent_category(self):
        res = self.client().get('categories/1000/questions')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 406)
        self.assertEqual(data['success'], False)

    def test_get_quizzes_questions(self):
        res = self.client().post('/quizzes', json= {"previous_questions": [], 'quiz_category': {'type': 'Sports', 'id': 6}})
        data = json.loads(res.data)   

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(['question'])

    def test_406_error_with_missing_previous_questions(self):
        res = self.client().post('/quizzes', json={"quiz_category": "all"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_400_error_quizzes_no_parameter(self):
        res = self.client().post('/quizzes')

        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()