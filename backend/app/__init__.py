
from flask import Flask, send_from_directory
import os

def create_app():
    app = Flask(__name__)

    # Example default route
    @app.route("/")
    def home():
        return {"status": "Backend is running!"}

    # Handle favicon requests
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    # TODO: register blueprints here
    # from .auth.routes import auth_bp
    # app.register_blueprint(auth_bp)

    return app
