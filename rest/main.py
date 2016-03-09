# -*- coding: utf-8 -*-

import os
import json
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from flask import Flask, make_response, request
from flask.ext.restplus import Api, Resource, fields

from geodb import init_db, get_all, near

app = Flask(__name__)

@app.before_first_request
def before_first_request():
    init_db()

api = Api(
    app,
    version='1.0',
    title='Memory DB API',
    description='Memory DB API.',
    contact='Nothing to do here!!',
    contact_email='',
    contact_url='',
    default='Memory DB Services',
    default_label='Services'
)

@api.route('/list', methods=['GET'])
class listHandler(Resource):
    def get(self):

        code = 200

        try:

            offices = get_all()

            result = {
                "status": "OK" ,
                "count": len(offices),
                "list": offices
            }

        except BaseException:

            logging.info("Unable to connect to sqllite with provided connection details.")
            code = 500
            result = {
                "message": "sqllite is not working!!!",
                "status": "KO"
            }

        resp = make_response(json.dumps(result), code)
        resp.headers['Content-Type'] = 'application/json'
        return resp


parser = api.parser()
parser.add_argument('lat', type=int, help='Latitude', location='query')
parser.add_argument('lng', type=int, help='Longitude', location='query')
parser.add_argument('radius', type=int, help='Radius', location='query')

@api.route('/near', methods=['GET'])
class nearHandler(Resource):
    @api.doc(parser=parser)
    def get(self):

        code = 200
        lat = request.args.get('lat', 42.3251855)
        lng = request.args.get('lng', 33.453145)
        radius = request.args.get('radius', None)

        if lat and lng and radius:

            try:

                offices = near(lat, lng, radius)

                result = {
                    "status": "OK" ,
                    "count": len(offices),
                    "list": offices,
                    "parameters": {
                        "coords": 'POINT({0} {1})'.format(lat, lng),
                        "radius": radius
                    }
                }

            except BaseException, ex:

                logging.info("Unable to connect to sqllite with provided connection details: %s" % ex)
                code = 500
                result = {
                    "message": "sqllite is not working!!!",
                    "status": "KO"
                }

        else:
            code = 500
            result = {
                "message": "Missing fields!!!",
                "status": "KO"
            }

        resp = make_response(json.dumps(result), code)
        resp.headers['Content-Type'] = 'application/json'
        return resp


if __name__ == '__main__':

    PORT = os.getenv("PORT", 5000)

    logging.info("Starting server!!!")
    app.run(host="0.0.0.0", port=PORT, debug=False)