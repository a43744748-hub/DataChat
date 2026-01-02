import pandas as pd
import sqlite3
import os


def create_db_from_csvs(folder_path, db_name='my_data.db'):
    """
    Reads all CSV files in a specified folder and creates a separate table
    for each one in an SQLite database.


    Args:
        folder_path (str): The path to the folder containing the CSV files.
        db_name (str): The name for the SQLite database file.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print(f"Database '{db_name}' created/connected successfully.")


    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)


            table_name = filename.replace('.csv', '').replace(' ', '_').replace('.', '_')


            try:
                df = pd.read_csv(file_path)


                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"✅ Successfully created table: **{table_name}**")


            except Exception as e:
                print(f"❌ Error processing file {filename}: {e}")


    conn.commit()
    conn.close()
    print("\nAll CSV files processed and connection closed.")


if __name__ == "__main__":
    csv_folder_location = './data/'
    database_file_name = 'pharma.db'


    if not os.path.exists(csv_folder_location):
        print(f"Error: Folder path '{csv_folder_location}' does not exist. Please check the path.")
    else:
        create_db_from_csvs(csv_folder_location, database_file_name)