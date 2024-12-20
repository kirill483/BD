from repositories.connector import get_connection
from datetime import date

def get_liables(office_id: int, first_name: str, last_name: str):
    query = """
        SELECT liables.user_id, first_name, last_name, birth_date, health_level, health_description
        FROM liables
        LEFT JOIN health_reports ON liables.user_id = health_reports.user_id
        WHERE military_office_id = %(office_id)s 
          AND first_name ILIKE %(first_name)s 
          AND last_name  ILIKE %(last_name)s
          AND liables.user_id not in (SELECT user_id FROM summons);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "office_id": office_id,
                "first_name": first_name,
                "last_name": last_name
            })
            return cur.fetchall()

def get_all_liables(office_id: int):
    query = """
        SELECT liables.user_id, first_name, last_name, birth_date, health_level, health_description
        FROM liables
        LEFT JOIN health_reports ON liables.user_id = health_reports.user_id
        WHERE military_office_id = %(office_id)s
          AND liables.user_id not in (SELECT user_id FROM summons)
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "office_id": office_id
            })
            return cur.fetchall()

def create_summon(liable_id: int, appearance_time: str, description: str, worker_id: int, military_office_id: int):
    query = """
        INSERT INTO summons (user_id, creation_date, appearance_date, description, worker_id, military_office_id)
        VALUES (%(liable_id)s, %(creation_date)s, %(appearance_time)s, %(description)s, %(worker_id)s, %(military_office_id)s);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "liable_id": liable_id,
                "creation_date": date.today(),
                "appearance_time": appearance_time,
                "description": description,
                "worker_id": worker_id,
                "military_office_id": military_office_id
            })
            conn.commit()

def get_summons(office_id: int, first_name: str, last_name: str):
    query = """
        SELECT summon_id, creation_date, appearance_date, description, 
               liables.first_name, liables.last_name, liables.birth_date
        FROM summons
        LEFT JOIN liables ON summons.user_id = liables.user_id
        WHERE liables.military_office_id = %(office_id)s 
          AND liables.first_name ILIKE %(first_name)s 
          AND liables.last_name ILIKE %(last_name)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "office_id": office_id,
                "first_name": first_name,
                "last_name": last_name
            })
            return cur.fetchall()

def get_all_summons(office_id: int):
    query = """
        SELECT summon_id, creation_date, appearance_date, description, 
               liables.first_name, liables.last_name, liables.birth_date
        FROM summons
        LEFT JOIN liables ON summons.user_id = liables.user_id
        WHERE summons.military_office_id = %(office_id)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "office_id": office_id
            })
            return cur.fetchall()

def delete_summon(summon_id: int):
    query = """
        DELETE FROM summons
        WHERE summon_id = %(summon_id)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "summon_id": summon_id
            })
            conn.commit()

def get_health_data(office_id: int, first_name: str, last_name: str):
    query = """
        SELECT liables.user_id, liables.first_name, liables.last_name, liables.birth_date, array_agg(health_data.description) as descriptions
        FROM liables
        JOIN health_data ON liables.user_id = health_data.user_id
        WHERE liables.military_office_id = %(office_id)s
          AND liables.first_name ILIKE %(first_name)s
          AND liables.last_name ILIKE %(last_name)s
        GROUP BY liables.user_id, liables.first_name, liables.last_name, liables.birth_date;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "office_id": office_id,
                "first_name": f"%{first_name}%",
                "last_name": f"%{last_name}%"
            })
            return cur.fetchall()

def get_all_health_data(office_id: int):
    query = """
        SELECT liables.user_id, liables.first_name, liables.last_name, liables.birth_date, array_agg(health_data.description) as descriptions
        FROM liables
        JOIN health_data ON liables.user_id = health_data.user_id
        WHERE liables.military_office_id = %(office_id)s
        GROUP BY liables.user_id, liables.first_name, liables.last_name, liables.birth_date;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"office_id": office_id})
            return cur.fetchall()

def create_health_report(liable_id: int, worker_id: int, level: str, description: str):
    query = """
        INSERT INTO health_reports (user_id, worker_id, health_level, health_description)
        VALUES (%(liable_id)s, %(worker_id)s, %(level)s, %(description)s);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "liable_id": liable_id,
                "worker_id": worker_id,
                "level": level,
                "description": description
            })
            conn.commit()

def get_health_reports(office_id: int, first_name: str, last_name: str):
    query = """
        SELECT health_reports.report_id, health_reports.health_level, health_reports.health_description,
               liables.first_name, liables.last_name, liables.birth_date
        FROM health_reports
        LEFT JOIN liables ON health_reports.user_id = liables.user_id
        WHERE liables.military_office_id = %(office_id)s
          AND liables.first_name ILIKE %(first_name)s
          AND liables.last_name ILIKE %(last_name)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {
                "office_id": office_id,
                "first_name": f"%{first_name}%",
                "last_name": f"%{last_name}%"
            })
            return cur.fetchall()

def get_all_health_reports(office_id: int):
    query = """
        SELECT health_reports.report_id, health_reports.health_level, health_reports.health_description,
               liables.first_name, liables.last_name, liables.birth_date
        FROM health_reports
        LEFT JOIN liables ON health_reports.user_id = liables.user_id
        WHERE liables.military_office_id = %(office_id)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"office_id": office_id})
            return cur.fetchall()

def delete_health_report(report_id: int):
    query = """
        DELETE FROM health_reports
        WHERE report_id = %(report_id)s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"report_id": report_id})
            conn.commit()

