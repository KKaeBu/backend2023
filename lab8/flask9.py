from flask import Flask, request, render_template


app = Flask(__name__)


@app.route("/")
def index():
    name = request.args.get("name", default=None)
    return render_template("hello.html", name=name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=19140)
