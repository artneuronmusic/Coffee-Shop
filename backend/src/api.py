import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
from database.models import setup_db, Drink
from auth.auth import requires_auth
import sys
#from flask_cors import cross_origin
#from sqlalchemy import exc

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def get_drinks(payload):
    print(payload)
    drinks = Drink.query.all()
    if len(drinks) > 0:
        drinks_short_detail = [i.short() for i in drinks]
        return jsonify({
            'status_code': 200,
            "success": True,
            "drinks": drinks_short_detail

        })
    else:
        abort(404)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_explicit(payload):
    
    drinks = Drink.query.all()
  
    if len(drinks) > 0:
        drinks_long_detail = [i.long() for i in drinks]

        return jsonify({
            'status_code': 200,
            "success": True,
            "drinks": drinks_long_detail

        })
    else:
        abort(404)
'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
   
    body = request.get_json()
    print(body)

    try:

        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)
        new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        drink = new_drink.long()
        new_drink.insert()
        new_drink.update()
        return jsonify({
            "success": True,
            "drinks": drink

        })

    except:
        abort(400)

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:update-drinks')
def update_specific_drink(payload, drink_id):
    specific_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if specific_drink is None:
        abort(404)
    else:
        body = request.get_json()
        try:
            new_title = body.get('title')
            new_recipe = body.get('recipe')
            specific_drink.title = new_title
            specific_drink.recipe = json.dumps(new_recipe)
            specific_drink.update()
            drink = specific_drink.long()
            return jsonify({
                "status_code": 200,
                "success": True,
                "drinks": drink
            })
        except:
            abort(400)
       

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):

    specific_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if specific_drink is None:
        abort(404)

    else:
        specific_drink.delete()
        return jsonify({
            "status_code": 200,
            "success": True,
            "delete_drink": drink_id

        })


@ app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404,
                 "message": "resource not found"}),
        404,
    )


@ app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422,
                 "message": "unprocessable"}),
        422,
    )


@ app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400


@ app.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify({"success": False, "error": 405,
                 "message": "method not allowed"}),
        405,
    )


@ app.errorhandler(500)
def server_error(error):

    return (
        jsonify({"success": False, "error": 500,
                 "message": "Internal Server Error"}),
        500,
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
