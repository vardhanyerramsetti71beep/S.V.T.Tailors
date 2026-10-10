import os
import json
import re
import hashlib
from datetime import datetime
import pymysql

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'db_config.json')

def hash_password(password):
    if not password:
        return ""
    return hashlib.sha256(password.strip().encode('utf-8')).hexdigest()

def load_config():
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", 3306)),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", "customers")
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"[DB Warning] Could not read db_config.json: {e}")
    return config

def get_connection(use_database=True):
    cfg = load_config()
    db_name = cfg["database"] if use_database else None
    return pymysql.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def test_connection():
    try:
        conn = get_connection(use_database=True)
        with conn.cursor() as cur:
            cur.execute("SELECT DATABASE() as db, VERSION() as ver;")
            row = cur.fetchone() or {"db": "customers", "ver": "8.0"}
            cur.execute("SHOW TABLES;")
            tables = [list(t.values())[0] for t in cur.fetchall()]
        conn.close()
        return {
            "success": True,
            "message": f"Successfully connected to MySQL database '{row['db']}' (v{row['ver']})",
            "tables": tables
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "hint": "Please set your MySQL password in 'db_config.json' or environment variables."
        }

def ensure_user_auth_columns(cur, table_name="users"):
    """Adds username and password columns to users table if they don't already exist"""
    try:
        cur.execute(f"DESC `{table_name}`;")
        cols = [c['Field'].lower() for c in cur.fetchall()]
        if 'username' not in cols:
            cur.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `username` VARCHAR(100) UNIQUE AFTER `mobile`;")
            print(f"[DB] Added 'username' column to {table_name}")
        if 'password' not in cols:
            cur.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `password` VARCHAR(255) AFTER `username`;")
            print(f"[DB] Added 'password' column to {table_name}")
    except Exception as e:
        print(f"[DB Notice] ensure_user_auth_columns: {e}")

