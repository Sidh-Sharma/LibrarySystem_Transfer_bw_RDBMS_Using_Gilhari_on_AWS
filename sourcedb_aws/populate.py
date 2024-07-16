import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta

def create_connection():
    """Connect to the database."""
    try:
        connection = mysql.connector.connect(
            host='source-db.cvwgwcim6rpq.ap-south-1.rds.amazonaws.com',
            user='admin',
            password='softree_5',
            database='db1'
        )
        if connection.is_connected():
            print("Connection successful")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def insert_data(connection):
    """Insert data into the database."""
    try:
        cursor = connection.cursor()

        authors = [
            ('J.K. Rowling',),
            ('George Orwell',),
            ('J.R.R. Tolkien',),
            ('F. Scott Fitzgerald',),
            ('Jane Austen',),
            ('Mark Twain',),
            ('Charles Dickens',),
            ('Ernest Hemingway',),
            ('Leo Tolstoy',),
            ('Agatha Christie',),
            ('John Green',),
            ('Yuval Noah Harari',),
            ('Tara Westover',),
            ('Michelle Obama',),
            ('Rebecca Skloot',),
            ('David McCullough',)
        ]

        
        cursor.executemany("INSERT INTO authors (name) VALUES (%s)", authors)
        connection.commit()

        #fetch author IDs
        cursor.execute("SELECT author_id, name FROM authors")
        authors_id_map = {name: author_id for author_id, name in cursor.fetchall()}

        
        books = [
            ('Harry Potter and the Philosopher\'s Stone', authors_id_map['J.K. Rowling'], 'Fantasy', 1997, '9780747532699'),
            ('1984', authors_id_map['George Orwell'], 'Dystopian', 1949, '9780451524935'),
            ('The Hobbit', authors_id_map['J.R.R. Tolkien'], 'Fantasy', 1937, '9780345339683'),
            ('The Great Gatsby', authors_id_map['F. Scott Fitzgerald'], 'Novel', 1925, '9780743273565'),
            ('Pride and Prejudice', authors_id_map['Jane Austen'], 'Romance', 1813, '9781503290563'),
            ('Adventures of Huckleberry Finn', authors_id_map['Mark Twain'], 'Adventure', 1884, '9780486280615'),
            ('A Tale of Two Cities', authors_id_map['Charles Dickens'], 'Historical', 1859, '9780486406510'),
            ('The Old Man and the Sea', authors_id_map['Ernest Hemingway'], 'Literary Fiction', 1952, '9780684830490'),
            ('War and Peace', authors_id_map['Leo Tolstoy'], 'Historical', 1869, '9780199232765'),
            ('Murder on the Orient Express', authors_id_map['Agatha Christie'], 'Mystery', 1934, '9780062073495'),
            ('The Fault in Our Stars', authors_id_map['John Green'], 'Young Adult', 2012, '9780525478812'),
            ('Looking for Alaska', authors_id_map['John Green'], 'Young Adult', 2005, '9780142402511'),
            ('Sapiens: A Brief History of Humankind', authors_id_map['Yuval Noah Harari'], 'Non-Fiction', 2011, '9780062316097'),
            ('Educated', authors_id_map['Tara Westover'], 'Non-Fiction', 2018, '9780399590504'),
            ('Becoming', authors_id_map['Michelle Obama'], 'Non-Fiction', 2018, '9781524763138'),
            ('The Immortal Life of Henrietta Lacks', authors_id_map['Rebecca Skloot'], 'Non-Fiction', 2010, '9781400052189'),
            ('The Wright Brothers', authors_id_map['David McCullough'], 'Non-Fiction', 2015, '9781476728759')
        ]

        
        cursor.executemany(
            "INSERT INTO books (title, author_id, genre, published_year, isbn) VALUES (%s, %s, %s, %s, %s)",
            books
        )
        connection.commit()

        
        members = [
            ('Manas Tomar', 'manas.tomar@gmail.com', '9820011222', 'Goa'),
            ('Simran Rao', 'simran_rao@ymail.com', '9820011223', 'Hyderabad'),
            ('Ashmita Dutta', 'alice.johnson@example.com', '9820011224', 'Goa'),
            ('Siddharth Sharma', 'sid10827@gmail.com', '7984537109', 'Pilani')
        ]

     
        cursor.executemany(
            "INSERT INTO members (name, email, phone, address) VALUES (%s, %s, %s, %s)",
             members
        )
        connection.commit()

    
        cursor.execute("SELECT book_id FROM books")
        book_ids = [book_id for (book_id,) in cursor.fetchall()]

        cursor.execute("SELECT member_id FROM members")
        member_ids = [member_id for (member_id,) in cursor.fetchall()]

        
        def random_date(start, end):
            return start + timedelta(days=random.randint(0, (end - start).days))
        
        timedelta_choices = [
            timedelta(weeks=1),
            timedelta(weeks=2),
            timedelta(days=30),     
        ]
        loans = []
        for _ in range(50):
            book_id = random.choice(book_ids)
            member_id = random.choice(member_ids)
            loan_date = random_date(datetime.strptime('2020-11-01', '%Y-%m-%d'), datetime.strptime('2024-01-01', '%Y-%m-%d'))
            return_date = random_date(loan_date, loan_date + random.choice(timedelta_choices))
            loans.append((book_id, member_id, loan_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d')))

        cursor.executemany(
            "INSERT INTO loans (book_id, member_id, loan_date, return_date) VALUES (%s, %s, %s, %s)",
            loans
        )
        connection.commit()

        print("Data inserted successfully")
    except Error as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        cursor.close()

def main():
    connection = create_connection()
    if connection is not None:
        insert_data(connection)
        connection.close()

if __name__ == "__main__":
    main()
