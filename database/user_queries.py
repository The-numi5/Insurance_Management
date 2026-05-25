from database.connection import get_connection


def verify_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT user_id, username, role
    FROM USERS
    WHERE username = %s AND password = %s AND role = %s
    """

    cursor.execute(query, (username, password, role))
    user = cursor.fetchone()

    conn.close()
    return user


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT user_id, username, role FROM USERS"
    cursor.execute(query)

    users = cursor.fetchall()

    conn.close()
    return users


def add_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO USERS (username, password, role)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (username, password, role))
    conn.commit()

    conn.close()

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT user_id, username, role FROM USERS WHERE user_id = %s"
    cursor.execute(query, (user_id,))

    user = cursor.fetchone()

    conn.close()
    return user