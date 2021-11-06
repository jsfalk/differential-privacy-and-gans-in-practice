import sqlite3 as sql

def query(query_str):
    query_str = query_str.lower()
    conn = sql.connect('../data/people.db')
    cur = conn.cursor()
    if query_str.count(';') > 0:
        raise ValueError('Cannot execute multiple statements')
    results = cur.execute(query_str).fetchall()
    if len(results) > 1:
        raise ValueError('Cannot execute query, please use aggregate functions (AVG, COUNT, SUM, MIN, MAX)')
    if len(results) == 0:
        raise ValueError('Cannot execute query for privacy reasons')
    if len(results[0]) > 1:
        raise ValueError('Cannot execute query for privacy reasons')
    if results[0][0] is None:
        raise ValueError('Cannot execute query for privacy reasons')
    modified_query = 'select * from people' + query_str[(query_str.find('from people')+11):]
    count = len(cur.execute(modified_query).fetchall())
    return results[0][0], count


def query_aggregate(query_str):
    result, _ = query(query_str)
    return result


def query_restricted(query_str):
    result, count = query(query_str)
    if count < 50:
        raise ValueError('Cannot execute query for privacy reasons')
    return result
