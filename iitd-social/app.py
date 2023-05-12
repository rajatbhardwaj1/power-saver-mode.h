import datetime
from flask import Flask, Response, flash, jsonify ,render_template, session,redirect,url_for
from flask import request
import psycopg2
import random 
from PIL import Image
from io import BytesIO
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
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


@app.route('/add_friend/<kerberosid>', methods=['POST', 'GET'])
def add_friend(kerberosid):
    cur = conn.cursor()
    conn.rollback()
    # if()
    print(len(session['user_id']))
    print(len(kerberosid))
    a = kerberosid
    b = session['user_id']
    if a > b:
        temp = a 
        a = b 
        b = temp
    print(kerberosid , session['user_id'])
    # cur.execute("INSERT INTO Friends values(%s, %s)", (a ,b))
    # cur.execute("INSERT INTO Friends values(%s, %s)", (kerberosid,session['user_id']))
    cur.execute("INSERT INTO Friends values(%s, %s)", (session['user_id'], kerberosid))
    conn.commit()

    cur.close()

    return redirect(url_for('FriendsProfile',kerberosid = kerberosid))

@app.route('/remove_friend/<kerberosid>', methods=['POST', 'GET'])
def remove_friend(kerberosid):
    cur = conn.cursor()
    conn.rollback()
    cur.execute("DELETE from Friends where (person1 = %s and person2 = %s) or (person2 = %s and person1 = %s)", (session['user_id'], kerberosid,session['user_id'], kerberosid))
    conn.commit()

    cur.close()

    return redirect(url_for('FriendsProfile',kerberosid = kerberosid))


@app.route("/group_chat/<group_id>", methods = ['GET' , 'POST'])
def group_chat(group_id):
    cur = conn.cursor()

    conn.rollback()
    current = int(request.args.get('current', 3))  # Get the 'current' parameter from the request or default to 3
    limit = current + 3  # Limit the number of images fetched

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
                        post.belongstogroups = %s
                    GROUP BY
                        post.postid
                    order by
                        post.postid;
''', (session['user_id'],group_id,))
    images = cur.fetchall()
        
    
    cur.close()
    return render_template('group_chat.html', images=images, group_id = group_id,current = current)

@socketio.on('new_message')
def handle_new_message(data):
    # Extract the necessary data from the received message
    new_message = data['message']
    user_idCurrent = session['user_id']
    user_idOther = data['user_idOther']

    # Process and store the new message in the database
    id = randomIDcreator("M")
    exist = True
    while exist:
        cur = conn.cursor()
        conn.rollback()
        cur.execute("select count(*) from chatting where messageid = %s;", (id,))
        num = cur.fetchone()
        if num[0] == 0:
            exist = False
        else:
            id = randomIDcreator("M")
    time = datetime.datetime.now()
    cur = conn.cursor()
    conn.rollback()
    cur.execute(
        "INSERT INTO chatting (messageid, sentby, sentto, time, message) VALUES (%s, %s, %s, %s, %s)",
        (id, user_idCurrent, user_idOther, time, new_message))
    conn.commit()
    cur.close()

    # Broadcast the new message to all connected clients
    emit('message_broadcast', {'message': new_message}, broadcast=True)


@app.route('/load_more_group/<group_id>')
def load_more_group(group_id):
    current = int(request.args.get('current'))
    limit = 3  # Number of additional images to load

    cur = conn.cursor()
    conn.rollback()
    cur.execute('''
        SELECT
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
            post.belongstogroups = %s
        GROUP BY
            post.postid
        order by
            post.postid
        LIMIT %s OFFSET %s;
    ''', (session['user_id'],group_id, limit, current))
    images = cur.fetchall()

    cur.close()
    
    return render_template('load_more.html', images=images)


@app.route("/create-account", methods = ['GET' , "POST"])
def CreateAccount():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        gender = request.form['gender']
        hostel = request.form['hostel']
        conn.rollback()
        curr.execute("select count(*) from person where kerberosid = %s;" , (username, ))
        count = curr.fetchall()

        if count[0][0] > 0:
            flash("user already exists" , 'warning')
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
            session['user_name'] = name 
            session['name'] = name
            conn.rollback()
            curr.execute("insert into person values(%s,%s,%s,%s);", (username, name ,hostel ,gender,))
            curr.execute("insert into passwords values(%s, %s);", (username, password,))
            conn.commit()
            return redirect(url_for('Home') )
    return render_template("create-account.html")


@app.route("/" , methods = ['POST', 'GET'])
def Login():
    if request.method != 'POST':
        return render_template("login.html")
    session.pop('user_id' , None)
    username = request.form['username']
    password = request.form['password']
    conn.rollback()
    curr.execute("select pass from passwords where kerberosid = %s;" , (username,))
    correct_pass = curr.fetchone()
    curr.execute("SELECT count(*) FROM person WHERE kerberosid = %s;", (username,))
    count = curr.fetchall()
    if count[0][0] != 1:
        flash("Login Failed! User doesnt exist",'warning')
        return redirect(url_for('Login') )
    if password != correct_pass[0]:
        flash("Login Failed! Incorrect password",'warning')
        return redirect(url_for('Login') )
    conn.rollback()
    curr.execute("select name from person where kerberosid=%s;",(username,))
    name = curr.fetchone()
    session['user_id'] = username
    session['name'] = name[0]
    flash('You have successfully logged in', 'success')
    return redirect(url_for('Home') )



@app.route('/home')
def Home():
    cur = conn.cursor()
    conn.rollback()
    current = int(request.args.get('current', 3))  # Get the 'current' parameter from the request or default to 3
    limit = current + 3  # Limit the number of images fetched
    cur.execute("select * from friends where person1 = %s;",(session['user_id'],))
    p = cur.fetchall()
    print("f",p)
    print(session['user_id'])
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
                        left JOIN friends on friends.person1 = post.postedby
                        left JOIN person_likes_post ON post.postid = person_likes_post.postid
                        left JOIN person ON person_likes_post.kerberosid = person.kerberosid
                    WHERE
                        (post.belongstogroups IS NULL
                        OR post.belongstogroups = '')
                        AND friends.person2 = %s
                    GROUP BY
                        post.postid
                    
                    union all 
                    SELECT
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
                        left JOIN friends on friends.person2 = post.postedby
                        left JOIN person_likes_post ON post.postid = person_likes_post.postid
                        left JOIN person ON person_likes_post.kerberosid = person.kerberosid
                    WHERE
                        (post.belongstogroups IS NULL
                        OR post.belongstogroups = '')
                        AND friends.person1 = %s
                    GROUP BY
                        post.postid
                    ;
''', (session['user_id'],session['user_id'],session['user_id'],session['user_id']))
    images = cur.fetchall()

    

    cur.close()
    return render_template('home.html', images=images, current = current)


@app.route('/load_more')
def load_more():
    current = int(request.args.get('current'))
    limit = 3  # Number of additional images to load

    cur = conn.cursor()
    conn.rollback()
    cur.execute('''
        SELECT
            post.postid,
            post.postedby,
            COUNT(person_likes_post.kerberosid) AS like_count,
            post.caption,
            (SELECT COUNT(*) 
             FROM person_likes_post 
             WHERE post.postid = person_likes_post.postid 
             AND person_likes_post.kerberosID = %s) AS user_like_count
        FROM
            post
            JOIN person_likes_post ON post.postid = person_likes_post.postid
            JOIN person ON person_likes_post.kerberosid = person.kerberosid
            JOIN friends ON friends.person1 = post.postedby
        WHERE
            (post.belongstogroups IS NULL
            OR post.belongstogroups = '')
            AND friends.person2 = %s
        GROUP BY
            post.postid
                    
        UNION
        
        SELECT
            post.postid,
            post.postedby,
            COUNT(person_likes_post.kerberosid) AS like_count,
            post.caption,
            (SELECT COUNT(*) 
             FROM person_likes_post 
             WHERE post.postid = person_likes_post.postid 
             AND person_likes_post.kerberosID = %s) AS user_like_count
        FROM
            post
            JOIN person_likes_post ON post.postid = person_likes_post.postid
            JOIN person ON person_likes_post.kerberosid = person.kerberosid
            JOIN friends ON friends.person2 = post.postedby
        WHERE
            (post.belongstogroups IS NULL
            OR post.belongstogroups = '')
            AND friends.person1 = %s
        GROUP BY
            post.postid
        LIMIT %s OFFSET %s;
    ''', (session['user_id'], session['user_id'], session['user_id'], session['user_id'], limit, current))
    images = cur.fetchall()

    cur.close()
    
    return render_template('load_more.html', images=images)


@app.route('/load_more_profile')

def load_more_profile():
    
    current = int(request.args.get('current'))
    limit = 3  # Number of additional images to load

    cur = conn.cursor()
    conn.rollback()
    cur.execute('''
        SELECT
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
            (post.belongstogroups IS NULL or post.belongstogroups = '')
            AND post.postedby = %s
        GROUP BY
            post.postid 
        order by post.postid
        LIMIT %s OFFSET %s;
    ''', (session['user_id'],session['user_id'],limit, current))
    images = cur.fetchall()

    cur.close()
    
    return render_template('load_more.html', images=images)


