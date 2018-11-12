from flask import Flask, render_template, redirect, url_for, request, session

from Utils.LoggerUtil import LoggerUtil
from Core.UserAuthentication import UserAuthentication
from Core.UserRegistration import UserRegistration
from Core.UpdateProfile import UpdateProfile

log = LoggerUtil(__name__).get()
auth = UserAuthentication()
reg = UserRegistration()
update = UpdateProfile()

app = Flask(__name__)


@app.route('/index', methods=['GET'])
def hello_world():
    return 'Welcome to cab sharing site :)'


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        is_username_available = auth.is_username_available(username=email)
        if is_username_available:
            reg.add_user(name=name, email=email, contact=contact, password=password)
            return redirect(url_for('login'))
        else:
            error = 'Username not available. Please try again'
    return render_template('registration.html', error=error)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login_method', methods=['POST'])
def login_page():
    error = None
    if request.method == 'POST':
        email_id = request.form['email_id']
        password = request.form['password']
        is_existing_user = auth.check_in_db(email_id, password)
        if is_existing_user:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('logged_out.html')


@app.route('/update', methods=['POST'])
def update():
    try:
        source = request.form['source']
        destination = request.form['destination']
        time = request.form['time']
        date = request.form['date']
        num_seats_req = request.form['num_seats_req']
        # Contact details. If any value
        phone_num = request.form['phone_num']
        email = request.form['email']
        # Below is a text field. If any value
        preferences = request.form['preferences']
        update.update(source, destination, time, date, num_seats_req, phone_num, email, preferences)
        return redirect(url_for('home'))
    except Exception as e:
        error = e
    return render_template('update.html', error=error)


@app.route('/post', methods=['POST'])
def post():
    try:
        pass
    except Exception as e:
        error = e
    return render_template('post.html', error=error)


if __name__ == '__main__':
    app.run()
