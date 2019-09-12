import sys
import graphene
from graphene import ObjectType, String, Schema, relay 
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField 
from graphql import GraphQLError
from ..models import User, Post, Message
from app import db
# from app.graph_api.auth import token_auth
from app.graph_api.errors import bad_request
from flask_jwt_extended import current_user, jwt_required

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        # exclude_fields = ('id', 'username', 'email')
        only_fields = ('id','username','email','posts','about_me','followed', 'followers')

class PostType(SQLAlchemyObjectType):
    class Meta:
        model = Post
class MessageType(SQLAlchemyObjectType):
    class Meta:
        model = Message
class Query(graphene.ObjectType):
    users = graphene.List(
        UserType,
        id=graphene.Int(),
        first=graphene.Int(),
        skip=graphene.Int(),    
    )
    print("size of UserType:", sys.getsizeof(UserType))
    print("size of users:", sys.getsizeof(users))
    print("size of User:", sys.getsizeof(User))

    @jwt_required
    def resolve_users(self, info, id=None, first=None, skip=None, **kwargs):
        if id:
            qs = User.query.filter_by(id=id)
            return qs
        else:
            qs = User.query.all()
        if skip:
            qs =  qs[skip:]
        if first:
            qs = qs[:first]
        return qs
        

class CreateUser(graphene.Mutation):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()
    aboutMe = graphene.String()

    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()
        aboutMe = graphene.String()

    def mutate(self, info, username=None, email=None, password=None, aboutMe=None):
        if not username and not password and not email:
            return GraphQLError('must include username, email and password')
        if User.query.filter_by(username=username).first():
            return GraphQLError('please use a different username')
        if User.query.filter_by(email=email).first():
            return GraphQLError('please use a different email address')
        user = User()
        data = {
            'username': username,
            'email': email,
            'password': password,
            'aboutMe': aboutMe,
        }
        user.from_dict(data, new_user=True)
        db.session.add(user)
        db.session.commit()

        return CreateUser(
            id=user.id,
            username=user.username,
            email=user.email,
            aboutMe=user.about_me,
        )

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
