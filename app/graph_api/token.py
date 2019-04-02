import graphene
from graphql import GraphQLError
from flask import jsonify, g
from app import db, jwt
from app.graph_api import bp
from ..models import User
from flask_jwt_extended import create_access_token

# jwt.user_identity_loader(User.to_dict)

def verify_password(usern, pwd):
    user = User.query.filter_by(username=usern).first()
    if user is None:
        return False 
    g.current_user = user 
    return user.check_password(pwd)

def basic_auth_error():
    raise GraphQLError("Error 401 user does not exist")

class TokenAuth(graphene.Mutation):
    token = graphene.String()

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, username, password):
        if verify_password(username, password):
            user = g.current_user.to_dict()
            token = create_access_token(identity=user)
            db.session.commit()
            
            return TokenAuth(
                token=token,
            )
        else:
            basic_auth_error()

class Mutation(graphene.ObjectType):
    token_auth = TokenAuth.Field()