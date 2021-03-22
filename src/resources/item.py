from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from src.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field can"t be left blank')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'an item with {} already exists'.format(name)}, 400
        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'], request_data['store_id'])
        try:
            item.save_to_db()
        except Exception as e:
            return {"message": "an error occurred inserting the item."}, 500  # internal server error
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            try:
                item = ItemModel(name, data['price'], data['store_id'])
            except Exception as e:
                return {"message": "an error occurred inserting the item"}, 500
        else:
            try:
                item.price = data['price']
            except Exception as e:
                return {"message": "an error occurred updating the item"}, 500
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
