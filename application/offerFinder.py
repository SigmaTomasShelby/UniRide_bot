import sqlite3
from datetime import datetime, timedelta

DB_PATH = "visits.db"

def find_offers(
    trip_time_str: str,
    from_place: str,
    to_place: str,
    time_delta_minutes: int = 60
):
    trip_time = datetime.strptime(trip_time_str, "%d.%m.%y %H:%M")

    time_from = (trip_time - timedelta(minutes=time_delta_minutes)).strftime("%d.%m.%y %H:%M")
    time_to = (trip_time + timedelta(minutes=time_delta_minutes)).strftime("%d.%m.%y %H:%M")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    query = """
        SELECT username, name, time_of_start, place_of_departure,
               place_of_arrival, cost, comment
        FROM visits
        WHERE time_of_start BETWEEN ? AND ?
          AND place_of_departure LIKE ?
          AND place_of_arrival LIKE ?
        ORDER BY time_of_start ASC
    """
    params = (
        time_from,
        time_to,
        f"%{from_place}%",
        f"%{to_place}%",
    )

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows
