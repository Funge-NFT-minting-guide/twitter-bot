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
    'url': fields.String()
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


@api.route('/minting')
class Minting(Resource):
    @api.marshal_list_with(minting)
    def get(self):
        return list(DAO.find('minting', {}))

    '''
    @api.expect(minting, validate=True)
    @api.marshal_list_with(minting, code=201)
    def post(self):
        print(api.payload)
    '''

@api.route('/minting/search/<string:date>')
class MintingSearchData(Resource):
    @api.marshal_list_with(minting)
    def get(self, data):
        ret = DAO.find({'created_at'})



@api.route('/minting/<string:_id>')
class MintingOne(Resource):
    @api.marshal_with(minting)
    def get(self, _id):
        ret = DAO.find_one('minting', {'id': _id})
        return ret if ret else abort(404, 'No result found.')
            


if __name__ == '__main__':
    app.run(debug=True)
