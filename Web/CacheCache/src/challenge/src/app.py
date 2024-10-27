from flask import Flask, request, Response
app = Flask(__name__)

@app.get("/")
def index():
    res = Response(request.cookies.get("FLAG") if request.cookies.get("FLAG") else "Not authenticated!")
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

app.run("0.0.0.0", 8000)
