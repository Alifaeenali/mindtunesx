import mysql.connector
from mysql.connector import Error
import json
from typing import Dict, Any

def get_database_connection():
    """
    Establish connection to the MindTunes database
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change this to your MySQL host
            database='mindtunes_db',
            user='root',  # Replace with your MySQL username
            password='10,Aug_2023'  # Replace with your MySQL password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def get_all_table_names(connection):
    """
    Get all table names from the database
    """
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    return tables

def get_table_columns(connection, table_name):
    """
    Get column names for a specific table
    """
    cursor = connection.cursor()
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.close()
    return columns

def retrieve_all_data(connection) -> Dict[str, Dict[str, Any]]:
    """
    Retrieve all data from all tables in the specified format
    Returns: dict = {tablename: {column: [data]}}
    """
    all_data = {}
    
    try:
        # Get all table names
        tables = get_all_table_names(connection)
        
        for table in tables:
            print(f"Processing table: {table}")
            
            # Get column names for the table
            columns = get_table_columns(connection, table)
            
            # Initialize table data structure
            table_data = {column: [] for column in columns}
            
            # Fetch all data from the table
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            cursor.close()
            
            # Organize data by columns
            for row in rows:
                for i, column in enumerate(columns):
                    table_data[column].append(row[i])
            
            all_data[table] = table_data
            
    except Error as e:
        print(f"Error retrieving data: {e}")
    
    return all_data

def print_formatted_data(data_dict):
    """
    Print the data in a nicely formatted way
    """
    print("=" * 80)
    print("MINDTUNES DATABASE - ALL DATA")
    print("=" * 80)
    
    for table_name, table_data in data_dict.items():
        print(f"\n📊 TABLE: {table_name.upper()}")
        print("-" * 60)
        
        if not table_data or not any(table_data.values()):
            print("   (No data found)")
            continue
            
        # Get the number of rows
        num_rows = len(next(iter(table_data.values()))) if table_data else 0
        
        for column_name, column_data in table_data.items():
            print(f"   🔹 {column_name}: {column_data}")
        
        print(f"   📈 Total rows: {num_rows}")

def save_to_json(data_dict, filename="mindtunes_data.json"):
    """
    Save the data dictionary to a JSON file
    """
    try:
        # Convert any non-serializable objects to strings
        def serialize_data(obj):
            if hasattr(obj, 'isoformat'):  # datetime objects
                return obj.isoformat()
            return str(obj)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, default=serialize_data, ensure_ascii=False)
        print(f"\n💾 Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def main():
    """
    Main function to execute the data retrieval process
    """
    print("🚀 Starting MindTunes Database Data Retrieval...")
    
    # Establish database connection
    connection = get_database_connection()
    if not connection:
        print("❌ Failed to connect to database. Please check your connection settings.")
        return
    
    try:
        # Retrieve all data
        all_data = retrieve_all_data(connection)
        
        # Print formatted data
        print_formatted_data(all_data)
        
        # Save to JSON file
        save_to_json(all_data)
        
        # Print summary
        print("\n" + "=" * 80)
        print("📋 SUMMARY")
        print("=" * 80)
        total_tables = len(all_data)
        total_records = sum(len(next(iter(table_data.values()))) if table_data else 0 
                          for table_data in all_data.values())
        
        print(f"Total Tables: {total_tables}")
        print(f"Total Records: {total_records}")
        
        for table_name, table_data in all_data.items():
            record_count = len(next(iter(table_data.values()))) if table_data else 0
            print(f"  - {table_name}: {record_count} records")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    finally:
        # Close database connection
        if connection and connection.is_connected():
            connection.close()
            print("\n🔐 Database connection closed.")

if __name__ == "__main__":
    main()

# Alternative function for specific table retrieval
def get_specific_table_data(table_name: str) -> Dict[str, Any]:
    """
    Retrieve data from a specific table only
    Usage: data = get_specific_table_data('navTable')
    """
    connection = get_database_connection()
    if not connection:
        return {}
    
    try:
        columns = get_table_columns(connection, table_name)
        table_data = {column: [] for column in columns}
        
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        cursor.close()
        
        for row in rows:
            for i, column in enumerate(columns):
                table_data[column].append(row[i])
        
        return {table_name: table_data}
        
    except Error as e:
        print(f"Error retrieving data from {table_name}: {e}")
        return {}
    
    finally:
        if connection and connection.is_connected():
            connection.close()
