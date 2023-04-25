import psycopg2
from flask import Flask 
conn = psycopg2.connect(
    database = 'group_19',
    host = '10.17.6.95',
    port = '5432',
    user = 'group_19',
    password = 'B0jzmL6aEhxI21'
)
curr = conn.cursor()
curr.execute('SELECT COUNT(*) FROM person')


app = Flask(__name__)

@app.route("/")
def index():
    count = curr.fetchall()
    print(count)
    return count

if __name__ == '__main__':
    app.run(host='127.0.0.1' , port=8080, debug=True)



curr.close()
conn.close()