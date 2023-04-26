from flask import Flask, Response, flash, jsonify ,render_template, session,redirect,url_for
from flask import request
import psycopg2
import json
import random 

app = Flask(__name__)
app.secret_key = 'somesecretkey'
user = {}

def randomIDcreator(initstring):
    random_number = random.randint(0, 9999991)
    return initstring + str(random_number)


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



@app.route('/home')
def Home():
    cur = conn.cursor()
    cur.execute('''SELECT
                        post.postid,
                        post.postedby,
                        COUNT(person_likes_post.kerberosid) AS like_count,
                        post.caption,
                        (select
                             COUNT(*) 
                        FROM 
                        person_likes_post 
                        WHERE post.postid = person_likes_post.postid 
                        AND person_likes_post.kerberosID = %s) AS user_like_count
                    FROM
                        post
                        LEFT JOIN person_likes_post ON post.postid = person_likes_post.postid
                        LEFT JOIN person ON person_likes_post.kerberosid = person.kerberosid
                    WHERE
                        post.belongstogroups IS NULL
                        AND post.postedby = %s
                    GROUP BY
                        post.postid;
''', ("ee1210653","ee1210653",))
    images = cur.fetchall()
    
    
    cur.close()
    return render_template('home.html', images=images)


@app.route('/home/<image_id>', methods=['GET', 'POST'])
def get_image(image_id):
    cur = conn.cursor()
    cur.execute("SELECT image  FROM post WHERE postid = %s", (image_id,))

    image_data = cur.fetchone()[0]
       
    cur.close()
    return Response(image_data, content_type='image/jpeg')

@app.route('/home/likes/<image_id>', methods=['POST'])
def get_likes(image_id):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM person_likes_post WHERE kerberosid = %s AND postid = %s", ("ee1210653", image_id))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("INSERT INTO person_likes_post (kerberosid, postid) VALUES (%s, %s)", ("ee1210653", image_id))
    else:
        cur.execute("DELETE FROM person_likes_post WHERE kerberosid = %s AND postid = %s", ("ee1210653", image_id))
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM person_likes_post WHERE postid = %s", (image_id,))
    like_count = cur.fetchone()[0]
    cur.close()

    return jsonify({'like_count': like_count})

@app.route('/home/comments/<image_id>', methods=['GET', 'POST'])
def get_comments(image_id):
    if request.method == 'POST' and 'comment' in request.form:
        id = randomIDcreator("C")
        exist = True 
        while exist:  
            cur = conn.cursor()
            cur.execute("select count(*) from comments where commentid = %s;", (id, ))
            num = cur.fetchone()
            if num[0] == 0:
                exist = False  
            else :
                id = randomIDcreator("C")
        comment = request.form['comment']
        cur = conn.cursor()
        cur.execute("INSERT INTO comments (commentid, content, creatorpersonid, parentpostid) VALUES (%s, %s, %s, %s)", ( id , comment, session['user_id'], image_id))
        # conn.commit()

    # Retrieve all comments for the given image ID
    cur = conn.cursor()
    cur.execute("SELECT content, creatorpersonid FROM comments WHERE parentpostid = %s", (image_id,))
    comments = cur.fetchall()

    return render_template('comments.html', comments=comments)

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
def Chats():
    with open("static/json/groups.json", "r") as f:
        groups = json.load(f)
    return render_template("chats.html", groups=groups)


@app.route("/groups")
def Groups():
    with open("static/json/groups.json", "r") as f:
        groups = json.load(f)
    return render_template("groups.html", groups=groups)


@app.route("/navbar")
def Navbar():
    return render_template("index.html" )

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == '__main__':
    
    app.debug = True
    app.run(debug=True)
