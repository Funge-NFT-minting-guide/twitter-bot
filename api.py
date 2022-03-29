from pymongo import MongoClient
from flask import Flask, request, abort
from flask_restx import Api, Resource, fields, reqparse

from env.db_config import *


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app=app, version='1.0', title='Twitty-API')


minting = api.model('Minting', {
    '_id': fields.String(readonly=True),
    'id': fields.String(readonly=True),
    'created_at': fields.DateTime(),
    'text': fields.String(),
    'user': fields.String(),
    'uid': fields.String(),
    'profile_image_url': fields.String(),
    'followers': fields.Integer(),
    'url': fields.String(),
    'invalid': fields.Boolean(),
    'outdated': fields.Boolean(),
    'processed': fields.Boolean()
    })


class TwittyDAO:
    def __init__(self):
        self.DB_NAME = 'twitty'
        self.mongo = MongoClient(host='localhost', port=db_config['port'], username=db_config['username'], password=db_config['password'], authSource=self.DB_NAME)[self.DB_NAME]
        

    def find(self, collection, query):
        return self.mongo[collection].find(query)

    def find_sort_by_date(self, collection, order='DESC'):
        pass

    def find_one(self, collection, document):
        return self.mongo[collection].find_one(document)


    def insert_one(self, collection, document):
        return self.mongo[collection].insert_one(document)


DAO = TwittyDAO()

parser = reqparse.RequestParser()
parser.add_argument('order', type=int, default=-1, choices=(-1, 1))
parser.add_argument('offset', type=int, default=0)
parser.add_argument('max_limit', type=int, default=10)


@api.route('/minting/tweets')
class Minting(Resource):
    @api.marshal_list_with(minting)
    def get(self):
        args = parser.parse_args()
        return list(DAO.find('minting_tweets', {'processed': False}).sort('created_at', args['order']).skip(args['offset']).limit(args['max_limit']))

    '''
    @api.expect(minting, validate=True)
    @api.marshal_list_with(minting, code=201)
    def post(self):
        print(api.payload)
    '''

@api.route('/minting/tweets/search/<string:date>')
class MintingSearchData(Resource):
    @api.marshal_list_with(minting)
    def get(self, data):
        ret = DAO.find({'created_at'})



@api.route('/minting/tweets/<string:_id>')
class MintingOne(Resource):
    @api.marshal_with(minting)
    def get(self, _id):
        ret = DAO.find_one('minting_tweets', {'id': _id})
        print(ret)
        return [ret] if ret else abort(404, 'No result found.')
            


if __name__ == '__main__':
    app.run(debug=True)
