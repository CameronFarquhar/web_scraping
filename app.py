from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars_1 import scrape_mars_data

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars_data = mongo.db.mars

    # Run the scrape function
    mars_data_scrape = scrape_mars_data()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars_data_scrape, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
