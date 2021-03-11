import connexion
import sqlite3
from swagger_server.models.node import Node  # noqa: E501


db_name = 'nodes.db'
init_con = sqlite3.connect(db_name)
init_cur = init_con.cursor()
init_cur.execute("CREATE TABLE IF NOT EXISTS nodes ("
    "fqdn text,"
    "serviceTag text,"
    "hostName text,"
    "status text PRIMARY KEY"))
init_con.commit()

def add_node(body):  # noqa: E501
    """Add a new node

     # noqa: E501

    :param body: Node object that needs to be added
    :type body: dict | bytes

    :rtype: Node
    """
    if connexion.request.is_json:
        body = Node.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        with sqlite3.connect(db_name) as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            pre_select = cur.execute("SELECT * FROM nodes WHERE "
                                     f"serviceTag='{body.service_tag}'")
            pre_result = pre_select.fetchone()
            if pre_result:
                return {"error": "Node not created, already exists"}, 500
            cur.execute(f"INSERT INTO nodes VALUES ('{body.fqdn}',"
                        f"'{body.service_tag}',"
                        f"'{body.host_name}',"
                        "'unknown')")
            con.commit()
            select = cur.execute("SELECT * FROM nodes WHERE "
                                 f"serviceTag='{body.service_tag}'")
            result = select.fetchone()
    except:
        return {"error": "Invalid Field"}, 405
    if not result:
        return {"error": "Node not created"}, 500
    return result


def delete_node(serviceTag):  # noqa: E501
    """Deletes a node

     # noqa: E501

    :param serviceTag: Node serviceTag to delete
    :type serviceTag: str

    :rtype: None
    """
    with sqlite3.connect(db_name) as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        select = cur.execute("DELETE FROM nodes "
                             f"WHERE serviceTag='{serviceTag}'")
        result = select.fetchone()
    return result


def get_node_by_service_tag(serviceTag):  # noqa: E501
    """Find node by serviceTag

    Returns a single node # noqa: E501

    :param serviceTag: serviceTag of node to return
    :type serviceTag: str

    :rtype: Node
    """
    with sqlite3.connect(db_name) as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        select = cur.execute("SELECT * FROM nodes "
                             f"WHERE serviceTag='{serviceTag}'")
        result = select.fetchone()
    return result


def get_nodes():  # noqa: E501
    """Get all nodes

     # noqa: E501


    :rtype: None
    """
    with sqlite3.connect(db_name) as con:
        con.row_factory = dict_factory
        cur = con.cursor()
        select = cur.execute("SELECT * FROM nodes")
        result = select.fetchall()
    return result


def update_node(serviceTag, body):  # noqa: E501
    """Updates a pet in the store with form data

     # noqa: E501

    :param serviceTag: serviceTag of node that needs to be updated
    :type serviceTag: str
    :param body: Node object that needs to be updated
    :type body: dict | bytes

    :rtype: Node
    """
    if connexion.request.is_json:
        body = Node.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        with sqlite3.connect(db_name) as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute(f"UPDATE nodes SET fqdn = '{body.fqdn}',"
                        f"hostName = '{body.host_name}'"
                        f"WHERE serviceTag = '{serviceTag}'")
            con.commit()
            select = cur.execute("SELECT * FROM nodes WHERE "
                                 f"serviceTag='{serviceTag}'")
            result = select.fetchone()
    except:
        return {"error": "Invalid Field"}, 405
    if not result:
        return {"error": "Node not created"}, 500
    return result


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
