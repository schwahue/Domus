from flask import Flask, render_template
from app.router import router

app = Flask(__name__)
app.register_blueprint(router)

@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def internal_server_errer(e):
    return render_template("errors/500.html"), 500

#TODO: refactor to factory pattern