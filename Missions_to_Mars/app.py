from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars_data = mongo.db.mars_data

# Route to index.html template
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_doc = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_doc=mars_doc)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    scraped_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, scraped_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)