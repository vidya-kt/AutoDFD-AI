from flask import Flask
from config import Config

from routes.dfd_routes import dfd_bp

app = Flask(__name__)

app.config.from_object(Config)

# Register Blueprint
app.register_blueprint(dfd_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)