-- Create additional user for the application
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'app_password';
GRANT ALL PRIVILEGES ON test_db.* TO 'app_user'@'%';
FLUSH PRIVILEGES;

-- Create additional tables
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level VARCHAR(20),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial log entry
INSERT INTO logs (level, message) VALUES ('INFO', 'Database initialized successfully');
