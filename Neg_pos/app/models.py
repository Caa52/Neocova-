from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # __bind_key__= 'users'
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    City = db.Column(db.String(60), nullable=False)
    State = db.Column(db.String(60), nullable=False)
    Zip = db.Column(db.String(60), nullable=False)
    Company = db.Column(db.String(60), nullable=False)
    Department = db.Column(db.String(60), nullable=False)
    Title = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    history = db.relationship('History', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}','{self.City}','{self.State}','{self.Zip}','{self.Company}','{self.Department}','{self.Title}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class History(db.Model):
    # __bind_key__= 'history'
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    # user = db.Column(db.String(20), nullable=False)
    
    roeinjr = db.Column(db.String(20), nullable=False)
    noijy = db.Column(db.String(20), nullable=False)
    asset = db.Column(db.String(20), nullable=False)
    RBCT1J= db.Column(db.String(20), nullable=False)
    core_deposit= db.Column(db.String(20), nullable=False)
    lnlsntv= db.Column(db.String(20), nullable=False)
    County_GDP_Percent= db.Column(db.String(20), nullable=False)
    PC_Labor_Force= db.Column(db.String(20), nullable=False)
    PC_Unemployed = db.Column(db.String(20), nullable=False)
    GR_Total_Population = db.Column(db.String(20), nullable=False)
    output = db.Column(db.String(20), nullable=False)

    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# What is this __repr__ for?? For retrieval???
    def __repr__(self):
        return f"History('{self.username}','{self.roeinjr}','{self.noijy}','{self.asset}','{self.RBCT1J}','{self.core_deposit}','{self.lnlsntv}','{self.County_GDP_Percent}','{self.PC_Labor_Force}','{self.PC_Unemployed}','{self.GR_Total_Population}',{self.output}','{self.time}')"