from sqlalchemy.sql import func
from config import db, bcrypt
import re
from flask import session



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

poke_table = db.Table('poke', db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True))

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_who_poke = db.relationship('User', secondary=poke_table)

    #class to validate user registration
    @classmethod
    def register_validation(cls, form):
        errors = []
        if len(form['first_name']) < 1:
            errors.append("Please enter your first name!")
        if len(form['last_name']) < 1:
            errors.append("Please enter your last name!")
        if not EMAIL_REGEX.match(form['email']):
            errors.append("Please enter valid email address!")
        
        #validate if email is already registered
        existing_emails = cls.query.filter_by(email=form['email']).first()
        if existing_emails:
            errors.append("Email is already registered!")

        if len(form['alias']) < 1:
            errors.append("Please enter alias!")
        #validate if alias is already taken
        exisitng_alias = cls.query.filter_by(alias=form['alias']).first()
        if exisitng_alias:
            errors.append("alias is already taken")

        if form['password'] != form['confirm_password']:
            errors.append("Password must be match!")
        if len(form['password']) < 8:
            errors.append("Password must be at least 8 characters!")
        elif re.search('[0-9]', form['password']) is None:
            errors.append("Password required a number!")
        
        return errors

    @classmethod
    def create(cls, form):
        pw_hash = bcrypt.generate_password_hash(form['password'])
        user = cls(
            first_name = form['first_name'],
            last_name = form['last_name'],
            alias = form['alias'],
            email = form['email'],
            pw_hash = pw_hash,
            birthday = form['birthday'],
        )
        db.session.add(user)
        db.session.commit()
        return user.id

    @classmethod
    def login_validation(cls, form):
        user = cls.query.filter_by(email=form['email']).first()
        if user:
            if bcrypt.check_password_hash(user.pw_hash, form['password']):
                return (True, user.id)
        return (False, "Emaill or password is incorrect")
    
    @classmethod
    def edit_user(cls, form):
        edit_user = User.query.get(session['user_id'])
        edit_user.first_name = form['first_name']
        edit_user.last_name = form['last_name']
        edit_user.alias = form['alias']
        edit_user.email = form['email']
        edit_user.password = form['password']
        db.session.commit()
        return edit_user.id
    
    @classmethod
    def get_user(cls, id):
        user = User.query.get(id)
        print(user)
        return user
    
    @classmethod
    def add_poke(cls, id):
        add_poke = cls.query.get(id)
        user = User.query.get(id)
        add_poke.user_who_poke.append(user)
        db.session.commit()

    @classmethod
    def all_user(cls):
        return cls.query.all()

