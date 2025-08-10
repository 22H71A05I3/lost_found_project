# Application entrypoint: import create_app from app, call init_db(), run Flask dev server when __main__
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
