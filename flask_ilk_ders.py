from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt


#User sign up formu
class RegisterForm(Form):
    name=StringField("Ad",validators=[validators.Length(min=1,max=30)])
    surname=StringField("Soyad",validators=[validators.Length(min=1,max=30)])
    password=PasswordField("Parol",validators=[
        validators.DataRequired(message="Zehmet olmasa parol daxil edin!")
    ])

app =Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgre1234@localhost:5432/user_pw'

db=SQLAlchemy(app)

class User_PW(db.Model):

    __tablename__='user_pw_table'

    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(30))
    lname=db.Column(db.String(30))
    password=db.Column(db.String(300))

    def __init__(self,fname,lname,password):
        self.fname=fname
        self.lname=lname
        self.password=password

@app.route("/")
def indexpage():
    # return "Ana seyfe"
    person=dict()
    person[1]="Amid Adullayev"
    person[2]="Umid Shahmarov"
    
    return render_template("index.html",person=person,secim=1)

@app.route("/about")
def about():
    reqemler=[1,2,3,4,5,6]
    return render_template("about.html",reqemler=reqemler)
@app.route("/about/<string:id>")
def detail(id):
    return "About id:"+id 

# @app.route("/signup")
# def signup():
#     return render_template("signup.html")
@app.route("/signup",methods=['GET','POST'])
def signup():
    fnamedata=''
    form=RegisterForm(request.form)
    if request.method=="POST" and form.validate():
        fname=request.form['name']
        lname=request.form['surname']
        password=sha256_crypt.encrypt( request.form['password'])
        
        with app.app_context():
            db.create_all()
        user= User_PW(fname,lname,password)   
        db.session.add(user)
        db.session.commit()

        userRESult=db.session.query(User_PW).filter(User_PW.fname==fname)
        success=userRESult
        fnamedata=fname
        for result in userRESult:
            print(result.fname ,result.lname)
        return render_template("success.html",data=fnamedata.upper())
     
    else:
        return render_template("signup.html",form=form)

if __name__=="__main__":
    app.run(debug=True)
