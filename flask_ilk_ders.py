from flask import Flask,render_template,session,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
from sqlalchemy import delete
from datetime import datetime,timedelta

#bu method decorator methodudur biz bunun vasitesi ile giris etmeyenlere qadaqa qoyuruq
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Giriş etməlisiniz!","warning")
            return redirect(url_for("login"))
       
    return decorated_function
 
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

class ArticlesForm(Form):
    title=StringField("Başlıq",validators=[validators.Length(min=1,max=150)])
    content=TextAreaField("Mətn",validators=[validators.Length(min=1)])

app =Flask(__name__)
app.secret_key = b'PythonWeb1234'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgre1234@localhost:5432/user_pw'

db=SQLAlchemy(app)

class Article_PW(db.Model):
    __tablename__ ='article_pw_table'

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String())
    content=db.Column(db.Text)
    author=db.Column(db.String())
    created_date=db.Column(db.DateTime)

    def __init__(self,title,content,author,created_date):
         self.title=title
         self.content=content
         self.author=author
         self.created_date=created_date

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
                session["logged_in"]=True
                session["username"]=user.fname
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

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required#giris etmesen bu method islemir
def dashboard():
    data=dict()
    articles= Article_PW.query.filter_by(author=session["username"])
    exists=articles.count()>0
    if exists:
        say=1
        for article in articles:
            data[say]=([article.title,article.created_date,article.id])
            say+=1
        return render_template("dashboard.html",data=data,exists=exists,say=say)
    else:
        flash("Heç bir məqalə tapılmadı.","info")
        return render_template("dashboard.html",exists=exists)

@app.route("/dashboard/create_article",methods=["GET","POST"])
def create_article():
    form =ArticlesForm(request.form)
    if request.method=="POST" and form.validate():
        title=form.title.data
        content=form.content.data
        user_name=session["username"]
        created_date=datetime.now()

        with app.app_context():
            db.create_all()
        article=Article_PW(title,content,user_name,created_date)
        db.session.add(article)
        db.session.commit()
        flash("Məqalə uğurlu şəkildə qeyd edildi.","success")
        return redirect(url_for("dashboard"))
    else:
        return render_template("create_article.html",form=form)

class Search(Form):
    search=StringField("Axtaris",validators=[validators.Length(min=1,max=150)])
    

@app.route("/articles",methods=['GET','POST'])
@login_required
def articles():
    data=dict()
    articles= Article_PW.query.all()
    
    if request.method=="POST" :
        search= request.form.get("search")
        if search!="":
            articles=Article_PW.query.filter_by(title=search).all()
        
    exists=len(articles)>0
    if exists:
        for article in articles:
            data[article.id]=([article.title,article.created_date,article.author])
        return render_template("articles.html",data=data,exists=exists)
    else:
        flash("Heç bir məqalə tapılmadı.","info")
        return render_template("articles.html",exists=exists)

@app.route("/article/<string:id>")
@login_required
def article(id):
    data=list()
    article= Article_PW.query.filter_by(id=id)
    exists=article.count()>0
    if exists:
        data.append(article[0].title)
        data.append(article[0].created_date)
        data.append(article[0].author)
        data.append(article[0].content)
        return render_template("article.html",data=data)
    else:
        flash("Belə bir məqalə tapılmadı.","warning")
        return redirect(url_for("dashboard"))
  
# meqale silme
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    # article=Article_PW.query.get(id)
    # bu usul daha yaxsidi
    delete_row=Article_PW.query.filter_by(id=id).first()
    if delete_row:
        # birden cox setiri silmek ucun:Article_PW.query.filter_by(id>2).delete()
        db.session.delete(delete_row)
        db.session.commit()
    flash(f"{delete_row} uğurlu şəkildə silindi","success")
    return redirect(url_for("dashboard"))

@app.route("/update/<string:id>",methods=["GET","POST"])
@login_required
def update_article(id):

    
    article=Article_PW.query.get_or_404(id)
    form =ArticlesForm()
    if article:
        form.title.data=article.title
        form.content.data=article.content
    else :
        flash("Bu adda blog tapılmadı.","danger")
        return redirect(url_for("dashboard"))
    if request.method=="POST" and form.validate():
        form=ArticlesForm(request.form)
        title=form.title.data
        content=form.content.data
        article.title=title
        article.content=content
        db.session.commit()
        flash("Məqalə uğurlu şəkildə yeniləndi.","success")
        return redirect(url_for("dashboard"))
    
    return render_template("update_article.html",form=form)


if __name__=="__main__":
    app.run(debug=True)
