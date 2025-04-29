from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Later: Handle Form Submission Implement DB insert logic here
        return render_template('success.html')
    return render_template('register.html')

@app.route('/users', methods=['GET'])
def users():
    users = []  # Later: Fetch from DB clearly
    return render_template('admin.html', users=users)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
