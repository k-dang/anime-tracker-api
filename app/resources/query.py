from flask_restful import Resource

import requests

class QueryQL(Resource):
    def get(self):
        query = '''
query ($year: Int, $type: MediaType, $format: MediaFormat) {
    Page(perPage: 10) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
        }
        media(seasonYear:$year, season:FALL, type:$type, format:$format, sort:POPULARITY_DESC) {
            title {
                romaji
                english
            }
            format
            type
            season
            episodes
            duration
            coverImage {
                medium
            }
            startDate {
                year
                month
                day
            }
            airingSchedule(perPage: 50) {
                nodes {
                    airingAt
                    episode
                }
            }
        }
    }
}
        '''

        variables = {
            'year': 2018,
            'type': 'ANIME',
            'format': 'TV',
        }
        
        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})
        aljson = response.json()

        return aljson['data']['Page']['media']