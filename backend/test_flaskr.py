import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from config import db_details
from flask import request


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = db_details["test_db_name"]
        self.database_path = "postgres://{}:{}@{}/{}".format(db_details["user"], db_details["password"], 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'This is a test question',
            'answer': 'Test',
            'category': 5,
            'difficulty': 1
        }

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
    TODO-DONE
    Write at least one test for each test for successful operation and for expected errors.
    """
    # ---------------------------------------------------------------#
    # Test on 'GET' '/questions'
    # ---------------------------------------------------------------#
    def test_get_questions_paginated(self):
        ''' Test all questions from all categories. '''
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_questions_not_available(self):
        ''' Test all questions with no existing page'''
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_405_wrong_method_to_get_questions(self):
        ''' Testing wrong method to get all questions '''
        res = self.client().patch('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # -----------------------------------------------------------------#
    # Test on 'POST' '/questions'
    # -----------------------------------------------------------------#
    def test_create_question(self):
        ''' Test on POST request to create new question '/questions' '''
        

        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_create_question_with_missing_details(self):
        ''' Test on POST request to create new question with missing details '/questions' '''
        incomplete_question = {
            'question': 'This is a test question',
            'answer': 'Test',
            'difficulty': 1
        }

        res = self.client().post('/questions', json=incomplete_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_search_question_with_search_term_success(self):
        ''' Test on POST request to search with a search term that already exist. '''
        res = self.client().post('/questions', json={'searchTerm' : 'test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_question_with_search_term_not_found(self):
        ''' Test on POST request to search with a search term that does not exist '''
        res = self.client().post('/questions', json={'searchTerm': 'This would definitely not present'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # ----------------------------------------------------------------#
    # Test on 'DELETE' '/questions/<int:question_id>'
    # ----------------------------------------------------------------#
    def test_delete_question(self):
        ''' Test on DELETE request on question '''
        ''' First create a question and get its question id then make test'''
        to_be_deleted = {
            'question': 'Is this question going to be deleted?',
            'answer': 'a big yes',
            'category': '5',
            'difficulty': '3'
        }
        res = self.client().post('/questions', json=to_be_deleted)
        data = json.loads(res.data)
        question_id = data['created']

        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)

    def test_404_question_not_found_while_deleting(self):
        ''' Test on DELETE request with question id which is not present '''
        res = self.client().delete('/questions/{}'.format(15211521))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # -----------------------------------------------------------------#
    # Test on 'POST' '/quizzes'
    # -----------------------------------------------------------------#

    def test_play_quiz(self):
        ''' Test on POST request on play_quiz with selected category '''
        quiz_details = {
            'previous_questions': [1,3],
            'quiz_category': {
                'type': 'Geography',
                'id': 3
            }
        }

        res = self.client().post('/quizzes', json=quiz_details)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # checks on random question selected
        self.assertTrue(data['question']['question'])
        self.assertTrue(data['question']['id'] not in quiz_details['previous_questions'])


    def test_405_wrong_method_on_quiz(self):
        ''' Test on wrong method request on play_quiz ex - get, patch, etc...'''
        res = self.client().get('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_400_error_play_quiz_without_questions(self):
        '''Test on play_quiz without providing category_details details'''
        quiz_details = {
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=quiz_details)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # '/categories/<string:category_id>/questions'

    #----------------------------------------------------------------------------#
    # Extended-part: Test on 'POST' /'categories'
    #----------------------------------------------------------------------------#

    def test_create_category(self):
        '''Test on category to create a new category '''
        new_category = {
            'type': 'Favourites'
        } 

        res = self.client().post('/categories', json=new_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])

    def test_400_create_category_missing_details(self):
        '''Test for error 400 on POST while creating new category '''

        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')



    # --------------------------------------------------------------------#
    # TEST on 'GET' '/categories'
    # --------------------------------------------------------------------#
    def test_get_categories(self):
        ''' Test on category 
            first create a category and insert it for successful test.
            successful if we get some categories.
        '''
        category = {
            'type': 'Favourites'
        }

        res = self.client().post('/categories', json=category)

        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_405_wrong_method_to_get_categories(self):
        ''' Test on category provided the wrong method
            i.e. methods other than get(), like - patch(), put() etc...
        '''
        res = self.client().patch('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_questions_by_category(self):
        '''Test on category provided category_d get all
            questions having category id as category_d
        '''
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], '3')

    def test_400_no_questions_within_given_category(self):
        '''Test on category provided category_id corresponding
            to which there are no questions
        '''
        res = self.client().get('/categories/15211521/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_405_wrong_method_to_get_questions_by_category(self):
        '''Test on get questions by category by making request
            with methods that are not allowed ex- post(), patch(), etc...
        '''
        res = self.client().post('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # ----------------------------------------------------------------------------#
    # Extended-part: Test on 'DELETE' '/categories'
    # ----------------------------------------------------------------------------#
    def test_delete_category(self):
        '''test on deleting category
            just get one category
            and try to delete it
        '''
        # get recently inserted category
        category_id = Category.query.order_by(Category.id.desc()).first().id

        res = self.client().delete('/categories/{}'.format(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], category_id)

    def test_404_no_such_category_exist(self):
        '''test on deleting category
            provide an id which you know does not exist.
        '''
        res = self.client().delete('/categories/{}'.format(1521521))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()