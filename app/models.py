from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from app import db
from app import ma

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    title_alt = db.Column(db.String(120))
    type = db.Column(db.String(80), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    season = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False, default='Base Image')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False, default=False)
    episodes = db.Column(db.ARRAY(db.Integer))

    def __repr__(self):
        return 'Anime {}, {}'.format(self.title, self.title_alt)

    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()

# Schemas
class AnimeSchema(ma.ModelSchema):
    class Meta:
        model = Anime