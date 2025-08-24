from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    image_url = db.Column(db.String)

    recipes = db.relationship("Recipe", back_populates="user")

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def authenticate(self, password):
        return self.check_password(password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "image_url": self.image_url
        }


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    minutes_to_complete = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship("User", back_populates="recipes")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.instructions and len(self.instructions) < 50:
            raise ValueError("Instructions must be at least 50 characters long.")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "instructions": self.instructions,
            "minutes_to_complete": self.minutes_to_complete,
            "user_id": self.user_id
        }
