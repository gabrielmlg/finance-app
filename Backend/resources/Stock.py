from flask_restful import Resource
from flask_restful import request
from Model import db, Stock, StockSchema
from marshmallow import ValidationError

import requests
import json
import boto3
from botocore.exceptions import NoCredentialsError

stocks_schema = StockSchema(many=True)
stock_schema = StockSchema()

ACCESS_KEY = 'XXX'
SECRET_KEY = 'XXX'

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

class StockResouce(Resource):
    def get(self):
        return {'stocks': [
            {'id': '1', 
            'symbol': 'MGLU3.SA'}
        ]}

    def put(self):
        json_data = request.get_json(force=True)
        errors = False
        # text_response = ''

        if not json_data:
            return {'message': 'No input data provided.'}, 400

        try:
            # ACCESS_KEY = json_data['ACCESS_KEY']
            # SECRET_KEY = json_data['SECRET_KEY']

            url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts"
            symbol_string = 'MGLU3.SA'
            querystring = {"region":"Brasil","lang":"en","symbol":symbol_string,"interval":"1d","range":"max"}
            headers = {
                'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
                'x-rapidapi-key': "XXX"
                }

            response = requests.request("GET", url, headers=headers, params=querystring)
            text_response = json.loads(response.text)

            with open('ibov-MGLU3_max.json', 'w') as json_file:
                json.dump(text_response, json_file)

            uploaded = upload_to_aws('ibov-MGLU3_max.json', 'ibov-raw', 'ibov-MGLU3_max_v2.json')

        except Exception as e:
            print(e)
            errors = True

        if errors:
            return errors, 422

        return {'status': 'success', 'data': uploaded}, 204

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided.'}, 400

        errors = False

        try:
            stock_schema.load(json_data)
        except ValidationError as error:
            print(error.messages)
            errors = True

        if errors:
            return errors, 442

        stock = Stock.query.filter_by(symbol=json_data['symbol']).first()

        if stock:
            return {'message': 'Stock already exists'}, 400

        stock = Stock(symbol=json_data['symbol'])
        db.session.add(stock)
        db.session.commit()

        result = stock_schema.dump(stock)

        return { "status": 'success', 'data': result }, 201