#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api, bcrypt
from models import User, Recipe


class Signup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Username and password required"}, 400

        try:
            user = User(username=username)
            user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.id
            return user.to_dict(), 201

        except IntegrityError:
            db.session.rollback()
            return {"error": "Username already taken"}, 422


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        user = User.query.get(user_id)
        return user.to_dict(), 200


class Login(Resource):
    def post(self):
        data = request.get_json()

        user = User.query.filter_by(username=data.get("username")).first()
        if user and bcrypt.check_password_hash(user.password_hash, data.get("password")):
            session["user_id"] = user.id
            return user.to_dict(), 200

        return {"error": "Invalid credentials"}, 401


class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        return {}, 204


class RecipeIndex(Resource):
    def get(self):
        recipes = [recipe.to_dict() for recipe in Recipe.query.all()]
        return recipes, 200

    def post(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        recipe = Recipe(
            title=data.get("title"),
            instructions=data.get("instructions"),
            minutes_to_complete=data.get("minutes_to_complete"),
            user_id=user_id
        )

        db.session.add(recipe)
        db.session.commit()

        return recipe.to_dict(), 201


api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
