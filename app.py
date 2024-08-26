from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import requests

app = Flask(__name__)

# Configure your database connection here
db_config = {
    'user': 'root',
    'password': '',  # Update with your MySQL password
    'host': 'localhost',
    'database': 'btl_testimonial'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home page route
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM testimonials')
    testimonials = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', testimonials=testimonials)

# About page route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Gallery page route
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

# Book page route
@app.route('/book')
def book():
    return render_template('book.html')

# TBook page route
# TBook page route
@app.route('/tbook', methods=['GET', 'POST'])
def tbook():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone_number = request.form['phone_number']
        hike = request.form['hike']
        amount_paid = request.form['amount_paid']

        # Insert booking information into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO bookings (full_name, phone_number, hike, amount_paid) VALUES (%s, %s, %s, %s)',
            (full_name, phone_number, hike, amount_paid)
        )
        conn.commit()
        cursor.close()
        conn.close()

        # SMS Integration
        sms_endpoint = "https://api2.tiaraconnect.io/api/messaging/sendsms"
        api_key = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI0MjEiLCJvaWQiOjQyMSwidWlkIjoiN2NhNTQ3NTktMTZkMi00NWI4LWFhNzUtNzc4YmJlYjQxZGRlIiwiYXBpZCI6MzUzLCJpYXQiOjE3MjMxOTM5NDEsImV4cCI6MjA2MzE5Mzk0MX0.2nz6gTpFhCei47FkZQMgJXsGZGD1_0cNaf6nsQtSXyEcZN7vV7W8hwFUVqMTLewAgE9cqdWUhwaCmJ7nDic9gg"

        sms_message = (f'Booking Confirmation!\n\n'
                       f'Name: {full_name}\n'
                       f'Phone Number: {phone_number}\n'
                       f'Hike: {hike}\n'
                       f'Amount Paid: {amount_paid}')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        data = {
            "from": "TIARACONECT",  # Sender ID
            "to": "254721779843",     # Recipient's phone number
            "message": sms_message, # SMS content
            "refId": "TUD5958019"  # Reference ID
        }
      
        response = requests.post(sms_endpoint, json=data, headers=headers)

        if response.status_code == 200:
            print("SMS sent successfully")
        else:
            print(f"Failed to send SMS: {response.text}")

        # Print response for debugging
        print(response.status_code)  # HTTP status code
        print(response.json())  # JSON response from the API

        return redirect(url_for('home'))

    return render_template('tbook.html')


# Review page route
@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        name = request.form['name']
        review = request.form['review']

        # Insert review into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO testimonials (name, review) VALUES (%s, %s)',
            (name, review)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('review.html')

if __name__ == '__main__':
    app.run(debug=True)
