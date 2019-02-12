from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    # preload from module, then override from file if it exists
    app.config.from_object('config.DevelopmentConfig')
    app.config.from_pyfile('config.py', silent=True)
    # app.config.from_envvar()

    if test_config is not None:
        app.config.from_mapping(test_config)
    
    db.init_app(app)
    ma.init_app(app)

    migrate = Migrate(app, db)

    from app.resources.hello import HelloWorld
    api.add_resource(HelloWorld, '/')

    from app.resources.anime import Anime, AnimeList
    api.add_resource(Anime, '/api/anime/<int:id>')
    api.add_resource(AnimeList, '/api/anime')

    from app.resources.query import QueryQL
    api.add_resource(QueryQL, '/api/queryme')

    return app