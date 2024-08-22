from app import app

"""
Pages
"""


@app.route("/")
def home():
    return "Hello world!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
