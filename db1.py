import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import datetime

def connect():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='student_data'
        )
        return conn
    except Error as e:

        messagebox.showerror("Database Connection Error", f"Failed to connect to database: {e}\nPlease ensure MySQL server is running and credentials are correct.")
        return None
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred during connection: {e}")
        return None



def id_exists(student_id):

    conn = connect()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM data WHERE id = %s", (student_id,))
            exists = cursor.fetchone() is not None
            return exists
        except Error as e:
            print(f"Error checking student ID: {e}")

            messagebox.showerror("Database Error", f"Error checking student ID: {e}")
            return True
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
    return True

def insert(id, name, phone, fees, course, gender):

    conn = connect()
    if conn:
        cursor = None
        try:
            if id_exists(id):
                messagebox.showerror("Error", "Student ID already exists!")
                return False

            cursor = conn.cursor()
            query = """INSERT INTO data (id, name, phone, fees, course, gender) VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (id, name, phone, fees, course, gender))
            conn.commit()
            return True
        except Error as e:
            messagebox.showerror("Database Error", f"Insert failed: {e}")
            conn.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
    return False

def fetch_all(column=None, value=None):

    conn = connect()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            if column and value:

                query = f"SELECT * FROM data WHERE `{column}` LIKE %s ORDER BY id"
                cursor.execute(query, (f"%{value}%",))
            else:
                cursor.execute("SELECT * FROM data ORDER BY id")
            return cursor.fetchall()
        except Error as e:
            messagebox.showerror("Database Error", f"Fetch failed: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
    return []

def delete(id):
    conn = connect()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM data WHERE id=%s", (id,))
            conn.commit()
            return cursor.rowcount > 0 # True if a row was deleted
        except Error as e:
            messagebox.showerror("Database Error", f"Delete failed: {e}")
            conn.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
    return False

def delete_all():

    conn = connect()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM data")
            conn.commit()
            return True
        except Error as e:
            messagebox.showerror("Database Error", f"Mass delete failed: {e}")
            conn.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
    return False

def update(id, name, phone, fees, course, gender):
    conn = connect()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            query = """UPDATE data SET name=%s, phone=%s, fees=%s, course=%s, gender=%s WHERE id=%s"""
            cursor.execute(query, (name, phone, fees, course, gender, id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            messagebox.showerror("Database Error", f"Update failed: {e}")
            conn.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
    return False

def show_data(tree):

    for item in tree.get_children():
        tree.delete(item)
    records = fetch_all()
    for record in records:
        if record and len(record) == 6:
             tree.insert("", "end", values=record)
        else:
            print(f"Skipping record with unexpected format: {record}")

def register_teacher(teacher_id, password):
    conn = connect()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT teacher_id FROM teachers WHERE teacher_id=%s", (teacher_id,))
            if cursor.fetchone():
                messagebox.showerror("Registration Error", "Teacher ID already exists. Please choose a different ID.")
                return False

            cursor.execute("INSERT INTO teachers (teacher_id, password) VALUES (%s, %s)", (teacher_id, password))
            conn.commit()
            return True
        except Error as e:
            messagebox.showerror("Database Error", f"Teacher registration failed: {e}")
            conn.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
    return False

def check_password_exists(password):

    conn = connect()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM teachers WHERE password = %s LIMIT 1", (password,))
            result = cursor.fetchone()
            return result is not None
        except Error as e:
            print(f"Database error checking password: {e}")
            raise e
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    raise ConnectionError("Database connection failed while checking password uniqueness.")


def login_teacher(teacher_id, password):
    conn = connect()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teachers WHERE teacher_id=%s AND password=%s", (teacher_id, password))
            return cursor.fetchone() is not None
        except Error as e:
            messagebox.showerror("Database Error", f"Teacher login failed: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
    return False

def log_operation(teacher_id, operation_type, student_id_affected):
    conn = connect()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            timestamp = datetime.datetime.now()
            query = """INSERT INTO operation_logs (teacher_id, operation_type, student_id_affected, timestamp)
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (teacher_id, operation_type, student_id_affected, timestamp))
            conn.commit()
            return True
        except Error as e:
            print(f"Database Error: Logging operation failed - {e}")
            conn.rollback()
            return False
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
    return False

def fetch_logs():
    conn = connect()
    logs = []
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT log_id, teacher_id, operation_type, student_id_affected, timestamp FROM operation_logs ORDER BY timestamp DESC"
            cursor.execute(query)
            logs_raw = cursor.fetchall()

            formatted_logs = []
            for log in logs_raw:
                timestamp_obj = log['timestamp']
                if isinstance(timestamp_obj, datetime.datetime):
                    log['timestamp_str'] = timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    log['timestamp_str'] = str(timestamp_obj)
                formatted_logs.append(log)

            return formatted_logs
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch logs: {e}")
            return []
        except Exception as e:
             messagebox.showerror("Error", f"An unexpected error occurred fetching logs: {e}")
             return []
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()
    return logs
