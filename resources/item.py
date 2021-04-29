from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required = True,
        help="This field cannot be left blank!"
        )

    parser.add_argument("store_id",
        type=int,
        required = True,
        help="Every item needs a store id"
        )
    

    @jwt_required()  # JWT authentication is required for this function (GET ITEM)
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()        # If item is not None then return item
        return {"message": "Item not found"}, 404   # else return message
        

    def post(self,name):
       
        if ItemModel.find_by_name(name):     # Checking that the item doesn't already exist.
            
            return {"Message":"An item with name '{}' already exists.".format(name)}, 400

        #First filter and work out if we are going to do anything, then load up the data to use... hence data variable is on next line.

        data = Item.parser.parse_args()

        item = ItemModel(name, data["price"], data["store_id"])

        try:                    # try to run code (insert into db) if an exception occurs return a certain message. 
            item.save_to_db()
        except:
            return {"message":"An error occurred when inserting into database"}, 500    # 500 = internal server error

        return item.json(), 201  #201 is json status for "created"


    def delete(self,name):
         
        item = ItemModel.find_by_name(name)

        if item is not None:
            item.delete_from_db()

        return {"message":"item deleted"}


    def put(self, name):
      
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        

        if item == None:
            item = ItemModel(name, data["price"], data["store_id"])
        
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        
        item.save_to_db()

            

        return item.json()
 


class ItemList(Resource):
    def get(self):

        item_list =[]
        for item in ItemModel.query.all():

            item_list.append(item.json())
        
        return {"items" : item_list}
        
        # the above can be written in one line:

        #return {"items": [item.json() for item in ItemModel.query.all()]}
