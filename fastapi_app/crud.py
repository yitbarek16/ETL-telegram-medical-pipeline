from fastapi_app.database import get_db_cursor

def get_top_products(limit: int = 10):
    cursor = get_db_cursor()
    cursor.execute(
        """
        SELECT object_class, COUNT(*) AS mention_count
        FROM raw_analytics.fct_image_detections
        GROUP BY object_class
        ORDER BY mention_count DESC
        LIMIT %s
        """, (limit,)
    )
    results = cursor.fetchall()
    cursor.close()
    return results

def get_channel_activity(channel_name: str):
    cursor = get_db_cursor()
    cursor.execute("""
    SELECT 
        date_day AS date,
        COUNT(*) AS message_count
    FROM raw_analytics.fct_messages
    WHERE channel_name = %s
    GROUP BY date_day
    ORDER BY date_day;
""", (channel_name,))

    results = cursor.fetchall()
    cursor.close()
    return results

def search_messages(query: str):
    cursor = get_db_cursor()
    cursor.execute(
        """
        SELECT message_id, message_length, message_text
        FROM raw_analytics.fct_messages
        WHERE message_text ILIKE %s
        LIMIT 50
        """, (f"%{query}%",)
    )
    results = cursor.fetchall()
    cursor.close()
    return results
