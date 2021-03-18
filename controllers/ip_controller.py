import connexion
import sqlite3
from swagger_server.models.ip import Ip  # noqa: E501


db_name = 'nodes.db'
init_con = sqlite3.connect(db_name)
init_cur = init_con.cursor()
init_cur.execute("CREATE TABLE IF NOT EXISTS ips ("
                 "address text PRIMARY KEY)")
init_con.commit()

def add_ip(body):  # noqa: E501
    """Add a new ip

     # noqa: E501

    :param body: Ip object that needs to be added
    :type body: dict | bytes

    :rtype: Ip
    """
    if connexion.request.is_json:
        body = Ip.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        with sqlite3.connect(db_name) as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            pre_select = cur.execute("SELECT * FROM ips WHERE "
                                     f"address='{body.address}'")
            pre_result = pre_select.fetchone()
            if pre_result:
                return {"error": "IP not created, already exists"}, 500
            cur.execute(f"INSERT INTO ips VALUES ('{body.address}')")
            con.commit()
            select = cur.execute("SELECT * FROM ips WHERE "
                                 f"address='{body.address}'")
            result = select.fetchone()
    except:
        return {"error": "Invalid Field"}, 405
    if not result:
        return {"error": "ip not created"}, 500
    return result


def delete_ip(address):  # noqa: E501
    """Deletes a ip

     # noqa: E501

    :param serviceTag: Ip serviceTag to delete
    :type serviceTag: str

    :rtype: None
    """
    with sqlite3.connect(db_name) as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        select = cur.execute("DELETE FROM ips "
                             f"WHERE address='{address}'")
        con.commit()
        result = select.fetchone()
    return result


def get_ips():  # noqa: E501
    """Get all ips

     # noqa: E501


    :rtype: None
    """
    with sqlite3.connect(db_name) as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        select = cur.execute("SELECT * FROM ips")
        result = select.fetchall()
    return result


def next_ip():
    """Get all next IP

     # noqa: E501


    :rtype: None
    """
    with sqlite3.connect(db_name) as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        select = cur.execute("SELECT * FROM ips")
        result = select.fetchone()
    delete_ip(result['address'])
    return result


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
