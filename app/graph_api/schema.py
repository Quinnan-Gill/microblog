import graphene 
# from flask_graphql_auth import (AuthInfoField, GraphQLAuth, get_jwt_identity,
#                                 get_raw_jwt, create_access_token, create_refresh_token,
#                                 query_jwt_required, mutation_jwt_required,
#                                 mutation_jwt_refresh_token_required)
from app.graph_api import user_schema, token
from flask_jwt_extended import create_access_token

class Query(user_schema.Query, graphene.ObjectType):
    pass

class Mutation(user_schema.Mutation, token.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)