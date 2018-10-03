from flask import jsonify, request
from flask_restful import Resource
from app.models import AnimeSchema, Anime as AnimeModel
from app import db
from datetime import datetime

anime_schema = AnimeSchema(many=True)

# /anime/id
class Anime(Resource):
    def get(self, id):
        anime = AnimeModel.query.get(id)
        return anime_schema.jsonify(anime, many=False)

    def put(self, id):
        anime = AnimeModel.query.get(id)
        data = request.get_json()
        errors = {}
        for field in data:
            if getattr(anime, field):
                setattr(anime, field, data[field])
            else:
                errors[field] = "field not in model"
        if errors:
            return jsonify({'errors':errors})
        db.session.commit()
        return anime_schema.jsonify(anime, many=False)

# /anime
class AnimeList(Resource):
    def get(self):
        query_params = request.args
        page = query_params.get('page', 1)
        animes = AnimeModel.query.filter_by(season=query_params.get('season')).paginate(page=page, per_page=10).items
        result = anime_schema.dump(animes)
        for r in result.data:
            r['episodes'] = [datetime.fromtimestamp(ep) for ep in r['episodes']]
        return jsonify(result.data)

    def post(self):
        anime_list = request.get_json()
        anime_objs = []
        try:
            for i in anime_list:
                ep_epochs = [asn['airingAt'] for asn in i['airingSchedule']['nodes']]
                episode_nodes = [datetime.fromtimestamp(ep) for ep in ep_epochs]
                anime_objs.append(AnimeModel(
                    title=i['title']['english'],
                    title_alt=i['title']['romaji'],
                    type=i.get('type', 'ANIME'),
                    start_date=episode_nodes[0],
                    end_date=episode_nodes[-1],
                    season=i['season'],
                    description='desc',
                    image_url=i['coverImage']['medium'],
                    updated_at=datetime.now(),
                    active=i.get('active', True),
                    episodes=ep_epochs
                ))
            db.session.add_all(anime_objs)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'failed',
                'message': 'Failed to add any anime',
                'exception': str(e)
            }

        return {
            'status': 'success',
            'data': {
                'anime': anime_list
            }
        }