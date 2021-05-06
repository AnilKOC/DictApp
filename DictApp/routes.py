from .models import Word,User
from .form import RegistrationForm,LoginForm, WordForm, WordInsert, Practice
from flask import render_template,redirect,flash,url_for, request,abort
from . import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from . import wordapi
import random

@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    practice=0
    try:
        post=Word.query.filter_by(user_id=current_user.id).all()
        if len(post)>= 10:
            practice=1
        post = list(reversed(post))
    except:
        post = None
    form = WordForm()
    form2 = WordInsert()
    if form.validate_on_submit() and form.search.data:
        word = str(request.form.get("word"))
        try:
            definition,example = wordapi.search(word)
        except:
            flash('Your word cannot found in api!', 'danger')
            return redirect(url_for('home'))
        result = [
            {
                "word": word,
                "definition": definition,
                "example": example
            }
        ]
        return render_template('home.html',posts=post, title="Home", form=form, result=result,form2=form2,practice=practice)
    if form2.validate_on_submit() and form2.insert.data:
        word = str(request.form["word"])
        definition = str(request.form["definition"])
        examples = str(request.form["examples"])
        word_insert = Word(word=word,definition=definition,examples=examples,power=0,user_id=current_user.id)
        if Word.query.filter((Word.word == word) & (Word.user_id == current_user.id)).first() == None:
            db.session.add(word_insert)
            db.session.commit()
            flash('Your word has been inserted!','success')
        return redirect(url_for('home'))

    return render_template('home.html',posts=post, title="Home", form=form, practice=practice,login_test=1)

@app.route('/practice',methods=['GET','POST'])
@login_required
def practice():
    if 'button1' in request.form:
        text = request.form['text']
        button =request.form['button1']
        quer = Word.query.filter_by(definition=text).first()
        if quer.word == button:
            quer.power = quer.power + 1
            db.session.add(quer)
            db.session.commit()
        else:
            quer.power = quer.power - 2
            db.session.add(quer)
            quer2 = Word.query.filter_by(word=button).first()
            quer2.power = quer2.power -1
            db.session.add(quer2)
            if quer.word == request.form['secret2']:
                quer3 = Word.query.filter_by(word=request.form['secret3']).first()
                quer3.power = quer3.power - 1
                db.session.add(quer3)
            if quer.word == request.form['secret3']:
                quer3 = Word.query.filter_by(word=request.form['secret2']).first()
                quer3.power = quer3.power - 1
                db.session.add(quer3)
            db.session.commit()
    if 'button2' in request.form:
        text = request.form['text']
        button =request.form['button2']
        quer = Word.query.filter_by(definition=text).first()
        if quer.word == button:
            quer.power = quer.power + 1
            db.session.add(quer)
            db.session.commit()
        else:
            quer.power = quer.power - 2
            db.session.add(quer)
            quer2 = Word.query.filter_by(word=button).first()
            quer2.power = quer2.power -1
            db.session.add(quer2)
            if quer.word == request.form['secret1']:
                quer3 = Word.query.filter_by(word=request.form['secret3']).first()
                quer3.power = quer3.power - 1
                db.session.add(quer3)
            if quer.word == request.form['secret3']:
                quer3 = Word.query.filter_by(word=request.form['secret1']).first()
                quer3.power = quer3.power - 1
                db.session.add(quer3)
            db.session.commit()
    if 'button3' in request.form:
        text = request.form['text']
        button =request.form['button3']
        quer = Word.query.filter_by(definition=text).first()
        if quer.word == button:
            quer.power = quer.power + 1
            db.session.add(quer)
            db.session.commit()
        else:
            quer.power = quer.power - 2
            db.session.add(quer)
            quer2 = Word.query.filter_by(word=button).first()
            quer2.power = quer2.power -1
            db.session.add(quer2)
            if quer.word == request.form['secret1']:
                quer3 = Word.query.filter_by(word=request.form['secret2']).first()
                quer3.power = quer3.power - 1
                db.session.add(quer3)
            if quer.word == request.form['secret2']:
                quer3 = Word.query.filter_by(word=request.form['secret1']).first()
                quer3.power = quer3.power - 1
                db.session.add(quer3)
            db.session.commit()
    form = Practice()
    if len(Word.query.filter_by(user_id=current_user.id).all()) < 10:
        return redirect(url_for('home'))
    wordlist = Word.query.filter_by(user_id=current_user.id).all()
    id1 = random.randint(0, len(wordlist)-1)
    question = wordlist[id1]
    while True:
        id2 = random.randint(0, len(wordlist) - 1)
        id3 = random.randint(0, len(wordlist) - 1)
        if id1!=id2 and id2!=id3 and id1!=id3:
            break
    answare = [question.word,wordlist[id2].word,wordlist[id3].word]
    random.shuffle(answare)
    content = [
        {
            'question':question.definition,
            'answare1':answare[0],
            'answare2':answare[1],
            'answare3':answare[2],

        }
    ]
    return render_template('practice.html', content=content, form=form, login_test=1)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/<int:word_id>/delete')
@login_required
def delete(word_id):
    word = Word.query.get(word_id)
    if word.user_id != current_user.id:
        abort(403)
    db.session.delete(word)
    db.session.commit()
    flash('Your word has been deleted!', 'danger')
    return redirect(url_for('home'))