from flask import Flask, render_template, session, url_for, redirect, flash
from main_product import your_product  # Import product blueprint
from main_cart import your_cart        # Import cart blueprint
from main_login import your_login      # Import login blueprint
from main_register import your_register # Import register blueprint
import sqlite3

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.template_folder = "templates"
app.static_folder = "static"

# Register blueprints for modularized routes
app.register_blueprint(your_product)
app.register_blueprint(your_cart)
app.register_blueprint(your_login)
app.register_blueprint(your_register)

# Define the home route
@app.route('/')
def index():
    return render_template("index.html", search_text="")

if __name__ == '__main__':
    app.run(debug=True)
