from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

 
def name(ad):
    if len(ad)==1:
        return ad.upper()
    else:
        herf_ilk=ad[0].upper()
        
        for i in ad[1:]:
            herf_ilk+=(i.lower())
        return herf_ilk
#User sign up formu
class RegisterForm(Form):
    name=StringField("Ad",validators=[validators.Length(min=1,max=30)])
    surname=StringField("Soyad",validators=[validators.Length(min=1,max=30)])
    password=PasswordField("Parol",validators=[
        validators.DataRequired(message="Zehmet olmasa parol daxil edin!")
    ])

class LoginForm(Form):
    name=StringField("Ad",validators=[validators.Length(min=1,max=30)])
    password=PasswordField("Parol")

app =Flask(__name__)
app.secret_key = b'PythonWeb1234'
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
#Login prosesi
@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm(request.form)
    if request.method=="POST":
      result = db.session.query(
               db.session.query(User_PW)
               .filter(User_PW.fname==form.name.data)
               .exists()
              ).scalar()
    #   exists = User_PW.query.filter_by(fname=str(form.name)).count() > 0 similar code
      if result :
        for user in User_PW.query.filter_by(fname=form.name.data):
            if sha256_crypt.verify(form.password.data,user.password):
                flash("Giriş uğurla başa çatdı.","success")
                return redirect(url_for("indexpage"))
            else:
                 flash("Şifrə yanlışdır!","danger")
      else:
        print("ad sehvdi")
        flash("Bu adda istifadəçi tapılmadı.","danger")
    return render_template("login.html",form=form)

@app.route("/signup",methods=['GET','POST'])
def signup():
   
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
        fnamedata=None
        for result in userRESult:
            fnamedata=name(result.fname)
 
        flash(message=f"{fnamedata} Üzv olmağınız uğurla tamalandı.",category="success")
        # yuxardaki kod sayesinde flash mesajdari (bir nov alert) leri istifade edirik
        return redirect(url_for("login"))
    else:
        return render_template("signup.html",form=form)

if __name__=="__main__":
    app.run(debug=True)
