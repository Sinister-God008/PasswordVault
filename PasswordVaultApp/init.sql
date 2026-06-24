/*This file basically creates the database on first start and readies the database for entries*/

/*Creating the User table*/
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

/*Creating the folders table that will store the folders data*/
CREATE TABLE IF NOT EXISTS folders (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    name VARCHAR(255) NOT NULL,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

/*Creating the Vault_entries table that stores the folder wise data for passwords,apis,etc,.*/
CREATE TABLE IF NOT EXISTS vault_entries (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    folder_id INTEGER
        REFERENCES folders(id)
        ON DELETE SET NULL,

    type VARCHAR(50) NOT NULL,

    name VARCHAR(255) NOT NULL,

    username VARCHAR(255),

    url TEXT,

    notes TEXT,

    encrypted_secret TEXT NOT NULL,

    strength_score INTEGER DEFAULT 0,

    is_breached BOOLEAN DEFAULT FALSE,

    rotation_interval_days INTEGER,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    last_changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

/*This stores the log data in table*/
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE,

    action VARCHAR(100) NOT NULL,

    resource_name VARCHAR(255),

    ip_address VARCHAR(45),

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

/*Creating index for easy traversal to access data efficiently*/
CREATE INDEX IF NOT EXISTS idx_vault_user
ON vault_entries(user_id);

CREATE INDEX IF NOT EXISTS idx_folder_user
ON folders(user_id);

CREATE INDEX IF NOT EXISTS idx_audit_user
ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_vault_security
ON vault_entries(user_id, is_breached, strength_score);
CREATE INDEX IF NOT EXISTS idx_vault_folder
ON vault_entries(folder_id);
