import app
from flask import Blueprint
from flask_graphql import GraphQLView
from flask_jwt_extended import JWTManager
from app import db
from flask import current_app

bp = Blueprint('graph_api', __name__)

from app.graph_api.schema import schema

def graphql_view():
    view = GraphQLView.as_view('graphql', schema=schema, context={'session': db.session},
                                graphiql=True)
    return view

bp.add_url_rule(
        '/',
        view_func=graphql_view()
    )   