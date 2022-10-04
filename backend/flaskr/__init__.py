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
    #Cors allows * for origin
    #cors  = CORS(app,resources={r'/api/*':{'origins':'*'}})
    #cors = CORS(app, resources={r"/api/*":{"origins": "*"}})
    cors =  CORS(app, resources={'/': {'origins': '*'}})
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
    #handles the Categories route
    @app.route("/categories", methods = ['GET'])
    def handleCategory():
        category = Category.query.order_by(Category.id).all()
        my_cat = [cat.format() for cat in category]
       #Determine if categories are available
        if len(my_cat) == 0:
            abort(404,"No category found")
        else:
            cating = {}
            #cat = [mycat.format() for mycat in category]
            #loops through the list of categories
            for catlist in my_cat:
                cating[catlist["id"]] = catlist["type"]
        
        #return  a jsonify object
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
    #Handles list of questions,categories,total questions
    @app.route("/questions",methods = ["GET"])
    def handleQuestions():
          
          
          #allCategory = Category.query.filterby(Category.type).all()
          
          #cat =myCategory.type
         # my_page = request.args.get("page")
         #queries database for questions
          page = request.args.get("page", 1, type=int)
          myQuestion = Question.query.order_by(Question.id).all()
          quest = paginate(request,myQuestion)
          #myCategory = Category.query.filter(Category.type==type).one_or_none()
          #loops throught list of categories
          category = Category.query.all()
          my_cat = [cat.format() for cat in category]
          cating = {}
          
          
          for catlist in my_cat:
            cating[catlist["id"]] = catlist["type"]

          if len(quest) <= 0:
            abort(404,'questions not available')
          else:#else returns jsonify object
              return jsonify({
               "questions":quest,
               "total_questions":len(Question.query.all()),
               "success":True,
               "categories":cating,
                "page":page
                           })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    #Handles the deletion of questions
    
    @app.route("/questions/<int:question_id>",methods = ["DELETE"])
    def delete_Question(question_id):
        my_quest = Question.query.get(question_id)

        if my_quest == None:
            abort(404,"question not available")
        else:    
            my_quest.delete()#deletes intended questions if available
        
        
            #return a jsonify object
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
    #handles the creation of question
    
    @app.route('/questions',methods=["POST"])
    def create_questions():
        #Retrieves all variable named request from the frontend
        body = request.get_json()
        question = body["question"]
        answer = body["answer"]
        category = body["category"]
        difficulty = body["difficulty"]
        #inserts data into database tables
        print(category,answer,question,difficulty)
        
        
        
        try:
            if question is None or answer is None or category is None or difficulty is None:
                abort(404,"Entry not valid")
            else:
                new_question = Question(question=question,answer=answer,category=category,difficulty=difficulty)
                new_question.insert()

               # new_quest = Question.query.order_by(Question.id).all()
               # all_quest = [quest.format()for quest in new_quest]
                #all_quest = Question.query.all()
                questions = Question.query.order_by(Question.id).all()
                all_quest = [question.format() for question in questions]
             #returns jsonify object
                return jsonify({"success":True,
                        "questions":len(Question.query.all()),
                        "allquestions":all_quest
                       })
        except:
            abort(422,"Unexpected Error")
    
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    #Handle search request
    
    @app.route('/questions/search',methods =['POST'])
    def search_term():
        body = request.get_json()
        my_search = body["searchTerm"]
        #art_search = Artist.query.filter(Artist.name.ilike(f'%{artname}%')).all()
        #Searches through the table for the specified question
        my_question = Question.query.order_by(Question.id).filter(
            Question.question.ilike(f'%{ my_search }%')
        ).all()
        #all_question = paginate(request,my_question)
        questlist = [myquest.format() for myquest in my_question]
        #Returns jsonify object
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
    #Gets questions based on categories
    @app.route("/categories/<int:id>/questions", methods =['GET'])
    def get_Questions(id):
        my_Question = Question.query.filter(Question.category == id).all()
        all_category = Category.query.get(id)
        all_question = paginate(request,my_Question)
        if all_category is None or all_question is None:
            abort(404)
      
        return jsonify(
            {   
                "success":True,
                "questions":all_question,
               
                
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
    #handles quizzes request form the frontend
    ''''''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        prev_quest = body.get('previous_questions')
        

        if (quiz_category is None) or (prev_quest is None):
            abort(400)

        elif (quiz_category['id'] == 0):
            questions = Question.query.filter(Question.id.notin_((prev_quest))).all()
            
        else:
            questions = Question.query.filter_by(category=quiz_category['id']
                ).filter(Question.id.notin_((prev_quest))).all()
            #questions = Question.query.filter_by(category=quiz_category['id']).all()

        def random_quest():
            return questions[random.randrange(0, len(questions), 1)]
            #rand=random.choice(range(1,len(questions)))
            #random_question = questions[rand]
            #return random_question
        def confirm(question):
            check = False
            for quest in prev_quest:
                if (quest == question.id):
                    check = True

            return check

        random_question = random_quest()
        while (confirm(random_question)):
            random_question = random_quest()

    
        return jsonify({
            'success': True,
            'question': random_question.format()
        })










    '''
    @app.route('/quizzes', methods=['POST'])
    def play():
        
        
            body = request.get_json()

            category = body['quiz_category']
            question = body['previous_questions']
            

            if ((category is None) or (question is None)):
                abort(400)
            if category['id'] == 0:
            
                 all_questions = Question.query.all()  
                 quest = [myquest.format() for myquest in all_questions]
                 rand=random.choice(range(1,len(quest)))
                 random_question = quest[rand]
                 return {
                    "success":True,
                    "question":random_question
                 }
                    
                 
                 

            else: 
                   all_questions = Question.query.filter_by(category=category['id']).all()

                   rand=random.choice(range(1,len(all_questions)))
                   random_question = all_questions[rand]

           
            

            def confirm(rand_quest):
                used = False
                for q in question:
                  if (q == question.id):
                        used = True

                return used
            

            
            while True:
                 if confirm(random_question == True):
                   rand=random.choice(range(1,len(all_questions)))
                   random_question = all_questions[rand]
                 else:
                    break   
                
            return jsonify({
                        "success":True,
                         "question":random_question.format()     
                        })
        '''             
                   
    
              

    # Create error handlers for all expected errors
    # including 404 and 422.
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