@app.route('/profile')
def Profile():
    cur = conn.cursor()
    conn.rollback()
    cur.execute("select count(*) from friends where person1 = %s or person2 = %s;" ,(session['user_id'],session['user_id']))
    friends = cur.fetchone()[0]
    current = int(request.args.get('current', 3))  # Get the 'current' parameter from the request or default to 3

    conn.rollback()
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
                        (post.belongstogroups IS NULL or post.belongstogroups = '')
                        AND post.postedby = %s
                    GROUP BY
                        post.postid
                    order by post.postid;
''', (session['user_id'],session['user_id'],))
    images = cur.fetchall()
        
    
    cur.close()
    return render_template('profile.html',kerberosid=session['user_id'],username=session['name'], images=images, friends = friends , current =current)


@app.route('/home/<image_id>', methods=['GET', 'POST'])
def get_image(image_id):
    cur = conn.cursor()
    conn.rollback()
    cur.execute("SELECT image  FROM post WHERE postid = %s", (image_id,))

    image_data = cur.fetchone()[0]
       
    cur.close()
    return Response(image_data, content_type='image/jpeg')

@app.route('/home/likes/<image_id>', methods=['POST'])
def get_likes(image_id):
    cur = conn.cursor()
    conn.rollback()
    cur.execute("SELECT COUNT(*) FROM person_likes_post WHERE kerberosid = %s AND postid = %s", (session['user_id'], image_id))
    count = cur.fetchone()[0]
    if count == 0:
        conn.rollback()
        cur.execute("INSERT INTO person_likes_post (kerberosid, postid) VALUES (%s, %s)", (session['user_id'], image_id))
    else:
        conn.rollback()
        cur.execute("DELETE FROM person_likes_post WHERE kerberosid = %s AND postid = %s", (session['user_id'], image_id))
    conn.commit()

    conn.rollback()
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
            conn.rollback()
            cur.execute("select count(*) from comments where commentid = %s;", (id, ))
            num = cur.fetchone()
            if num[0] == 0:
                exist = False  
            else :
                id = randomIDcreator("C")
        comment = request.form['comment']
        cur = conn.cursor()
        conn.rollback()
        cur.execute("INSERT INTO comments (commentid, content, creatorpersonid, parentpostid) VALUES (%s, %s, %s, %s)", ( id , comment, session['user_id'], image_id))
        conn.commit()

    # Retrieve all comments for the given image ID
    cur = conn.cursor()
    conn.rollback()
    cur.execute("SELECT content, creatorpersonid FROM comments WHERE parentpostid = %s", (image_id,))
    comments = cur.fetchall()

    return render_template('comments.html', comments=comments)

@app.route("/chat/<user_idOther>", methods = ['GET' , 'POST'])
def Chat(user_idOther):
    user_idCurrent = session['user_id']
    cur = conn.cursor()
    conn.rollback()
    cur.execute("select name from person where kerberosid = %s;",(user_idOther,))
    other_username = cur.fetchone()
    # print(other_username)
    # if request.method == 'POST':
    if request.method == 'POST':
        id = randomIDcreator("M")
        exist = True
        while exist:  
            cur = conn.cursor()
            conn.rollback()
            cur.execute("select count(*) from chatting where messageid = %s;", (id, ))
            num = cur.fetchone()
            if num[0] == 0:
                exist = False  
            else :
                id = randomIDcreator("M")
        newMessage = request.form.get('newMessage')
       
        time = datetime.datetime.now()
        cur = conn.cursor()
        conn.rollback()
        cur.execute("INSERT INTO chatting (messageid, sentby, sentto, time, message) VALUES (%s, %s, %s, %s, %s)", (id, user_idCurrent, user_idOther, time, newMessage))
        conn.commit()
        cur.close()
        return redirect(url_for('Chat', user_idOther=user_idOther))
    cur = conn.cursor()
    conn.rollback()
    cur.execute("SELECT message, sentby FROM chatting WHERE (sentby = %s AND sentto = %s) OR (sentby = %s AND sentto = %s) ORDER BY time ASC", (user_idCurrent, user_idOther, user_idOther, user_idCurrent))
    messages = cur.fetchall()
    cur.close()
    return render_template("chat.html", messages=messages, name=user_idOther, user = other_username[0])
    


@app.route("/chats")
def Chats():
    user_id = session['user_id']
    cur = conn.cursor()
    conn.rollback()
    # cur.execute("WITH chatlist AS (SELECT distinct sentby as other FROM messages WHERE sentto = %s UNION SELECT distinct sentto as other FROM messages WHERE sentby = %s) SELECT other FROM chatlist WHERE other != %s", (user_id, user_id, user_id))
    cur.execute("SELECT person2 FROM Friends WHERE Person1 = %s UNION SELECT person1 FROM Friends WHERE Person2 = %s", (session['user_id'], session['user_id']))
    chats = cur.fetchall()
    cur.close()
    return render_template("chats.html", chats=chats)



@app.route("/groups")
def Groups():
    cur = conn.cursor()
    conn.rollback()
    cur.execute("select groups.groupid, title from groups join person_belongsto_group on kerberosid = %s and person_belongsto_group.groupid = groups.groupid;" ,(session['user_id'],))
    groups = cur.fetchall()
    return render_template("groups.html", groups=groups)



@app.route("/searching" , methods = ['GET' , 'POST'])
def Search():

    useridstr = request.form['query']
    # print(useridstr)
    cur = conn.cursor()
    conn.rollback()
    cur.execute("SELECT kerberosid, name from person where kerberosid like %s or name like %s ;", (f"%{useridstr}%",f"%{useridstr}%",))

    users = cur.fetchall()
    return render_template("search.html", users=users)

@app.route('/post-upload/<group_id>', methods=['GET', 'POST'])
def post_upload(group_id):
    if request.method != 'POST':
        return render_template('post_upload.html')
    id = randomIDcreator("P")
    exist = True
    while exist:  
        cur = conn.cursor()
        conn.rollback()
        cur.execute("select count(*) from post where postid = %s;", (id, ))
        num = cur.fetchone()
        if num[0] == 0:
            exist = False  
        else :
            id = randomIDcreator("P")
    file = request.files['file']
    image_data1 = Image.open(file)
    buffer = BytesIO()
    quality = 10
    image_data1.save(buffer, format='JPEG', optimize=True, quality=quality)
    image_data = buffer.getvalue()
    caption = request.form['caption']

    if group_id == 'G':
        group_id = ''
    conn.rollback()
    curr.execute("INSERT INTO post values(%s,%s, %s, %s, %s)" , (id ,image_data, caption, session['user_id'], group_id) )
    conn.commit()
    return redirect(url_for('Profile'))
    
        
@app.route("/FriendsProfile/<kerberosid>" , methods = ['GET','POST'])
def FriendsProfile(kerberosid):
    current = int(request.args.get('current', 3 ))  # Get the 'current' parameter from the request or default to 3
    limit = current + 3  # Limit the number of images fetched

    cur = conn.cursor()
    conn.rollback()
    cur.execute("select count(*) from friends where person1 = %s or person2 = %s;" ,(kerberosid,kerberosid,))
    friends = cur.fetchone()[0]
    conn.rollback()
    cur.execute("select name from person where kerberosid = %s ;" ,(kerberosid,))

    name = cur.fetchone()[0]
    conn.rollback()
    cur.execute("select count(*) from friends where (person1 = %s and person2 = %s) or (person2 = %s and person1 = %s);" ,(kerberosid,session['user_id'], kerberosid,session['user_id'],))
    is_friend = cur.fetchone()[0]
    conn.rollback()


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
                        (post.belongstogroups IS NULL or post.belongstogroups = '') 
                        AND post.postedby = %s
                    GROUP BY
                        post.postid
                    order by 
                        post.postid;
''', (session['user_id'],kerberosid,))
    images = cur.fetchall()
    cur.close()
    return render_template('friends_profile.html',user_id = session['user_id'],is_friend = is_friend,kerberosid=kerberosid,username=name,images=images,friends = friends,current = current)


@app.route('/load_more_friends/<kerberosid>')
def load_more_friends(kerberosid):
    current = int(request.args.get('current'))
    limit = 3  # Number of additional images to load

    cur = conn.cursor()
    conn.rollback()
    cur.execute('''
        SELECT
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
            (post.belongstogroups IS NULL or post.belongstogroups = '') 
            AND post.postedby = %s
        GROUP BY
            post.postid
        order by 
            post.postid
        LIMIT %s OFFSET %s
    ''', (session['user_id'],kerberosid,limit, current))
    images = cur.fetchall()

    cur.close()
    
    return render_template('load_more.html', images=images)



if __name__ == '__main__':
    
    app.debug = True
    app.run(debug=True)
