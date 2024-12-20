from repositories.connector import get_connection
from passlib.hash import bcrypt

def get_military_offices(address: str):
    query = """
        SELECT military_office_id, address FROM military_offices WHERE address = %(address)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "address": address
            })
            return cur.fetchall()

def get_all_military_offices():
    query = """
        SELECT military_office_id, address FROM military_offices;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def add_liable(first_name: str, last_name: str, email: str, birth_date: str, password: str, military_office_id: int):
    password_hash = bcrypt.hash(password)
    role = "liable"
    user_id = None
    user_query = """
        INSERT INTO users (email, hash_password, role)
        VALUES (%(email)s, %(hash_password)s, %(role)s)
        RETURNING user_id;
    """
    liable_query = """
        INSERT INTO liables (user_id, first_name, last_name, birth_date, military_office_id)
        VALUES (%(user_id)s, %(first_name)s, %(last_name)s, %(birth_date)s, %(military_office_id)s);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(user_query, {
                "email": email,
                "hash_password": password_hash,
                "role": role
            })
            user_id = cur.fetchone()[0]
            cur.execute(liable_query, {
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "birth_date": birth_date,
                "military_office_id": military_office_id
            })
            conn.commit()
    return user_id

def get_summons(user_id: int):
    query = """
        SELECT summons.creation_date, summons.appearance_date, summons.description,
               military_offices.address, 
               workers.first_name AS worker_first_name, workers.last_name AS worker_last_name
        FROM summons
        JOIN military_offices ON summons.military_office_id = military_offices.military_office_id
        JOIN workers ON summons.worker_id = workers.user_id
        WHERE summons.user_id = %(user_id)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"user_id": user_id})
            return cur.fetchall()

def get_health_reports(user_id: int):
    query = """
        SELECT health_reports.health_level, health_reports.health_description,
               workers.first_name AS worker_first_name, workers.last_name AS worker_last_name
        FROM health_reports
        JOIN workers ON health_reports.worker_id = workers.user_id
        WHERE health_reports.user_id = %(user_id)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"user_id": user_id})
            return cur.fetchall()

def get_data(user_id: int):
    query = """
        SELECT liables.first_name, liables.last_name, liables.birth_date, users.email,
               military_offices.address AS address_of_military_office
        FROM liables
        JOIN users ON liables.user_id = users.user_id
        JOIN military_offices ON liables.military_office_id = military_offices.military_office_id
        WHERE liables.user_id = %(user_id)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"user_id": user_id})
            return cur.fetchall()

def create_health_data(user_id: int, description: str):
    query = """
        INSERT INTO health_data (user_id, description)
        VALUES (%(user_id)s, %(description)s)
        RETURNING data_id;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"user_id": user_id, "description": description})
            conn.commit()
            return cur.fetchone()[0]

