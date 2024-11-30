import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate

# Function to insert new data into the database
def insert_data():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    # Insert 10 new records into the table
    students_data = [
        ('Alice', 'alice@example.com', 'Python, Machine Learning', 'AI, Data Science'),
        ('Bob', 'bob@example.com', 'Java, Web Development', 'AI, Cloud Computing'),
        ('Charlie', 'charlie@example.com', 'Python, Machine Learning', 'AI, Data Science'),
        ('David', 'david@example.com', 'C++, Python', 'Gaming, AI'),
        ('Eve', 'eve@example.com', 'JavaScript, React', 'Web Development, UI/UX'),
        ('Frank', 'frank@example.com', 'Python, Data Analysis', 'AI, Data Science'),
        ('Grace', 'grace@example.com', 'Java, Kotlin', 'Mobile Development, AI'),
        ('Hannah', 'hannah@example.com', 'C++, Python', 'Gaming, AI'),
        ('Ivy', 'ivy@example.com', 'JavaScript, React', 'Web Development, Cloud Computing'),
        ('Jack', 'jack@example.com', 'Python, Machine Learning', 'AI, Data Science'),
    ]

    # Insert data into the students table
    cursor.executemany('''
    INSERT OR IGNORE INTO students (name, email, skills, interests)
    VALUES (?, ?, ?, ?)
    ''', students_data)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Function to recommend peers based on email
def recommend_peers(email):
    # Connect to the SQLite database
    conn = sqlite3.connect('students.db')
    
    # Fetch all student records into a DataFrame
    query = "SELECT * FROM students"
    df = pd.read_sql(query, conn)
    conn.close()

    # Find the user whose email is passed as a parameter
    user = df[df['email'] == email]
    if user.empty:
        return "User not found in the database."

    # Combine skills and interests to create a feature string
    df['combined_features'] = df['skills'] + " " + df['interests']
    user_features = user['skills'].iloc[0] + " " + user['interests'].iloc[0]

    # Create a CountVectorizer to convert text data into numerical features
    vectorizer = CountVectorizer()

    # Fit and transform the entire dataset and user features together
    all_features = df['combined_features'].tolist() + [user_features]
    vectors = vectorizer.fit_transform(all_features)

    # Get the vector for the user
    user_vector = vectors[-1]
    
    # Get the vectors for all other students
    student_vectors = vectors[:-1]
    
    # Calculate cosine similarity between the user and all other students
    similarity = cosine_similarity(user_vector, student_vectors)

    # Add similarity to the DataFrame
    df['similarity'] = similarity[0]

    # Convert similarity to percentage
    df['similarity_percentage'] = df['similarity'] * 100

    # Sort students by similarity score (percentage), excluding the user themselves
    recommendations = df[df['email'] != email].sort_values(by='similarity_percentage', ascending=False)

    # Get the top 5 recommendations
    top_recommendations = recommendations[['name', 'email', 'skills', 'interests', 'similarity_percentage']].head(5)

    # Ensure the test person also has the similarity_percentage column
    user['similarity_percentage'] = 100  # The similarity with themselves is always 100%

    # Display the details of the test person
    test_person_details = user[['name', 'email', 'skills', 'interests', 'similarity_percentage']]
    
    # Print the test person first, followed by the recommendations
    print("Test Person's Details:")
    print(tabulate(test_person_details, headers='keys', tablefmt='pretty', showindex=False))
    print("\nTop 5 Peer Recommendations:")
    print(tabulate(top_recommendations, headers='keys', tablefmt='pretty', showindex=False))

# Insert data into the database (run only once to populate the database)
insert_data()

# Test with a user email
if __name__ == "__main__":
    email_to_test = 'alice@example.com'  # Replace with any email from the database
    recommend_peers(email_to_test)
