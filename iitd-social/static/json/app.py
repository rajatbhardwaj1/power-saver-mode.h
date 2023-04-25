from flask import Flask, flash ,render_template, session,redirect,url_for
from flask import request
import psycopg2
import json

app = Flask(__name__)
app.secret_key = 'somesecretkey'
user = {}

conn = psycopg2.connect(
    database = 'group_19',
    host = '10.17.6.95',
    port = '5432',
    user = 'group_19',
    password = 'B0jzmL6aEhxI21'
)
curr = conn.cursor()
#cur.execute("SELECT image FROM post WHERE postid = %s;", ("P0000040",))


@app.route("/create-account", methods = ['GET' , "POST"])
def CreateAccount():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        gender = request.form['gender']
        hostel = request.form['hostel']
        
        curr.execute("select count(*) from person where kerberosid = %s;" , (username, ))
        count = curr.fetchall()

        if count[0][0] > 0:
            flash("user already exists" , 'warning')
            print("user already exists")
            return redirect(url_for('CreateAccount'))
        elif len(username) != 9:
            flash("Enter 9 character kerberos ID" , 'warning')
            return redirect(url_for('CreateAccount'))
        elif len(password) < 8:
            flash("Enter atleast 8 characters for password" , 'warning')
            return redirect(url_for('CreateAccount'))
        elif len(name) < 1:
            flash("Please enter your name" , 'warning')
            return redirect(url_for('CreateAccount'))
        else :
            session['user_id'] = username 
            curr.execute("insert into person values(%s,%s,%s%s);", (username, name ,hostel ,gender,))
            conn.commit()
            return redirect(url_for('Home') )
    return render_template("create-account.html")


@app.route("/login" , methods = ['POST', 'GET'])
def Login():
    if request.method != 'POST':
        return render_template("login.html")
    session.pop('user_id' , None)
    username = request.form['username']
    password = request.form['password']
    print(type(username))
    curr.execute("SELECT count(*) FROM person WHERE kerberosid = %s;", (username,))
    count = curr.fetchall()
    print(count)
    if count[0][0] != 1:
        flash("Login Failed!",'warning')
        return redirect(url_for('Login') )
    session['user_id'] = username
    flash('You have successfully logged in', 'success')
    return redirect(url_for('Home') )


@app.route("/groups", methods = ['POST'])
def Groups():
    render_template("groups.html")


@app.route("/home", methods = ['GET' , "POST"])
def Home():
    return render_template("home.html",user=session['user_id'])


@app.route("/chat", methods = ['GET' , 'POST'])
def Chat():
    messages = [
        {'message': 'Hello!', 'by': 'sender'},
        {'message': 'Hi there!', 'by': 'receiver'},
        {'message': 'How are you?', 'by': 'sender'},
        {'message': 'I am good, thanks.', 'by': 'receiver'},
    ]
    name = 'Rajat'
    newMessage = ''
    return render_template("chat.html", messages=messages, name=name, newMessage=newMessage)




@app.route("/chats")
def index():
    with open("static/json/groups.json", "r") as f:
        groups = json.load(f)
    return render_template("chats.html", groups=groups)


@app.route("/navbar")
def Navbar():
    return render_template("index.html" )

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == '__main__':
    
    app.debug = True
    app.run(debug=True)
