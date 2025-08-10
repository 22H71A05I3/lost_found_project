# Initialize the reports module and register routes for user-generated content flagging and moderation.

def init_reports(app):
    from .routes import reports_bp
    app.register_blueprint(reports_bp, url_prefix="/reports")
