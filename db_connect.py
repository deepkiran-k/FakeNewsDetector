import mysql.connector
from mysql.connector import Error
from datetime import datetime

def create_db_connection(dbhost, dbuser, dbname):
    """
    Creates and returns a database connection.
    """
    try:
        conn = mysql.connector.connect(
            host=dbhost,
            user=dbuser,
            database=dbname
        )
        print("Database connection successful.")
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def store_search_result(conn, user_id, search_query, verdict, explanation, relevant_links):
    """
    Stores a search result in the search_results table.
    """
    cursor = None  # Define cursor to avoid NameError in the finally block
    try:
        # Create a cursor
        cursor = conn.cursor()
        # SQL query to insert the data
        insert_query = """
            INSERT INTO search_results (user_id, search_query, verdict, explanation, relevant_links, search_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        # Use the current timestamp for the search_date
        current_time = datetime.now()
        cursor.execute(insert_query, (user_id, search_query, verdict, explanation, relevant_links, current_time))

        # Commit the transaction
        conn.commit()
        print(f"Search result for query '{search_query}' stored successfully.")

    except Error as e:
        print(f"Error while storing search result: {e}")
    finally:
        if cursor:
            cursor.close()

def get_latest_search_results(conn, user_id, limit=10):
    """
    Retrieves the top N latest search results for a specific user.
    """
    cursor = None  # Define cursor to avoid NameError in the finally block
    try:
        # Create a cursor
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True to fetch rows as dicts
        # SQL query to fetch the latest results
        select_query = """
            SELECT id, search_query, verdict, explanation, relevant_links, search_date
            FROM search_results
            WHERE user_id = %s
            ORDER BY search_date DESC
            LIMIT %s
        """
        cursor.execute(select_query, (user_id, limit))

        # Fetch all results
        results = cursor.fetchall()
        return results

    except Error as e:
        print(f"Error while retrieving search results: {e}")
        return []
    finally:
        if cursor:
            cursor.close()

def get_dashboard_data(conn):
    """
    Fetch fact-checking statistics for the dashboard.

    Args:
        conn: A database connection object.

    Returns:
        A dictionary containing total articles, verdict distribution, and common false claims.
    """
    try:
        cursor = conn.cursor(dictionary=True)

        # Fetch total articles fact-checked
        cursor.execute("SELECT COUNT(*) AS total_articles FROM search_results")
        total_articles = cursor.fetchone()['total_articles']

        # Fetch percentage of true/false claims
        cursor.execute("""
            SELECT 
                verdict,
                COUNT(*) * 100.0 / (SELECT COUNT(*) FROM search_results) AS percentage
            FROM search_results
            GROUP BY verdict
        """)
        verdict_data = cursor.fetchall()

        # Fetch common topics in false claims
        cursor.execute("""
            SELECT search_query, COUNT(*) AS frequency
            FROM search_results
            WHERE verdict = 'False'
            GROUP BY search_query
            ORDER BY frequency DESC
            LIMIT 10
        """)
        trends_data = cursor.fetchall()

        cursor.close()
        return {
            "total_articles": total_articles,
            "verdict_data": verdict_data,
            "trends_data": trends_data
        }

    except Exception as e:
        raise Exception(f"Error fetching dashboard data: {str(e)}")