from config import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(
        db.String,
        default="https://cdn.vox-cdn.com/thumbor/I3GEucLDPT6sRdISXmY_Yh8IzDw=/0x0:1920x1080/1820x1024/filters:focal(960x540:961x541)/cdn.vox-cdn.com/uploads/chorus_asset/file/23952901/1240183845.jpg"
    )
    bio = db.Column(db.String, default="")

    recipes = db.relationship("Recipe", backref="user", lazy=True, cascade="all, delete-orphan")

    @property
    def password_hash(self):
        raise AttributeError("Password is write-only")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "image_url": self.image_url,
            "bio": self.bio
        }


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "instructions": self.instructions,
            "minutes_to_complete": self.minutes_to_complete,
            "user": self.user.to_dict() if self.user else None
        }
