from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    """Establish database connection with retry logic"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'db'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', 'example'),
                database=os.getenv('DB_NAME', 'test_db')
            )
            return connection
        except mysql.connector.Error as err:
            if attempt == max_retries - 1:
                raise err
            print(f"Database connection failed (attempt {attempt + 1}/{max_retries}): {err}")
            time.sleep(retry_delay)
    
    return None

def init_database():
    """Initialize database with sample data"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Create users table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            sample_users = [
                ('Alice Johnson', 'alice@example.com'),
                ('Bob Smith', 'bob@example.com'),
                ('Charlie Brown', 'charlie@example.com'),
                ('Diana Prince', 'diana@example.com')
            ]
            
            cursor.executemany(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                sample_users
            )
            connection.commit()
            print("Sample users inserted successfully")
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Database initialization error: {err}")

@app.route('/')
def index():
    """Home page with database status"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Get database info
        cursor.execute("SELECT VERSION()")
        db_version = cursor.fetchone()[0]
        
        # Get user count
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        # Get recent users
        cursor.execute("SELECT name, email, created_at FROM users ORDER BY created_at DESC LIMIT 5")
        recent_users = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('index.html', 
                             db_version=db_version,
                             user_count=user_count,
                             recent_users=recent_users,
                             db_status="Connected")
        
    except Exception as e:
        return render_template('index.html', 
                             error=str(e),
                             db_status="Disconnected")

@app.route('/users', methods=['GET'])
def get_users():
    """API endpoint to get all users"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'status': 'success',
            'count': len(users),
            'users': users
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/users', methods=['POST'])
def add_user():
    """API endpoint to add a new user"""
    try:
        data = request.json
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'status': 'error', 'message': 'Name and email are required'}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (data['name'], data['email'])
        )
        connection.commit()
        user_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'status': 'success',
            'message': 'User added successfully',
            'user_id': user_id
        })
        
    except mysql.connector.Error as err:
        return jsonify({
            'status': 'error',
            'message': f'Database error: {err}'
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        connection.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'service': 'flask-app'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 503

if __name__ == "__main__":
    # Initialize database on startup
    print("Initializing database...")
    init_database()
    
    # Start Flask app
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )
