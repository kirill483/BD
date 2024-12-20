from repositories.connector import get_connection

def get_user(email: str):
    query = """
        SELECT * FROM users WHERE email = %(email)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "email": email
            })
            return cur.fetchone()

def get_military_office_id(user_id: int, role: str):
    if role == "worker":
        query = """
            SELECT military_office_id FROM workers WHERE user_id = %(user_id)s;
        """
    else:
        query = """
            SELECT military_office_id FROM liables WHERE user_id = %(user_id)s;
        """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "user_id": user_id
            })
            return cur.fetchone()