def init_db():
    cfg = load_config()
    db_name = cfg["database"]
    
    # 1. Ensure database exists
    conn = get_connection(use_database=False)
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
    conn.close()

    # 2. Ensure tables exist matching user schema: users, bookings, measurements
    conn = get_connection(use_database=True)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS `users` (
                `user_id` INT PRIMARY KEY,
                `name` VARCHAR(200) NOT NULL,
                `mobile` VARCHAR(20) NOT NULL,
                `username` VARCHAR(100) UNIQUE,
                `password` VARCHAR(255),
                `is_deleted` BOOLEAN DEFAULT FALSE,
                `deletion_reason` VARCHAR(250) DEFAULT NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        ensure_user_auth_columns(cur, "users")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS `bookings` (
                `booking_id` SERIAL PRIMARY KEY,
                `user_id` INT NOT NULL,
                `locality` VARCHAR(250) NOT NULL,
                `pref_date` DATE NOT NULL,
                `pref_time` TIME NOT NULL,
                `garments` TEXT,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS `measurements` (
                `measurement_id` INT PRIMARY KEY,
                `user_id` INT UNIQUE NOT NULL,
                `shirt_size` VARCHAR(20),
                `pant_size` VARCHAR(20),
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
            );
        """)
    conn.close()
    return True

def parse_time_slot(time_str):
    """Converts strings like 'Morning (10:00 AM - 1:00 PM)' to valid TIME (HH:MM:SS)"""
    if not time_str:
        return "10:00:00"
    
    clean = time_str.strip()
    if re.match(r'^\d{1,2}:\d{2}(:\d{2})?$', clean):
        parts = clean.split(':')
        if len(parts) == 2:
            return f"{int(parts[0]):02d}:{parts[1]}:00"
        return f"{int(parts[0]):02d}:{parts[1]}:{parts[2]}"

    lower = clean.lower()
    if 'morning' in lower:
        return "10:00:00"
    elif 'afternoon' in lower:
        return "14:00:00"
    elif 'evening' in lower:
        return "17:00:00"

    match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)?', clean, re.IGNORECASE)
    if match:
        hr = int(match.group(1))
        mn = match.group(2)
        ampm = match.group(3)
        if ampm and ampm.upper() == 'PM' and hr < 12:
            hr += 12
        elif ampm and ampm.upper() == 'AM' and hr == 12:
            hr = 0
        return f"{hr:02d}:{mn}:00"

    return "10:00:00"

def parse_date(date_str):
    if not date_str:
        return datetime.now().strftime("%Y-%m-%d")
    try:
        dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d")

def get_users_table_name(cur):
    cur.execute("SHOW TABLES;")
    tables = [list(t.values())[0].lower() for t in cur.fetchall()]
    return "users" if "users" in tables else "user"

def get_garments_column_name(cur):
    cur.execute("DESC bookings;")
    cols = [c['Field'].lower() for c in cur.fetchall()]
    return "garments" if "garments" in cols else "garnments"

def register_user(name, mobile, locality, username, password, pref_date=None, pref_time=None, garments=None, shirt_size=None, pant_size=None):
    clean_name = str(name).strip() or "Valued Customer"
    clean_mobile = re.sub(r'[^\d]', '', str(mobile))[-10:] or str(mobile).strip()
    clean_username = str(username).strip().lower()
    hashed_pwd = hash_password(password)
    clean_locality = str(locality).strip() or "Governorpet, Vijayawada"

    if not clean_username:
        return {"success": False, "error": "Username is required"}
    if not password:
        return {"success": False, "error": "Password is required"}
    if not clean_mobile:
        return {"success": False, "error": "Mobile number is required"}

    conn = get_connection(use_database=True)
    try:
        with conn.cursor() as cur:
            users_table = get_users_table_name(cur)
            garments_col = get_garments_column_name(cur)
            ensure_user_auth_columns(cur, users_table)

            # Check if username already taken
            cur.execute(f"SELECT user_id, username, mobile FROM `{users_table}` WHERE `username` = %s LIMIT 1;", (clean_username,))
            user_by_uname = cur.fetchone()
            if user_by_uname:
                return {
                    "success": False,
                    "already_exists": True,
                    "error": f"Username '{clean_username}' is already registered. Directing you to Sign In...",
                    "identifier": clean_username
                }

            # Check if mobile exists
            cur.execute(f"SELECT user_id, username, password, mobile FROM `{users_table}` WHERE `mobile` = %s LIMIT 1;", (clean_mobile,))
            existing_user = cur.fetchone()

            if existing_user and existing_user.get("password"):
                return {
                    "success": False,
                    "already_exists": True,
                    "error": f"An account is already created for mobile {clean_mobile}! Directing you to Sign In...",
                    "identifier": existing_user.get("username") or clean_mobile
                }
            elif existing_user:
                user_id = existing_user["user_id"]
                cur.execute(
                    f"UPDATE `{users_table}` SET `name` = %s, `username` = %s, `password` = %s WHERE `user_id` = %s;",
                    (clean_name, clean_username, hashed_pwd, user_id)
                )
            else:
                cur.execute(f"SELECT COALESCE(MAX(`user_id`), 0) + 1 AS next_id FROM `{users_table}`;")
                id_row = cur.fetchone() or {}
                user_id = id_row.get("next_id", 1)
                cur.execute(
                    f"""
                    INSERT INTO `{users_table}` (`user_id`, `name`, `mobile`, `username`, `password`, `is_deleted`)
                    VALUES (%s, %s, %s, %s, %s, FALSE);
                    """,
                    (user_id, clean_name, clean_mobile, clean_username, hashed_pwd)
                )

            booking_id = None
            # If garments or preferred date/time are provided, record an initial booking
            if garments or pref_date:
                valid_date = parse_date(pref_date)
                valid_time = parse_time_slot(pref_time)
                clean_garments = str(garments or "Bespoke Gents Wear Consultation").strip()

                cur.execute(
                    f"""
                    INSERT INTO `bookings` (`user_id`, `locality`, `pref_date`, `pref_time`, `{garments_col}`)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (user_id, clean_locality, valid_date, valid_time, clean_garments)
                )
                booking_id = cur.lastrowid

            # Save measurements if provided
            if shirt_size or pant_size:
                clean_shirt = str(shirt_size).strip()[:20] if shirt_size else None
                clean_pant = str(pant_size).strip()[:20] if pant_size else None

                cur.execute("SELECT measurement_id FROM `measurements` WHERE `user_id` = %s LIMIT 1;", (user_id,))
                m_row = cur.fetchone()
                if m_row:
                    cur.execute(
                        "UPDATE `measurements` SET `shirt_size` = COALESCE(%s, `shirt_size`), `pant_size` = COALESCE(%s, `pant_size`) WHERE `user_id` = %s;",
                        (clean_shirt, clean_pant, user_id)
                    )
                else:
                    cur.execute("SELECT COALESCE(MAX(`measurement_id`), 0) + 1 AS next_m_id FROM `measurements`;")
                    mid_row = cur.fetchone() or {}
                    next_m_id = mid_row.get("next_m_id", 1)
                    cur.execute(
                        "INSERT INTO `measurements` (`measurement_id`, `user_id`, `shirt_size`, `pant_size`) VALUES (%s, %s, %s, %s);",
                        (next_m_id, user_id, clean_shirt, clean_pant)
                    )

        return {
            "success": True,
            "message": "Account created successfully!",
            "user": {
                "user_id": user_id,
                "name": clean_name,
                "mobile": clean_mobile,
                "username": clean_username,
                "locality": clean_locality
            },
            "booking_id": booking_id
        }
    finally:
        conn.close()

def login_user(username_or_mobile, password):
    clean_identifier = str(username_or_mobile).strip()
    hashed_pwd = hash_password(password)

    if not clean_identifier or not password:
        return {"success": False, "error": "Username/Mobile and password are required"}

    conn = get_connection(use_database=True)
    try:
        with conn.cursor() as cur:
            users_table = get_users_table_name(cur)
            garments_col = get_garments_column_name(cur)
            ensure_user_auth_columns(cur, users_table)

            digits = re.sub(r'[^\d]', '', clean_identifier)
            query_cond = "`username` = %s"
            params = [clean_identifier.lower()]
            if len(digits) >= 10:
                query_cond += " OR `mobile` = %s OR `mobile` LIKE %s"
                params.extend([digits, f"%{digits[-10:]}%"])

            sql = f"""
                SELECT `user_id`, `name`, `mobile`, `username`, `password`
                FROM `{users_table}`
                WHERE ({query_cond}) AND (`is_deleted` IS NULL OR `is_deleted` = FALSE)
                LIMIT 1;
            """
            cur.execute(sql, tuple(params))
            user = cur.fetchone()

            if not user:
                return {"success": False, "error": "No account found matching this username or phone number"}

            stored_pwd = user.get("password") or ""
            if stored_pwd != hashed_pwd and stored_pwd != password.strip():
                return {"success": False, "error": "Incorrect password. Please try again."}

            user_id = user["user_id"]

            cur.execute(
                f"""
                SELECT `booking_id`, `locality`, DATE_FORMAT(`pref_date`, '%%Y-%%m-%%d') AS pref_date,
                       TIME_FORMAT(`pref_time`, '%%h:%%i %%p') AS pref_time, `{garments_col}` AS garments
                FROM `bookings`
                WHERE `user_id` = %s
                ORDER BY `booking_id` DESC;
                """,
                (user_id,)
            )
            bookings = cur.fetchall()

            cur.execute(
                "SELECT `shirt_size`, `pant_size`, DATE_FORMAT(`updated_at`, '%%Y-%%m-%%d') as updated_at FROM `measurements` WHERE `user_id` = %s LIMIT 1;",
                (user_id,)
            )
            measurements = cur.fetchone()

            return {
                "success": True,
                "message": f"Welcome back, {user['name']}!",
                "user": {
                    "user_id": user["user_id"],
                    "name": user["name"],
                    "mobile": user["mobile"],
                    "username": user.get("username") or user["mobile"]
                },
                "bookings": bookings,
                "measurements": measurements
            }
    finally:
        conn.close()

def reset_password(username_or_mobile, new_password):
    clean_identifier = str(username_or_mobile).strip()
    if not clean_identifier:
        return {"success": False, "error": "Registered mobile number or username is required"}
    if not new_password or len(str(new_password).strip()) < 4:
        return {"success": False, "error": "New password must be at least 4 characters long"}

    hashed_pwd = hash_password(new_password)
    digits = re.sub(r'[^\d]', '', clean_identifier)

    conn = get_connection(use_database=True)
    try:
        with conn.cursor() as cur:
            users_table = get_users_table_name(cur)
            ensure_user_auth_columns(cur, users_table)

            query_cond = "`username` = %s"
            params = [clean_identifier.lower()]
            if len(digits) >= 10:
                query_cond += " OR `mobile` = %s OR `mobile` LIKE %s"
                params.extend([digits, f"%{digits[-10:]}%"])

            sql = f"""
                SELECT `user_id`, `name`, `mobile`, `username`
                FROM `{users_table}`
                WHERE ({query_cond}) AND (`is_deleted` IS NULL OR `is_deleted` = FALSE)
                LIMIT 1;
            """
            cur.execute(sql, tuple(params))
            user = cur.fetchone()

            if not user:
                return {"success": False, "error": f"No account found matching '{clean_identifier}'."}

            user_id = user["user_id"]
            cur.execute(
                f"UPDATE `{users_table}` SET `password` = %s WHERE `user_id` = %s;",
                (hashed_pwd, user_id)
            )

        return {
            "success": True,
            "message": f"Password reset successfully for {user.get('name') or clean_identifier}!",
            "identifier": user.get("username") or user.get("mobile")
        }
    finally:
        conn.close()

def save_booking(name, mobile, locality, pref_date, pref_time, garnments=None, garments=None, shirt_size=None, pant_size=None):
    clean_mobile = re.sub(r'[^\d]', '', str(mobile))[-10:] or str(mobile).strip()
    clean_name = str(name).strip() or "Valued Customer"
    clean_locality = str(locality).strip() or "Governorpet, Vijayawada"
    valid_date = parse_date(pref_date)
    valid_time = parse_time_slot(pref_time)
    
    garments_text = garments or garnments or "Bespoke Garments"
    clean_garments = str(garments_text).strip()

    conn = get_connection(use_database=True)
    try:
        with conn.cursor() as cur:
            users_table = get_users_table_name(cur)
            garments_col = get_garments_column_name(cur)

            cur.execute(f"SELECT user_id FROM `{users_table}` WHERE `mobile` = %s LIMIT 1;", (clean_mobile,))
            user_row = cur.fetchone()
            
            if user_row:
                user_id = user_row["user_id"]
                cur.execute(f"UPDATE `{users_table}` SET `name` = %s WHERE `user_id` = %s;", (clean_name, user_id))
            else:
                cur.execute(f"SELECT COALESCE(MAX(`user_id`), 0) + 1 AS next_id FROM `{users_table}`;")
                id_row = cur.fetchone() or {}
                user_id = id_row.get("next_id", 1)
                cur.execute(
                    f"INSERT INTO `{users_table}` (`user_id`, `name`, `mobile`, `is_deleted`) VALUES (%s, %s, %s, FALSE);",
                    (user_id, clean_name, clean_mobile)
                )

            cur.execute(
                f"""
                INSERT INTO `bookings` (`user_id`, `locality`, `pref_date`, `pref_time`, `{garments_col}`)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (user_id, clean_locality, valid_date, valid_time, clean_garments)
            )
            booking_id = cur.lastrowid

            if shirt_size or pant_size:
                clean_shirt = str(shirt_size).strip()[:20] if shirt_size else None
                clean_pant = str(pant_size).strip()[:20] if pant_size else None

                cur.execute("SELECT measurement_id FROM `measurements` WHERE `user_id` = %s LIMIT 1;", (user_id,))
                m_row = cur.fetchone()
                if m_row:
                    cur.execute(
                        """
                        UPDATE `measurements` 
                        SET `shirt_size` = COALESCE(%s, `shirt_size`),
                            `pant_size` = COALESCE(%s, `pant_size`),
                            `updated_at` = CURRENT_TIMESTAMP
                        WHERE `user_id` = %s;
                        """,
                        (clean_shirt, clean_pant, user_id)
                    )
                else:
                    cur.execute("SELECT COALESCE(MAX(`measurement_id`), 0) + 1 AS next_m_id FROM `measurements`;")
                    mid_row = cur.fetchone() or {}
                    next_m_id = mid_row.get("next_m_id", 1)
                    cur.execute(
                        """
                        INSERT INTO `measurements` (`measurement_id`, `user_id`, `shirt_size`, `pant_size`)
                        VALUES (%s, %s, %s, %s);
                        """,
                        (next_m_id, user_id, clean_shirt, clean_pant)
                    )

        return {
            "success": True,
            "booking_id": booking_id,
            "user_id": user_id,
            "name": clean_name,
            "mobile": clean_mobile,
            "locality": clean_locality,
            "pref_date": valid_date,
            "pref_time": valid_time,
            "garments": clean_garments
        }
    finally:
        conn.close()

def get_bookings(query):
    """Search bookings by phone number or booking ID"""
    clean_query = str(query).strip()
    digits = re.sub(r'[^\d]', '', clean_query)
    
    conn = get_connection(use_database=True)
    try:
        with conn.cursor() as cur:
            users_table = get_users_table_name(cur)
            garments_col = get_garments_column_name(cur)

            sql = f"""
                SELECT 
                    b.booking_id,
                    u.user_id,
                    u.name,
                    u.mobile,
                    b.locality,
                    DATE_FORMAT(b.pref_date, '%%Y-%%m-%%d') AS pref_date,
                    TIME_FORMAT(b.pref_time, '%%h:%%i %%p') AS pref_time,
                    b.{garments_col} AS garments,
                    m.shirt_size,
                    m.pant_size,
                    DATE_FORMAT(u.created_at, '%%Y-%%m-%%d %%H:%%i') AS user_created_at
                FROM `bookings` b
                JOIN `{users_table}` u ON b.user_id = u.user_id
                LEFT JOIN `measurements` m ON u.user_id = m.user_id
                WHERE 1=0
            """
            params = []
            
            if digits:
                sql += " OR b.booking_id = %s OR u.mobile LIKE %s"
                params.extend([digits, f"%{digits[-10:]}%"])
            
            if clean_query:
                sql += " OR u.name LIKE %s"
                params.append(f"%{clean_query}%")
                
            sql += " ORDER BY b.booking_id DESC LIMIT 10;"
            
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()

if __name__ == '__main__':
    res = test_connection()
    print(json.dumps(res, indent=2))