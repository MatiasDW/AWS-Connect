import os
from flask import Flask
from dotenv import load_dotenv
from app.routes import define_routes, update_contact_flow  #Important to define this function in routes.py 

load_dotenv()  #loading Variables enviorment 

app = Flask(__name__)
define_routes(app)  # Register your lines in the Flask app

if __name__ == "__main__":
    app.run(debug=True)
