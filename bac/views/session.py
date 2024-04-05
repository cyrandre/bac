from flask import Blueprint,render_template,request,session
from flask import redirect, url_for,jsonify
from flask_login import login_required
from sqlalchemy.sql.expression import func
import random
import json

from bac.plugins.models import Question, Answer,Image, db
from bac.utils.forms import SettingsForm

bp = Blueprint('session',__name__)

@bp.route('/',methods=('GET','POST'))
def index():
    if request.method == 'POST':
        return redirect(url_for('accounts.login'),code=307)
    
    settings = {
        'title':'Bac++',
        'subtitle': 'Bactériologie médicale',  
        'body':'Test tes connaissances en bactériologie médicale',
        'photo':"static/images/home.png"
    }

    return render_template('session/index.html', **settings)

@bp.route('/start',methods=('GET',))
def start():
    training = True #TODO should be in the user's profile
    questions = get_questions() 

    if len(questions) == 0:
        return redirect(url_for('session.index'))
    session['score'] = 0
    session['solutions'] = [q['solution'] for q in questions]

    if not training:
        for question in questions:
            del question['solution']    
    print(f'Questions {questions}')
    return render_template('session/question.html',questions=questions)

@bp.route('/answer',methods=('GET','POST',))
def answer():
    solutions = session.get('solutions',[])
    score = session.get('score',0)
    if request.method == 'POST':
        error = None
        score = request.form.get('score','0')
        try:
            score = int(score)
        except:
            score = 0
        answers = request.form.get('answer',[])
        answers = json.loads(answers)       
        if len(answers) == len(solutions):
            sc = 0
            for answer,solution in zip(answers,solutions):
                if check_answer(answer,solution):
                    sc += 1            
            if score > 0 and sc != score:
                print("Bad score",sc,score) 
            score = sc
        else:
            print(answers)
            print(solutions)
            error = "Wrong number of answers " 
        print('Score:', score)
        session['score'] = score
        if error is not None:
            print(error)
            return jsonify(error=error), 400
        return jsonify({'msg':'Answers submited'})
    
    total = len(solutions)
    return render_template('session/result.html',score=score,total=total)

@bp.route("/settings",methods=("POST","GET"))
@login_required
def settings():
    form = SettingsForm(request.form)
    if request.method == 'POST':
        #TODO
        return redirect(url_for('session.index'))
    
    return render_template('session/settings.html',form=form)

def check_answer(answer,solution):
    ret = True
    for item in answer:
        if not item in solution:
            ret = False
    for item in solution:
        if not item in answer:
            ret = False
    return ret

def model2dict(model):
    result = {}
    for col in model.__table__.columns:
        value = getattr(model,col.name)
        if value is None:
            value = ''
        result[col.name] = value
    return result

def get_questions(n = 10):
    # Cette fonction devrait tenir compte du thème, erreurs passées etc
    questions = []
    models = Question.query.order_by(func.random()).limit(n)
    questions = [load_question(model) for model in models]
    return questions

def load_question(model):
    id = model.id
    question = model2dict(model)
    del question['created_on']
    
    answer = Answer.query.filter_by(question_id=id).all()
    answer = [model2dict(item) for item in answer] 
    
    size = len(answer)
    random.shuffle(answer)
    solution = [ind for ind in range(size) if answer[ind]['solution']]
    for item in answer:
        del item['solution']

    question['choice'] = answer
    question['solution'] = solution
    question['multi'] = 1 if len(solution) > 1  else 0

    image = Image.query.filter_by(question_id = id).all()
    question['image'] =  [model2dict(img) for img in image]
    return question