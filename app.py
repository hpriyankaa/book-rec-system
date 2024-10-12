from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import pickle
import numpy as np

# Load your existing data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)


# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect('your_database.db')  # Make sure to use your database file
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = (books[books['Book-Title'] == pt.index[i[0]]])
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
        item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)

        data.append(item)
    print(data)
    return render_template('recommend.html', data=data)


@app.route('/set_challenge', methods=['GET', 'POST'])
def set_challenge():
    if request.method == 'POST':
        user_id = 1  # Static for now; replace with actual user id after authentication
        description = request.form['description']
        target_books = request.form['target_books']
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = request.form['end_date']

        # Insert into the database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO challenges (user_id, challenge_description, target_books, start_date, end_date) 
            VALUES (?, ?, ?, ?, ?)''',
                     (user_id, description, target_books, start_date, end_date))
        conn.commit()
        conn.close()

        return redirect(url_for('view_challenges'))

    return render_template('set_challenge.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # You can process/store the form data here
    print(f"Received message from {name}, Email: {email}, Message: {message}")

    return 'Thank you for reaching out! We will get back to you soon.'


@app.route('/view_challenges')
def view_challenges():
    conn = get_db_connection()
    challenges = conn.execute('SELECT * FROM challenges WHERE user_id = 1').fetchall()  # Static user_id for now
    conn.close()
    return render_template('view_challenges.html', challenges=challenges)


if __name__ == '__main__':
    app.run(debug=True)


