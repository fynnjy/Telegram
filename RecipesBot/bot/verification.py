import sqlite3


# Creating a database with recipes
def db_recipes_creation():
    connect = sqlite3.connect('../db/info.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS recipes(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title VARCHAR(30),
        photo BLOB NOT NULL,
        description VARCHAR(3000)        
    )""")

    connect.commit()
    connect.close()


# The function responsible for checking the user's fingerprint in the database
def check_user(userid):
    try:
        # Connect DB and create new table
        connect = sqlite3.connect('../db/info.db')
        cursor = connect.cursor()

        # Check id in fields
        cursor.execute(f"SELECT id FROM users WHERE id = {userid}")

        if cursor.fetchone() is None:
            return False

        else:
            for values in cursor.execute(f"SELECT * FROM users WHERE id = {userid}"):
                input_name = values[2]
                gender = values[3]
                registration_period = values[6]

                old_info = {"input_name": input_name,
                            "gender": gender,
                            "registration_period": registration_period}

                connect.close()
                return old_info

    except sqlite3.Error as e:
        print(f"[+] {e}")


# New user creation feature
def registration(userid, username, input_name, gender, first_name,
                 last_name, registration_date):
    try:
        # Connect DB and create new table
        connect = sqlite3.connect('../db/info.db')
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER,
                    username VARCHAR(30),
                    input_name VARCHAR(15),
                    gender VARCHAR,
                    first_name VARCHAR(25),
                    last_name VARCHAR(30),
                    registration_date VARCHAR(30)
                )""")

        connect.commit()

        # Add user in fields
        default_values = [userid, username, input_name, gender, first_name,
                          last_name, registration_date]
        cursor.execute("INSERT INTO users(id, username, input_name, "
                       "gender, first_name, last_name, registration_date) "
                       "VALUES(?, ?, ?, ?, ?, ?, ?)", default_values)

        connect.commit()
        connect.close()

    except sqlite3.Error as e:
        print(f"[+] {e}")
