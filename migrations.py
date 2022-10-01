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
"12": "ALTER TABLE users ADD COLUMN user_token CHAR(100)",
"13": "ALTER TABLE harvests ADD COLUMN userplant_id INT",
"14": "ALTER TABLE harvests ADD COLUMN garden_id INT",
"15": "INSERT INTO plants (name, description, info_url) VALUES ('Green Beans', 'immature beans, in bush and pole variety.', 'www.google.com')",
"16": "INSERT INTO varietys (plant_id, name, description, info_url) VALUES (1, 'Rattle Snake Beans', 'old hairloom Pole variety, can be eaten as green bean or dry bean. very prolific.', 'www.google.com')",
"17": "INSERT INTO user_gardens (user_id, created_at, updated_at, name, description, layout) VALUES (1,'9/14/2022','9/14/2022','backyard garden', '', '[[0,0,0,0],[0,0,0,0]]')",
"18": "INSERT INTO user_plants (user_id, plant_id, variety_id, garden_id, created_at, updated_at, name, description) VALUES (1,1,1,1,'9/14/2022','9/14/2022','My Beans','In the back of garden')",
"19": "INSERT INTO harvests (user_id, plant_id, userplant_id, garden_id, harvested_at, quantity, pound, ounce, notes) VALUES (1,1,1,1,'9/14/2022',1,1,5,'lots of beans')",
"20": "ALTER TABLE harvests ADD COLUMN metadata TEXT"}

unrun_migrations = {}
