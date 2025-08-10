
def init_notifications(app):
	from .routes import notifications_bp
	app.register_blueprint(notifications_bp, url_prefix="/notifications")

