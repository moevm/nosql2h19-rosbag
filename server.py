from flask import Flask, render_template, jsonify, make_response
from pymongo import MongoClient
from adapter import getDataFromBag

client = MongoClient()
app = Flask(__name__)

# print(getDataFromBag('bags/Double.bag'))

@app.route("/")
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/addData', methods=['POST'])
def addData():
    db = client.test_database
    collection = db.test_collection
    newDocument = {"author": "Maxim",
                   "text": "This text was added on site!",
                   "tags": ["mongodb", "python", "pymongo", "flask"],
    }
    posts = db.posts
    post_id = posts.insert_one(newDocument).inserted_id
    print(post_id)

    ans = {'status': True}
    print(jsonify(ans))
    return make_response(jsonify(ans), 200)


if __name__ == '__main__':
    app.run(debug=True)