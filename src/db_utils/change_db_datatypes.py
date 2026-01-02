import sqlite3


def alter_db_datatypes(DB_path):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()


    q1 = """
    UPDATE dim_product
    SET launch_date =
        SUBSTR(launch_date, 7, 4) || '-' ||
        SUBSTR(launch_date, 4, 2) || '-' ||
        SUBSTR(launch_date, 1, 2)
    WHERE launch_date IS NOT NULL;
    """


    q2 = """
    UPDATE dim_sales_rep
    SET month =
        SUBSTR(month, 7, 4) || '-' ||
        SUBSTR(month, 4, 2) || '-' ||
        SUBSTR(month, 1, 2)
    WHERE month IS NOT NULL;
    """


    q3 = """
    UPDATE fact_inventory
    SET month =
        SUBSTR(month, 7, 4) || '-' ||
        SUBSTR(month, 4, 2) || '-' ||
        SUBSTR(month, 1, 2)
    WHERE month IS NOT NULL;
    """


    q4 = """
    UPDATE fact_marketing
    SET month =
        SUBSTR(month, 7, 4) || '-' ||
        SUBSTR(month, 4, 2) || '-' ||
        SUBSTR(month, 1, 2)
    WHERE month IS NOT NULL;
    """


    q5 = """
    UPDATE fact_sales
    SET month =
        SUBSTR(month, 7, 4) || '-' ||
        SUBSTR(month, 4, 2) || '-' ||
        SUBSTR(month, 1, 2)
    WHERE month IS NOT NULL;
    """


    cursor.execute(q1)
    cursor.execute(q2)
    cursor.execute(q3)
    cursor.execute(q4)
    cursor.execute(q5)


    conn.commit()


if __name__ == "__main__":
    DB_PATH = "pharma.db"
    alter_db_datatypes(DB_PATH)