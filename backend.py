import sqlite3
import csv
from os.path import basename


def create_connection():
    """
    Create a database connection to the SQLite3 database.
    
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(r"db\parts.db")
        return conn
    except Error as e:
        print(e)
        
    return None
    

def close_connection(conn):    
    """
    Close database connection to the SQLite3 database.
    
    :param conn: Connection object
    """
    try:
        conn.commit()
        conn.close()
    except Erro as e:
        print(e)   
    
 
def create_table(conn, create_table_sql):
    """
    Create a table from the create_table_sql statement.
    
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print(e)


def part_in_db(conn, table, part_num):
    """
    Checks to see if part exists in the database.
    
    :param conn: Connection object
    :param table: Name of database table
    :param part: Part number to check
    :return: True or False
    """
    cur = conn.cursor()
    sql = "SELECT count(*) FROM " + table + " WHERE part_num = ?"
    cur.execute(sql, (part_num,)) 
    return cur.fetchone()[0]
    

def search_part(table, part):
    """
    Returns part info if part is in database.
    
    :param conn: Connection object
    :param table: Name of database table
    :param part: Part number
    :return: Part info or None
    """
    conn = create_connection()
    
    if conn is not None:
        cur = conn.cursor()
        
        if part_in_db(conn, table, part):
            cur.execute("SELECT * FROM " + table + " WHERE part_num = ?", (part,))
            result = cur.fetchone()
            close_connection(conn)
            return result    
        else:
            return None
    else:
        print("Error! Unable to connect to the database.")        


def add_part(table, part_info):
    """
    Adds part to the SQLite3 database.
    
    :param table: Name of database table
    :param part: part_info to add
    :return: "Done" 
    """
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + table + ";")
        columns = ["?" for list in cur.description]  
        sql = "INSERT OR IGNORE INTO " + table + " VALUES (" + ",".join(columns) + ");"
        cur.execute(sql, part_info)
        close_connection(conn)
        return "Done"
    else:
        print("Error! Unable to connect to the database.")    
    
            
def remove_part(table, part_num):
    """
    Removes a part from the SQLite3 databse.
    
    :param table: Name of database table
    :param part: Part to remove
    :return: "Done" or None
    """
    conn = create_connection()
    if conn is not None:
        if part_in_db(conn, table, part_num):
            cur = conn.cursor()
            sql = "DELETE FROM " + table + " WHERE part_num = ?"
            cur.execute(sql, (part_num,))
            close_connection(conn)
            return "Done"
        else:
            return None
    else:
        print("Error! Unable to connect to the database.")


def convert_to_dict(table, part_num):  # DO I NEED THIS?
    """
    Gets row data of part_num from table and
    converts it to a dict.
    
    :param table: Name of database table
    :param part_num: Part number as string
    :return: Record of part_num
    """
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + table + ";")
        headers = [list[0] for list in cur.description]
        part_info = search_part(table, part_num)        
        part_dict = dict(zip(headers, part_info))
        close_connection(conn)
        return part_dict
    else:
        print("Error! Unable to connect the database.")

        
def list_subs(table, part_num):
    """
    Compares to parts to see if they are valid subs.
    
    :param table: Name of database table
    :param part_num: Part number as string
    :return: List of subs for part_num
    """
    
    def generate_sql(table, part):
        if table == "hdd":
            sql = "SELECT brand, part_num, type, physical_size, height, connector, \
                    hdd_capacity, ssd_capacity, speed FROM " + table + \
                    " WHERE (brand = 'CVO' OR brand = ?) AND type = ? AND physical_size = ? \
                    AND height = ? AND connector = ? AND hdd_capacity = ? \
                    AND ssd_capacity = ? AND speed = ? AND do_not_sub = 'FALSE'"
            cur.execute(sql, (part["brand"], part["type"], part["physical_size"], \
                        part["height"], part["connector"], part["hdd_capacity"], \
                        part["ssd_capacity"], part["speed"]))
            results = [list(filter(None, lst)) for lst in cur.fetchall()]
            return results
        if table == "mem":
            sql = "SELECT brand, part_num, connector, capacity, speed FROM " \
                    table + " WHERE (brand = 'GPC' OR brand = ?) AND \
                    connector = ? AND capacity = ? AND speed = ? AND do_not_sub = 'FALSE'"
            cur.execute(sql, (part["brand"], part["connector"], part["capacity"], part["speed"]))
            results = cur.fetchall()
            return results
        if table == "cpu":
            pass
    
    conn = create_connection()
    
    if conn is not None:
        cur = conn.cursor()           
        part_dict = convert_to_dict(table, part_num)      
        subs = generate_sql(table, part_dict)        
        close_connection(conn)
        return subs        
    else:
        print("Error! Unable to connect to the database.")
        
    pass
        
def remove_table(table):
    """
    Remove table from SQLite3 database.
    
    :param table:  Table to be removed
    """
    conn = create_connection()
    
    if conn is not None:
        cur = conn.cursor()
        cur.execute("DROP TABLE " + table)
    else:
        print("Error! Unable to connect to the database.")
     
    
def import_from_csv(file):
    """
    Import lines from file into SQLite3 database.
    
    :param file: File to import.
    """
    conn = create_connection()
    
    if conn is not None:
        table = basename(file).lower()[:-4]
        with open(file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            first_row = next(reader)
            headers = [header for header,value in first_row.items()]
            headers[0] = "part_num PRIMARY KEY"
            
            create_table(conn, "CREATE TABLE IF NOT EXISTS " + table + "(" + ",".join(headers) + ");")
            
            to_import = [list(row.values()) for row in reader]
            to_import.append(list(first_row.values()))
            
            for list_item in to_import:
                for item in list_item:
                    if item.endswith("\xa0"):
                        index_of_list = to_import.index(list_item)
                        index_of_item = list_item.index(item)
                        to_import[index_of_list][index_of_item] = item.strip()

            cur = conn.cursor()
            columns = ["?" for item in headers]
            cur.executemany("INSERT OR IGNORE INTO " + table + " VALUES (" + ",".join(columns) + ")", to_import)
            
            close_connection(conn)
    else:
        print("Error! Unable to connect to the database.")
    

