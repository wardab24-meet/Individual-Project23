
from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

config = {
    "apiKey": "AIzaSyASf3Jp1lbB4qgBw-LWhbcYYDKL9G3cZJM",
    "authDomain": "miniproject-168f0.firebaseapp.com",
    "projectId": "miniproject-168f0",
    "storageBucket": "miniproject-168f0.appspot.com",
    "messagingSenderId": "1071357410059",
    "appId": "1:1071357410059:web:fe374bc107b3a04acf400e",
    "measurementId": "G-TLGT1J456W",
    "databaseURL": "https://miniproject-168f0-default-rtdb.europe-west1.firebasedatabase.app/"
}   

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth.sign_in_with_email_and_password(email, password)
        login_session['user'] =  auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('profile'))
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            db.child('users').child(login_session['user']['localId']).set({'email': email})
            return redirect(url_for('login'))
        except:
            pass
    return render_template("signup.html")

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' in login_session:
        if request.method == "POST":
            profile = db.child('users').child(login_session['user']['localId']).get().val()
            email=profile['email']
            image = request.form['image']
            return render_template("profile.html", email=email, img=image)
        else:
            profile = db.child('users').child(login_session['user']['localId']).get().val()
            email=profile['email']
            return render_template("profile.html", email=email,img=None)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    login_session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if request.method == 'POST':
        # Process the form submission for POST requests if needed
        pass

    products = [
        {
            'name': 'Playstation 5',
            'price': 10.99,
            'image': 'https://www.trustedreviews.com/wp-content/uploads/sites/54/2022/11/PS5-Review-8-1024x768.jpg',
            'description': 'This is a product .'
        },
        {
            'name': 'Playstation 4',
            'price': 15.99,
            'image': "https://upload.wikimedia.org/wikipedia/commons/7/71/Sony-PlayStation-4-PS4-wDualShock-4.jpg",
            'description': 'This is a product .'
        },
        {
            'name': 'XBOX 360',
            'price': 20.99,
            'image': "https://m.media-amazon.com/images/I/81+lz2g6bJL.jpg",
            'description': 'This is a product .'
        },
        {
            'name': 'XBOX ONE',
            'price': 25.99,
            'image': "https://www.stuff.tv/wp-content/uploads/sites/2/2021/08/xbox_1.png?w=1080.jpg",
            'description': 'This is a product .'
        },
        {
            'name': 'Iphone 14',
            'price': 30.99,
            'image': "https://d3m9l0v76dty0.cloudfront.net/system/photos/10722973/original/2e77d6f425b4d252368dcbd8b88c0eb6.jpg",
            'description': 'This is a product .'
        },
        {
            'name': 'Iphone 13',
            'price': 35.99,
            'image': "https://media.wired.com/photos/6148ef98a680b1f2086efee0/1:1/w_1037,h_1037,c_limit/Gear-Review-Apple_iphone13_hero_us_09142021.jpg",
            'description': 'This is a product .'
        },
        {
            'name': 'Laptop',
            'price': 40.99,
            'image': "https://i.pcmag.com/imagery/reviews/02lcg0Rt9G3gSqCpWhFG0o1-2..v1656623239.jpg",
            'description': 'This is a product .'
        },
        {
            'name': 'PC',
            'price': 45.99,
            'image': "https://m.media-amazon.com/images/I/715zrA5cmLL._AC_UF894,1000_QL80_.jpg",
            'description': 'This is a product .'
        },
        {
            'name': 'Speakers',
            'price': 50.99,
            'image': "https://www.popsci.com/uploads/2021/11/12/fluance-ai41-best-speakers.jpg?auto=webp",
            'description': 'This is a product .'
        },
    ]

    return render_template('shop.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)