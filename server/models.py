from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    _password_hash = db.Column(db.String, nullable=False)

    
    recipes = db.relationship('Recipe', back_populates='user', cascade='all, delete-orphan')

    
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

   
    user = db.relationship('User', back_populates='recipes')
