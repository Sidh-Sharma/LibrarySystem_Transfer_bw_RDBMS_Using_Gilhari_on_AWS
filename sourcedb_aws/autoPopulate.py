#Script to generate bogus data (50 fake JSON objects) to populate an existing MySQL database with 4 tables

import pymysql #to talk to MySQL database
import random 

#Connect to source MySQL database
con = pymysql.connect(
    host="source-db.cj2a0e4oq8nt.ap-south-1.rds.amazonaws.com",
    user="g5",
    password="software_tree5",
    database="db1",
    cursorclass=pymysql.cursors.DictCursor
)
cursor = con.cursor()


authors_and_books = {
    "Jane Austen": ["Pride and Prejudice", "Sense and Sensibility"],
    "Mark Twain": ["The Adventures of Tom Sawyer", "The Adventures of Huckleberry Finn"],
    "Charles Dickens": ["A Tale of Two Cities", "Great Expectations"],
    "George Orwell": ["1984", "Animal Farm"],
    "J.K. Rowling": ["Harry Potter and the Sorcerer's Stone", "Harry Potter and the Chamber of Secrets"],
    "Agatha Christie": ["Murder on the Orient Express", "The ABC Murders"],
    "Ernest Hemingway": ["The Old Man and the Sea", "A Farewell to Arms"],
    "F. Scott Fitzgerald": ["The Great Gatsby", "Tender Is the Night"],
    "Virginia Woolf": ["Mrs Dalloway", "To the Lighthouse"],
    "Leo Tolstoy": ["War and Peace", "Anna Karenina"]
}


genres = ["Fiction", "Science", "Fantasy", "Biography", "Horror", "History"]


def random_email(name):
    domain = random.choice(["gmail.com", "ymail.com", "icloud.com"])
    email = name.lower().replace(" ", ".") + f"@{domain}"
    return email


def random_phone_number():
    return f"(91{random.randint(1000, 9999)}{random.randint(1000, 9999)})"


def random_address():
    
    cities = ["Mumbai", "Delhi", "Kolkata", "NYC", "Bangalore"]
    return f"{random.choice(cities)}"


def generate_isbn():
    prefix = "978"  
    middle = ''.join(random.choices("0123456789", k=9))
    return prefix + middle

def generate_json_data():
    authors = []
    books = []
    members = []
    loans = []

    #Insert Authors 
    for author_name in authors_and_books:
        birth_year = random.randint(1800, 1950)
        authors.append((author_name, birth_year))

    cursor.executemany("INSERT INTO Authors (name, birth_year) VALUES (%s, %s)", authors)
    con.commit()

    #Fetch inserted authors to use their IDs as foreign keys
    cursor.execute("SELECT author_id, name FROM Authors")
    author_records = cursor.fetchall()
    author_id_map = {record['name']: record['author_id'] for record in author_records}

    # Insert Books
    for author_name, book_titles in authors_and_books.items():
        author_id = author_id_map[author_name]
        for title in book_titles:
            genre = random.choice(genres)
            published_year = random.randint(1800, 2023)
            isbn = generate_isbn()
            books.append((title, author_id, genre, published_year, isbn))

    cursor.executemany("INSERT INTO Books (title, author_id, genre, published_year, isbn) VALUES (%s, %s, %s, %s, %s)", books)
    con.commit()

    
    member_names = ["Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince", "Eve Adams"]
    for name in member_names:
        email = random_email(name)
        phone = random_phone_number()
        address = random_address()
        members.append((name, email, phone, address))

    cursor.executemany("INSERT INTO Members (name, email, phone, address) VALUES (%s, %s, %s, %s)", members)
    con.commit()

    # Fetch inserted books and members to use their IDs
    cursor.execute("SELECT book_id FROM Books")
    book_ids = [book['book_id'] for book in cursor.fetchall()]

    cursor.execute("SELECT member_id FROM Members")
    member_ids = [member['member_id'] for member in cursor.fetchall()]

    # Insert Loans
    for _ in range(55):
        book_id = random.choice(book_ids)
        member_id = random.choice(member_ids)
        loan_month = random.randint(1, 11)
        loan_day = random.randint(1, 28)
        loan_date = f"2024-{loan_month:02}-{loan_day:02}"
        return_month = loan_month + 1
        return_day = loan_day 
        return_date = f"2024-{return_month:02}-{return_day:02}"
        loans.append((book_id, member_id, loan_date, return_date))

    cursor.executemany("INSERT INTO Loans (book_id, member_id, loan_date, return_date) VALUES (%s, %s, %s, %s)", loans)
    con.commit()

# Push all tables to the database
generate_json_data()


cursor.close()
con.close()
