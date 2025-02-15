from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_FILE = "system_info.db"

# Create the database table if it doesn't exist
def create_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT,  -- ADDED: Task ID column
            system_name TEXT,
            ip_address TEXT,
            cpu_cores INTEGER,
            physical_cores INTEGER
        )
    """)
    conn.commit()
    conn.close()

create_db()  # Ensure table is created

@app.route('/update_system_info', methods=['POST'])
def update_system_info():
    """Receive and store system info in the database."""
    try:
        data = request.json  # Get JSON data from request
        print("Received Data:", data)  # Debugging
        
        task_id = data.get("task_id")  # ADDED: Task ID
        system_name = data.get("system_name")
        ip_address = data.get("ip_address")
        cpu_cores = data.get("cpu_cores")  # Logical (virtual) cores
        physical_cores = data.get("physical_cores")  # Physical cores

        if not all([task_id, system_name, ip_address, cpu_cores, physical_cores]):
            return jsonify({"error": "Missing data"}), 400

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO system_info (task_id, system_name, ip_address, cpu_cores, physical_cores)
            VALUES (?, ?, ?, ?, ?)
        """, (task_id, system_name, ip_address, cpu_cores, physical_cores))

        conn.commit()
        conn.close()

        return jsonify({"message": "System info updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_system_info', methods=['GET'])
def get_system_info():
    """Retrieve stored system info from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM system_info")
    data = cursor.fetchall()
    conn.close()

    return jsonify({"systems": data})

if __name__ == '__main__':
    app.run(debug=True)  # Run Flask on default port 5000
