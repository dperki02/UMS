from flask import Flask, render_template, request
import mysql.connector

db_config = {
    'host': 'database-ums.c7ksas0oekmx.us-east-2.rds.amazonaws.com',
    'user': 'admin',
    'password': 'password123',
    'database': 'userdb'
}


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle Form Submission Implement DB insert logic here
        username = request.form['username']
        password = request.form['password'] 
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            insert_query = """
            INSERT INTO users (username, password, first_name, last_name, email)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (username, password, first_name, last_name, email))
            conn.commit()

            cursor.close()
            conn.close()
  
            return render_template('success.html')
        except mysql.connector.Error as err:
            return f"Error: {err}"
    
    return render_template('register.html')

@app.route('/users', methods=['GET'])
def users():
    query = request.args.get('q', '')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        if query:
            sql = """
                SELECT * FROM users 
                WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR email LIKE %s
            """
            like_query = f"%{query}%"
            cursor.execute(sql, (like_query, like_query, like_query, like_query))
        else:
            cursor.execute("SELECT * FROM users")

        users = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('admin.html', users=users)

    except mysql.connector.Error as err:
        return f"Error: {err}"

@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
