import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')  # For non-GUI environments

app = Flask(__name__)

# Function to create and populate the database
def create_and_populate_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    # Drop the existing table if it exists to prevent schema conflicts
    cursor.execute('DROP TABLE IF EXISTS students')

    # Create table with corrected schema
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        skill1 TEXT,
        skill2 TEXT,
        interests1 TEXT,
        interests2 TEXT
    )
    ''')

    # Sample data
    students_data = [
        ('Richa', 'ars07richa@gmail.com', 'Python', 'Machine Learning', 'ML', 'Data Science'),
        ('Sharadhi', 'sharadiga1706@gmail.com', 'Java', 'Web Development', 'AI', 'Cloud Computing'),
        ('Shreya', 'shreyasuresh989@gmail.com', 'Azure', 'Machine Learning', 'Mobile App Development', 'Data Science'),
        ('Radhika', 'radhika@gmail.com', 'C++', 'Python', 'Gaming', 'AI'),
        ('Pramathi', 'pramathi@gmail.com', 'JavaScript', 'React', 'Web Development', 'UI/UX'),
        ('Nandini', 'nan@gmail.com', 'React', 'Data Analysis', 'ML', 'Data Science'),
        ('Anuj', 'anuj123@gmail.com', 'Java', 'Kotlin', 'Mobile Development', 'AI'),
        ('Abir', 'abhirkumar@gmail.com', 'C++', 'Python', 'Gaming', 'AI'),
        ('Ajay', 'ajays@gmail.com', 'JavaScript', 'Azure', 'Web Development', 'Cloud Computing'),
        ('Aman', 'aman896@example.com', 'Python', 'Machine Learning', 'PHP', 'Data Science'),
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO students (name, email, skill1, skill2, interests1, interests2)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', students_data)

    conn.commit()
    conn.close()

# Function to recommend peers based on input
def recommend_peers(selected_skills, selected_interests):
    conn = sqlite3.connect('students.db')
    query = "SELECT * FROM students"
    df = pd.read_sql(query, conn)
    conn.close()

    df['combined_features'] = df['skill1'] + " " + df['skill2'] + " " + df['interests1'] + " " + df['interests2']
    user_features = f"{selected_skills}, {selected_interests}"

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(df['combined_features'].tolist() + [user_features])

    user_vector = vectors[-1]
    student_vectors = vectors[:-1]

    similarity = cosine_similarity(user_vector, student_vectors)

    df['similarity'] = similarity[0]
    df['similarity_percentage'] = df['similarity'] * 100

    recommendations = df.sort_values(by='similarity_percentage', ascending=False).head(5)

    return recommendations[['name', 'email', 'skill1', 'skill2', 'interests1', 'interests2', 'similarity_percentage']]

# Route for form and recommendations
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_skills = request.form.get('skills')
        selected_interests = request.form.get('interests')
        recommendations = recommend_peers(selected_skills, selected_interests)
    else:
        recommendations = pd.DataFrame()

    conn = sqlite3.connect('students.db')
    skills_list = pd.read_sql("SELECT DISTINCT skill1 FROM students", conn)['skill1'].tolist()
    interests_list = pd.read_sql("SELECT DISTINCT interests1 FROM students", conn)['interests1'].tolist()
    conn.close()

    return render_template(
        "graph.html",
        skills_list=skills_list,
        interests_list=interests_list,
        recommendations=recommendations.to_dict(orient='records') if not recommendations.empty else []
    )

if __name__ == '__main__':
    create_and_populate_db()  # Ensure data is inserted
    app.run(debug=True)
