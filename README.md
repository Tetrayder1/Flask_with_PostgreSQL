
<h1 align="left">Flask_with_PostgreSQL</h1>

###

<p align="left">Bu proyekt pythonda flask framework-ündən istifadə edərək web-dən alınan məlumatları PostgreSQL DB-inə  yazır</p>

###

<h2 align="left">Gedişatlar</h2>

###

<p align="left">✨ Flask ile web platformanin yaradilması<br>📚 SqlAlchemy ile ORM prosesinin həyata keçirilməsi<br>🎯 WTForm ile məlumatların göndərilməsi<br>🎲 Alınan məlumatların PostgreSQL DB-inə göndərilməsi</p>

###
<p align="left">İstifadə edilən kitabxanalar</p>

```python
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
```

<p align="left"></p>

```python

class RegisterForm(Form):
    name=StringField("Ad",validators=[validators.Length(min=1,max=30)])
    surname=StringField("Soyad",validators=[validators.Length(min=1,max=30)])
    password=PasswordField("Parol",validators=[
        validators.DataRequired(message="Zehmet olmasa parol daxil edin!")#DataRequired bizə parolu boş keçməyə imkan vermir
    ])

```
<p align="left">Yuxarıdakı kod örnəyi validation yaratmaq üçündür</p>

<p align="left"></p>

```python
#postgresql ünvanı
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgre1234@localhost:5432/user_pw'

db=SQLAlchemy(app)
#User sinifi – ORM modeldir, və users adlı cədvəli təmsil edir.
class User_PW(db.Model):
#table name
    __tablename__='user_pw_table'
#Column name
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(30))
    lname=db.Column(db.String(30))
    password=db.Column(db.String(300))

    def __init__(self,fname,lname,password):
        self.fname=fname
        self.lname=lname
        self.password=password

```
<p align="left">Bu kod örnəyi isə SQLAlchemy ilə ORM edilməsidir.</p>

<p align="left"></p>

```python
@app.route("/signup",methods=['GET','POST'])
def signup():
    fnamedata=''
    form=RegisterForm(request.form)
    if request.method=="POST" and form.validate():
        fname=request.form['name']
        lname=request.form['surname']
        password=sha256_crypt.encrypt( request.form['password'])#Şifrəni şifrələmək
        
        with app.app_context():# Flask konteksti daxilində əməliyyat aparmaq üçün istifadə olunur (vacibdir).
            db.create_all()# mövcud modellər əsasında cədvəlləri DB-də yaradır(ORM öz işini görür)
        user= User_PW(fname,lname,password)   #model obyektidir.
        db.session.add(user)#obyekti sessiyaya əlavə edir.
        db.session.commit()# məlumatları bazaya həqiqətən yazır.

        userRESult=db.session.query(User_PW).filter(User_PW.fname==fname)
        success=userRESult
        fnamedata=fname
        for result in userRESult:
            print(result.fname ,result.lname)
        return render_template("success.html",data=fnamedata.upper())
     
    else:#GET işə düşür
        return render_template("signup.html",form=form)
```



<p align="left"></p>

###

<h2 align="left">I code with</h2>

###

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" height="40" alt="postgresql logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" height="40" alt="flask logo"  />
</div>

###




