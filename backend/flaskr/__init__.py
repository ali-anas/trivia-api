import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO-DONE: Set up CORS. Allow '*' for origins.
  Delete the sample route after completing the TODOs
  '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO-DONE: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,True')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

        '''
  @TODO-DONE:
  Create an endpoint to handle GET requests
  for all available categories.
  '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()

        # if no category found
        if not categories:
            abort(404)

        all_categories = [category.format()['type'] for category in categories]

        # return success response with list of categories
        return jsonify({
            'success': True,
            'categories': all_categories
        })

    '''
  @TODO-DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of
  the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        # if there is no question present
        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        all_categories = [category.format()['type'] for category in categories]

        # return success response
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': all_categories,
            'current_category': all_categories
        })

    '''
  @TODO-DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question,
  the question will be removed.
  This removal will persist in the database and when you
  refresh the page.
  '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def remove_question(question_id):
        # get question from with question_id from database
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        # if question does not exist
        if not question:
            abort(404)

        try:
            # delete and reflect changes to database
            question.delete()

            # return success response
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except BaseException:
            abort(422)

    '''
  @TODO-DONE:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    '''
  @TODO-DONE:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        # creates a question or search a qestion with search
        body = request.get_json()
        # print(body)

        if not body:
            abort(400)

        to_search = body.get('searchTerm', None)

        if to_search:
            # if request contains search term then search question
            # with searchTerm.
            # there can be many questions containing searchTerm.
            # returns each questions containing 'to_search' as substring
            # ex -> if 'to_search' == 'title' then it will returns
            # questions which contains words like
            # title, entitled ...
            questions = Question.query.filter(
                Question.question.ilike(f'%{to_search}%')).all()

            # if there are no such questions
            if not questions:
                abort(404)

            # if found questions then format them
            all_questions = paginate_questions(request, questions)

            # required for response
            categories = Category.query.all()
            all_categories = [category.format()['type']
                              for category in categories]

            # return success response
            # returns total_questions as total no of questions with searchTerm
            return jsonify({
                'success': True,
                'questions': all_questions,
                'total_questions': len(questions),
                'current_category': all_categories
            })

        new_question_text = body.get('question', None)
        new_answer_text = body.get('answer', None)
        new_question_category = body.get('category', None)
        new_question_difficulty = body.get('difficulty', None)

        # check all requirements are full-filled
        if not new_question_text:
            abort(400)
        if not new_answer_text:
            abort(400)
        if not new_question_category:
            abort(400)
        if not new_question_difficulty:
            abort(400)

        try:

            question = Question(
                question=new_question_text,
                answer=new_answer_text,
                category=new_question_category,
                difficulty=new_question_difficulty)

            # if all ok then insert the question and reflect the changes to
            # database
            question.insert()

            # get all questions after insertion
            selections = Question.query.order_by(Question.id).all()
            all_questions = paginate_questions(request, selections)

            # return success response
            return jsonify({
                'success': True,
                'created': question.id,
                'questions': all_questions,
                'total_questions': len(selections)
            })
        except BaseException:
            abort(422)

    '''
  @TODO-DONE:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

    @app.route('/categories/<string:category_id>/questions', methods=['GET'])
    def get_question_by_category(category_id):
        selections = Question.query.filter(
            Question.category == int(category_id)).order_by(
            Question.id).all()

        # if no questions with this category id found
        if not selections:
            abort(404)

        all_questions = paginate_questions(request, selections)

        # return success response
        return jsonify({
            'success': True,
            'questions': all_questions,
            'total_questions': len(selections),
            'current_category': category_id
        })

    '''
  @EXTENDED-DONE:

  API endpoint to create new category
  This end point should respond to post request on categories
  the request message should contain 'type' as key in body.

  '''
    @app.route('/categories', methods=['POST'])
    def create_category():
        body = request.get_json()

        if not body:
            abort(400)

        category_type = body.get('type', None)

        # if type is not provided
        if category_type is None:
            abort(400)
        try:
            # insert new category
            new_category = Category(type=category_type)
            new_category.insert()

            # get all categories and update on view
            selections = Category.query.order_by(Category.id).all()
            all_categories = [category.format() for category in selections]
            # return success response
            return jsonify({
                'success': True,
                'created': new_category.id,
                'categories': all_categories,
                'total_categories': len(selections)
            })
        except BaseException:
            abort(422)

    '''
  @EXTENDED-DONE:
  API endpoint to delete a category
  This endpoint should take category id to delete particular category
  '''

    @app.route('/categories/<int:category_id>', methods=['DELETE'])
    def delete_category(category_id):
        category = Category.query.filter(
            Category.id == category_id).one_or_none()

        # if no category found
        if category is None:
            abort(404)

        try:
            # delete found category and reflect changes to database
            category.delete()

            # return success response
            return jsonify({
                'success': True,
                'deleted': category_id
            })
        except BaseException:
            abort(422)

    '''
  @TODO-DONE:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        if not ('quiz_category' in body and 'previous_questions' in body):
            abort(400)
        try:
            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(
                    Question.id.notin_(
                        (previous_questions))).all()

            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if
            len(available_questions) > 0 else None

            return jsonify({
                'success': True,
                'question': new_question
            })
        except BaseException:
            abort(422)

    '''
  @TODO-DONE:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
