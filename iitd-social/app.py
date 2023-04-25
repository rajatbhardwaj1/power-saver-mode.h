from flask import Flask ,render_template, session,redirect,url_for
from flask import request

app = Flask(__name__)

user = {}

# @app.route("/home")
@app.route("/create-account", methods = ['GET' , "POST"])
def CreateAccount():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        user['username'] = username
        # session['username'] = username
        return redirect(url_for('Home') )
    return render_template("create-account.html")

@app.route("/login" , methods = ['POST'])
def Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user['username'] = username
        # session['username'] = username
        return redirect(url_for('Home') )
    return render_template("create-account.html")


@app.route("/groups", methods = ['POST'])
def Groups():
    render_template("groups.html")


@app.route("/home", methods = ['GET' , "POST"])
def Home():
    return render_template("home.html",user=user['username'])


if __name__ == '__main__':
    app.run(debug=True)
