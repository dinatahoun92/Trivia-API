import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS')
      return response
  
    @app.route('/')
    def index():
      return jsonify({
        'message': 'Welcome to Trivia',
        'success': True,
      })
    
 

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def available_categories():
      try:
        return jsonify({
          'categories': {category.id: category.type for category in Category.query.order_by(Category.type).all()},
          'success':'true'
        })
      except:
        abort(400)

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. c

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''


    def pagination(page, available_questions):
      start = (page - 1) * 10
      end = (page + 1) * 10
      questions = [question.format() for question in available_questions]
      current_questions = questions[start:end]
      return current_questions

    @app.route('/questions')
    def available_questions():
      try:
        page = request.args.get('page', 1, type=int)
        available_questions = Question.query.order_by(Question.id).all()
        current_questions = pagination(page, available_questions)
        return jsonify({
            'questions': current_questions,
            'total_questions': len(available_questions),
            'categories': {category.id: category.type for category in Category.query.order_by(Category.type).all()},
            'current_category': None,
            'success': True
        })
      except:
        abort(400)
      
    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<id>',methods=['DELETE'])
    def delete_question(id):
      try:
          Question.query.get(id).delete()
          return jsonify({
              'id': id,
              'success': True
          })
      except:
          abort(422)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def add_question():
      try:
        question = request.form.get('question')
        answer = request.form.get('answer')
        category = request.form.get('category')
        difficulty = request.form.get('difficulty')
        question = Question(question=question, answer=answer, category=category,difficulty=difficulty)
        question.insert()
        return jsonify({
            'success': True
        })
      except:
        abort(422)

     

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions/search', methods=['POST'])
    def search():
      try:
        search_term = request.form.get('search_term')
        search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        return jsonify({
          'questions': [question.format() for question in search_results],
          'total_questions': len(search_results),
          'success': True,
          'current_category': [search_results['category'] for search_results in search_results]

        })
      except:
        abort(422)
    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<id>/questions', methods=['GET'])
    def get_questions_category(id):
      try:
        questions = Question.query.filter(Question.category == str(id)).all()
        return jsonify({
        "questions": [question.format() for question in questions],
        "current_category": id,
        "total_questions": len(questions),
        })
      except:
        abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route("/random_quiz", methods=["POST"])
    def quiz():
      previous_questions = list(request.form.getlist("previous_questions"))
      category = int(request.form.get("category"))
      if category:
        get_questions = Question.query.filter((Question.category)==(category))
      else:
        get_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
      questions = list(map(Question.format, get_questions))
      return jsonify(random.choice(questions))


          
    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
          "error": 404,
          "message": "resource not found",
          "success": False,
      })

    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
        "error": 422,
        "message": "unprocessable",
        "success": False,
      })

    @app.errorhandler(400)
    def bad_request(error):
      return jsonify({
        "error": 400,
        "message": "bad request",
        "success": False,
      })
    return app

    