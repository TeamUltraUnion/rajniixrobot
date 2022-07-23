from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1> Hello I'm 𝕣𝕒𝕛𝕟𝕚𝕚𝕩𝕣𝕠𝕓𝕠𝕥. </h1>"


if __name__ == "__main__":
    app.run(debug=True)
