# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Import scrape_mars
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Set root route
@app.route("/")
def home ():
    collection = mongo.db.collection
    mars = collection.find_one()
    return render_template('index.html', mars=mars)

# Scrape 
@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({},mars_data, upsert=True)
    return redirect('/')
    

if __name__ == "__main__":
    app.run(debug=True)