from flask import Flask, render_template
from app.router import router

app = Flask(__name__)
app.register_blueprint(router)

@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404
