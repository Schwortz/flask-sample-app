"""Entry point: python run.py"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=str(app.config["HOST"]), port=int(app.config["PORT"]))
