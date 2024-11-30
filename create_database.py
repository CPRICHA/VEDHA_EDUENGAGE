import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Drop the existing table if it exists
cursor.execute('DROP TABLE IF EXISTS students')

# Create a new table with the correct schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    skill1 TEXT,
    skill2 TEXT,
    interests1 TEXT,
    interest2 TEXT
)
''')

# Insert 10 new records into the table
students_data = [
   ('Richa', 'ars07richa@gmail.com', 'Python', 'Machine Learning', 'ML', 'Data Science'),
        ('Sharadhi', 'sharadiga1706@gmail.com', 'Java', 'Web Development', 'AI', 'Cloud Computing'),
        ('Shreya', 'shreyasuresh989@gmail.com', 'Azure', 'Machine Learning', 'Mobile App Development', 'Data Science'),
        ('Radhika', 'radhika@gmail.com', 'C++', 'Python', 'Gaming', 'AI'),
        ('Pramathi', 'pramathi@gmail.com', 'JavaScript', 'React', 'Web Development', 'UI/UX'),
        ('Nandini', 'nan@gmail.com', 'React', 'Data Analysis', '', 'Data Science'),
        ('Anuj', 'anuj123@gmail.com', 'Java', 'Kotlin', 'Mobile Development', 'AI'),
        ('Abir', 'abhirkumar@gmail.com', 'C++', 'Python', 'Machine Learning', 'AI'),
        ('Ajay', 'ajays@gmail.com', 'JavaScript', 'React', 'Web Development', 'Cloud Computing'),
        ('Aman', 'aman896@example.com', 'Python', 'Machine Learning', 'PHP', 'Data Science'),
]

# Insert data into the students table
cursor.executemany('''
INSERT OR IGNORE INTO students (name, email, skill1, skill2, interests1, interest2)
VALUES (?, ?, ?, ?, ?, ?)
''', students_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted in the database students")
