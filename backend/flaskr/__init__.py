import json
import os
from sre_constants import CATEGORY_LOC_WORD
from unicodedata import category
from flask import Flask, request, abort, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors  = CORS(app,resources={r'/api/*':{'origins':'*'}})
    
    
    '@TODO: Set up CORS. Allow * for origins. Delete the sample route after completing the TODOs'
    
    

    
    
    
    '@TODO: Use the after_request decorator to set Access-Control-Allow'
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods','GET,POST,PUT,DELETE,OPTIONS')
        return response
    
    def paginate(request,selection):
               page = request.args.get('page',1,type=int)
               start = (page-1)*QUESTIONS_PER_PAGE
               end = start + QUESTIONS_PER_PAGE
               myQuestion = [quest.format() for quest in selection]
               allquest = myQuestion[start:end]
               return allquest
    
    """
    def paginate(request,selection):


    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def handleCategory():
        category = Category.query.order_by(Category.id).all()
        my_cat = [cat.format() for cat in category]

        if len(my_cat) == 0:
            abort(404,"No category found")
        else:
            cating = {}
            #cat = [mycat.format() for mycat in category]

            for catlist in my_cat:
                cating[catlist["id"]] = catlist["type"]
        
        
            return jsonify({
                "success":True,
                "categories":cating
                         })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    
    @app.route("/questions")
    def handleQuestions():
          
          
          #allCategory = Category.query.filterby(Category.type).all()
          
          #cat =myCategory.type
         # my_page = request.args.get("page")
          myQuestion = Question.query.order_by(Question.id).all()
          quest = paginate(request,myQuestion)
          #myCategory = Category.query.filter(Category.type==type).one_or_none()
          
          category = Category.query.all()
          my_cat = [cat.format() for cat in category]
          cating = {}
          

          for catlist in my_cat:
            cating[catlist["id"]] = catlist["type"]

          if len(quest) == 0:
            abort(404,'questions not available')
          else:
              return jsonify({
               "questions":quest,
               "total_questions":len(Question.query.all()),
               "success":True,
               "categories":cating
            
                           })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>",methods = ["DELETE"])
    def delete_Question(question_id):
        my_quest = Question.query.get(question_id)

        if my_quest == None:
            abort(404,"question not available")
        else:    
            my_quest.delete()
        
        

            return jsonify({
                 "success":True,
                  "deleted":question_id

        })
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions',methods=["POST"])
    def create_questions():
        body = request.get_json()
        my_question = body.get("question")
        my_answer = body.get("answer")
        my_category = body.get("category")
        my_difficulty = body.get("difficulty")

        new_question = Question(question=my_question,answer=my_answer,category=my_category,
        difficulty=my_difficulty)
        
        my_category = Question.query.get(my_category)
        if my_category == None:
            abort(406,"Category not found")
        else:
             new_question.insert()
       
             new_quest = Question.query.order_by(Question.id).all()
             added_quest = [quest.format()for quest in new_quest]
             return jsonify({"success":True,
                        "new_quest":new_question.id,
                        "all_quest":added_quest})
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search',methods =['POST'])
    def search_term():
        body = request.get_json()
        my_search = body["searchTerm"]
        #art_search = Artist.query.filter(Artist.name.ilike(f'%{artname}%')).all()
        my_question = Question.query.order_by(Question.id).filter(
            Question.question.ilike(f'%{ my_search }%')
        ).all()
        #all_question = paginate(request,my_question)
        questlist = [myquest.format() for myquest in my_question]

        return jsonify({
            "success":True,
            "questions":questlist
        })


        

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:id>/questions", methods =['GET'])
    def get_Questions(id):
        my_Question = Question.query.filter(Question.category == id).all()
        my_category = Category.query.get(id)
        if my_Question or my_category == None:
            abort(404,"question or category not available ")
        else:
            all_Question = paginate(request,my_Question)
            categories = Category.query.filter(Category.id == id).all()
            categorydict = {}
        
            for cato in categories:
                categorydict[cato["id"]] = cato["type"]
        
            return jsonify(
            {   
                "success":True,
                "all_questions":all_Question,
                "all_categories":categorydict
            }
        )

        

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        
        try:
            body = request.get_json()

            current_category = body.get('quiz_category')
            previous_question = body.get('previous_questions')



            if current_category['type'] == 'click':
                gotten_questions = Question.query.filter(Question.id.notin_((previous_question))).all()

            else: 
                gotten_questions = Question.query.filter_by(category=current_category['id']
                ).filter(Question.id.notin_((previous_question))).all()

            questions = gotten_questions[random.randrange(0, len(gotten_questions))].format() if len(gotten_questions) > 0 else None

            return jsonify({
                "success": True,
                "question": questions
            })
        except:
            abort(422, "Quiz not found")
        
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error":404,"message":"resource not found"}),404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"error":422,"message":"unprocessable"}),422
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error":400,"message":"bad request"}),400
        
    @app.errorhandler(406)
    def not_acceptable(error):
        return jsonify({
            "success": False,
            "Error":f'{error}'
        }),406

    return app

   