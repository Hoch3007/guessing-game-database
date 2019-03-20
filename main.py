from flask import Flask, render_template, url_for, request, redirect, flash, make_response
from random import randint
import pymongo
#from flask_pymongo import PyMongo


# App und Einstellungen

app = Flask(__name__)

app.secret_key = '6ca97bc342cdbecabbadb5c47b006ef4'
#app.config['MONGO_URI']='mongodb+srv://SmartNinjaTest2019:jxqlkv5xQInb38V8@cluster0-l2yzh.azure.mongodb.net/test?retryWrites=true'

# Datenbank
client = pymongo.MongoClient("mongodb+srv://SmartNinjaTest2019:jxqlkv5xQInb38V8@cluster0-l2yzh.azure.mongodb.net/test?retryWrites=true")
db = client['guessing_game']
users = db.users

# Klassen für die Datenbank
# werden nicht benötigt????

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/new_game", methods=["POST", "GET"])
def new_game():
    number_guess = request.form.get("guess")
    user_name = request.form.get("user_name")

    if request.method == "POST":

        user = users.find_one({'user_name': user_name})

        if user is None:
            new_user = {'user_name': user_name, 'secret_number':str(randint(0,30))}
            users.insert_one(new_user)

        user = users.find_one({'user_name': user_name})
        secret = user['secret_number']

        if number_guess == secret:
            flash("Great. That's correct. The number was " + str(secret) +
                  ". If would like to guess another number just guess again.", "success")
            users.update_one({'user_name':user['user_name']},{'$set':{"secret_number":randint(0,30)}})

        elif number_guess>secret:
            flash("Sorry, that's too high.", "danger")
        else:
            flash("Sorry, that's too low.", "danger")

        return redirect("/new_game")

    return render_template('new_game.html')


if __name__ == '__main__':
    app.run(debug=True)