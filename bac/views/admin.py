
from flask import (
    Blueprint,redirect,render_template,request,url_for,current_app,jsonify
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from bac.utils.decorators import admin_required
from bac.plugins.models import Question, Answer,Image, db

bp = Blueprint('admin',__name__,url_prefix='/admin')

@bp.route('/viewquest')
@admin_required
def viewquest():
    questions = []
    models = Question.query.all()
    for model in models:
        question = load_question(model)
        questions.append(question)

    return render_template('admin/viewquest.html',questions=questions)

@bp.route('/<int:id>/update', methods=('GET','POST'))
@admin_required
def editquest(id):
    if request.method == 'POST':
        if len(request.form) > 0:
            title = request.form.get('title')
            body = request.form.get('body')    
            if isinstance(body,str):
                body = body.strip() 

            legend = request.form.get('legend')
            choices = []
            choice = request.form.get('choice')
            if choice is not None:
                choices.append(choice)
            else:
                for i in range(5):
                    choice = request.form.get('choice'+str(i))
                    if choice is not None:
                        choices.append(choice)

            answers = []        
            answer = request.form.get('answer')
            if answer is not None:
                answers.append(answer)
            else:
                for i in range(5):
                    answer = request.form.get('answer'+str(i))
                    if answer is not None:
                        answers.append(answer)

            error = None
            if not title:
                error = 'Title is required'
            if len(answers) == 0:
                error = 'Answer is required'

            if error is not None:
                # Debug
                print('Error',error)
                return jsonify(error=error), 400
            else:
                if id > 0:                    
                    print(f'Update {id}')
                    Question.query.filter_by(id=id).update({'title':title,
                                           'body':body,
                                           'legend':legend})
                    
                else:
                    print('Insert new question')
                    question = Question(
                        title=title,
                        body = body,
                        legend = legend,
                        created_on = datetime.now()
                    )
                    db.session.add(question)
                    db.session.flush()
                    db.session.refresh(question)        
                    id = question.id
                    print(f'Question id {id}')

                Answer.query.filter_by(question_id=id).delete()
                for answer in answers:
                    print(f'Add answer to question {id}')
                    db.session.add(Answer(
                        title = answer,
                        question_id = id,
                        solution=True,
                    ))
                    
                if choices is not None:
                    for answer in choices:
                        print(f'Add choice to question {id}')
                        db.session.add(Answer(
                            title = answer,
                            question_id = id,
                            solution=False,
                        ))
                
                Image.query.filter_by(question_id=id).delete()
                images = []
                for i in range(5):
                    image = request.form.get('image'+str(i))
                    if image is not None:
                        images.append(image)
                        
                for path in images:
                    print(f'Keep {path} for question  {id}')
                    db.session.add(Image(question_id=id,path=path))

                for key,file in request.files.items():
                    print(f'Upload {key} {file}')
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        path = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
                        file.save(path)
                        path = os.path.sep+os.path.relpath(path,'bac')
                        db.session.add(Image(question_id=id,path=path))
                db.session.commit() 
        return jsonify({'msg':'Question submited'})

    if id > 0:
        question = get_question(id)
    else:
        question = None
    
    print(f'Question {question}')

    return render_template('admin/editquest.html',question=question) 

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/<int:id>/deletequest')
@admin_required
def deletequest(id):
    Question.query.filter_by(id=id).delete()
    Answer.query.filter_by(question_id = id).delete()
    Image.query.filter_by(question_id = id).delete()
    db.session.commit()
    return redirect(url_for('admin.viewquest'))

def model2dict(model):
    result = {}
    for col in model.__table__.columns:
        value = getattr(model,col.name)
        if value is None:
            value = ''
        result[col.name] = value
    return result

def load_question(model):
    id = model.id
    question = model2dict(model)

    answers = Answer.query.filter_by(question_id=id).all()
    answers = [model2dict(item) for item in answers]
    answer = list(filter(
        lambda item: item['solution'],answers))
    choice = list(filter(
        lambda item: not item['solution'], answers))
    
    for item in answer:
        del item['solution']
    for item in choice:
        del item['solution']

    question['choice'] = choice
    question['answer'] = answer
    image = Image.query.filter_by(question_id = id).all()
    question['image'] =  [model2dict(img) for img in image]
    
    return question

def get_question(id):
    model = Question.query.filter_by(id = id).first()
    if model is None:
        abort(404,f"No question found")

    return load_question(model)    
