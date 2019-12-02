from flask import request
from flask_restful import Resource
from Model import db, Category, CategorySchema
from marshmallow import ValidationError

categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()

class CategoryResource(Resource):
    def get(self):
        categories = Category.query.all()

        categories = categories_schema.dump(categories)
        return {'status': 'success', 'data': categories}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data:
               return {'message': 'No input data provided'}, 400
        
        errors = False

        # Validate and deserialize input
        try:
            category_schema.load(json_data)
        except ValidationError as error:
            print("ERROR: package.json is invalid")
            print(error.messages)
            # sys.exit(1)
            errors = error.messages

        # data, errors = category_schema.load(json_data)

        # print(data)
        # print(errors)

        if errors:
            return errors, 422

        category = Category.query.filter_by(name=json_data['name']).first()
        
        if category:
            return {'message': 'Category already exists'}, 400
        
        category = Category(
            name=json_data['name']
            )

        db.session.add(category)
        db.session.commit()

        result = category_schema.dump(category)

        return { "status": 'success', 'data': result }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return errors, 422
        category = Category.query.filter_by(id=data['id']).first()
        if not category:
            return {'message': 'Category does not exist'}, 400
        category.name = data['name']
        db.session.commit()

        result = category_schema.dump(category).data

        return { "status": 'success', 'data': result }, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return errors, 422
        category = Category.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = category_schema.dump(category).data

        return { "status": 'success', 'data': result}, 204