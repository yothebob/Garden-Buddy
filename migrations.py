total_migrations = {
"0": "CREATE TABLE users (name CHAR(100),username CHAR(150), password CHAR(150), is_active INT DEFAULT 1, is_anonymous INT DEFAULT 0, is_authenticated INT DEFAULT 1)",
"1": "CREATE TABLE plants (name CHAR(100), description TEXT, info_url CHAR(150))",
"2": "CREATE TABLE harvests (user_id INT, plant_id INT, harvested_at CHAR(150), quantity INT, pound INT, ounce INT, notes TEXT)",
"3": "INSERT INTO users (name, username, password) VALUES ('admin', 'admin', 'admin')",
"4": "CREATE TABLE varietys (name CHAR(100), plant_id INT, description TEXT, info_url CHAR(150))",
"5": "CREATE TABLE user_plants (user_id INT, plant_id INT, variety_id INT, garden_id INT, created_at CHAR(150), updated_at CHAR(150), name CHAR(100), description TEXT, metadata TEXT)",
"6": "CREATE TABLE user_gardens (user_id INT, created_at CHAR(150), updated_at CHAR(150), name CHAR(100), description TEXT, layout TEXT, metadata TEXT)",
"7": "ALTER TABLE plants add column foot_size CHAR(20)",
"8": "ALTER TABLE varietys add column foot_size CHAR(20)",
"9": "ALTER TABLE user_plants add column foot_size CHAR(20)",
"10": "CREATE TABLE user_plants_update (userplant_id INT, plant_id INT, variety_id INT, garden_id INT, created_at CHAR(150), name CHAR(150), description TEXT, metadata TEXT)",
"11": "CREATE TABLE user_garden_update (created_at CHAR(150), name CHAR(150), description TEXT, layout TEXT, metadata TEXT)",
"12": "ALTER TABLE users ADD COLUMN user_token CHAR(100)"}

unrun_migrations = {}
