import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Iterate over the list of drop queries. This drops all relevant tables 
    such that the remaining functions can easily be debugged.
    """

    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Iterate over the list of create queries. This creates all relevant tables
    for staging, facts and dimensions.
    """

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Read config, establish DWH connection and call drop and create functions.
    """

    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()