from flask import Flask
from flask import jsonify, request
from flask_pymongo import PyMongo

app= Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://cst_user:mcit123@cluster0.vo3fn.mongodb.net/jasmeet?retryWrites=true&w=majority"
mongo_client = PyMongo(app)

db = mongo_client.db

@app.route("/book")
def add_one_book():
    db.books.insert_one({
	"id": 1,
    "author": "Chinua Achebe",
    "country": "Nigeria",
    "imageLink": "images/things-fall-apart.jpg",
    "language": "English",
    "link": "https://en.wikipedia.org/wiki/Things_Fall_Apart\n",
    "pages": 209,
    "title": "Things Fall Apart",
    "year": 1958
    })
    return jsonify(message="sucess")

@app.route("/books")
def add_many_books():
    db.books.insert_many([
    {
	"id": 1,
    "author": "Chinua Achebe",
    "country": "Nigeria",
    "imageLink": "images/things-fall-apart.jpg",
    "language": "English",
    "link": "https://en.wikipedia.org/wiki/Things_Fall_Apart\n",
    "pages": 209,
    "title": "Things Fall Apart",
    "year": 1958
    },
    {
	"id": 2,  
    "author": "Hans Christian Andersen",
    "country": "Denmark",
    "imageLink": "images/fairy-tales.jpg",
    "language": "Danish",
    "link": "https://en.wikipedia.org/wiki/Fairy_Tales_Told_for_Children._First_Collection.\n",
    "pages": 784,
    "title": "Fairy tales",
    "year": 1836
    },
    {
	"id": 3,  
    "author": "Dante Alighieri",
    "country": "Italy",
    "imageLink": "images/the-divine-comedy.jpg",
    "language": "Italian",
    "link": "https://en.wikipedia.org/wiki/Divine_Comedy\n",
    "pages": 928,
    "title": "The Divine Comedy",
    "year": 1315
    },
    {
	"id": 4,  
    "author": "Unknown",
    "country": "Sumer and Akkadian Empire",
    "imageLink": "images/the-epic-of-gilgamesh.jpg",
    "language": "Akkadian",
    "link": "https://en.wikipedia.org/wiki/Epic_of_Gilgamesh\n",
    "pages": 160,
    "title": "The Epic Of Gilgamesh",
    "year": -1700
    },
    {
	"id": 5,  
    "author": "Unknown",
    "country": "Achaemenid Empire",
    "imageLink": "images/the-book-of-job.jpg",
    "language": "Hebrew",
    "link": "https://en.wikipedia.org/wiki/Book_of_Job\n",
    "pages": 176,
    "title": "The Book Of Job",
    "year": -600
    },
    {
	"id": 6,  
    "author": "Unknown",
    "country": "India/Iran/Iraq/Egypt/Tajikistan",
    "imageLink": "images/one-thousand-and-one-nights.jpg",
    "language": "Arabic",
    "link": "https://en.wikipedia.org/wiki/One_Thousand_and_One_Nights\n",
    "pages": 288,
    "title": "One Thousand and One Nights",
    "year": 1200
    },
    ])
    return jsonify(message="Books Added SuccessFully")

@app.route("/books_list")
def get_books():
    books = db.books.find()
    response = []
    for book in books:
        book['_id'] = str(book['_id'])
        response.append(book)
    return jsonify(response)

@app.route("/update_book",methods=['GET'])
def update_book():
    id = int(request.args['id'])
    book_response = db.books.update_one({'id' : id},{"$set" : {'author':'Jasmeet'}})
    return book_response.raw_result

@app.route("/delete_book",methods=['DELETE'])
def delete_book():
    id = int(request.args['id'])
    book_response = db.books.delete_one({'id':id})
    return jsonify(message="Deleted Sccuessfully")

app.run()