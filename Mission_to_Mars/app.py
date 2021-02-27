# Import necessary libraries

from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Setup mongo connection

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Connect to mongo db and collection

db = client.mars_db
mars_info = db.mars_info


# Route to render index.html template using data from Mongo

@app.route("/")
def home():

    # Write a statement that finds all the items in the db and sets it to a variable

    mars_d = mars_info.find_one()

    # Render an index.html template and pass it the data you retrieved from the database

    return render_template("index.html", mars=mars_d)



# Route that will trigger the scrape function

@app.route("/scrape")
def scrape():

    # Run the scrape function

    mars_d = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True

    mars_info.update({}, mars_d, upsert=True)

    # Redirect back to home page
    
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
