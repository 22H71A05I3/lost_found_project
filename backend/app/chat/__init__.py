def init_chat(app):
	from .routes import chat_bp
	app.register_blueprint(chat_bp, url_prefix="/chat")
