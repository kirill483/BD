CREATE TABLE military_offices (
    military_office_id SERIAL PRIMARY KEY,
    address TEXT NOT NULL,
    count_of_liables int not null
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hash_password TEXT NOT NULL,
    role VARCHAR(50) NOT NULL
);

CREATE TABLE liables (
    user_id INTEGER NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    military_office_id INTEGER NOT NULL,
    FOREIGN KEY (military_office_id) REFERENCES military_offices(military_office_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE workers (
    user_id INTEGER NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    military_office_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (military_office_id) REFERENCES military_offices(military_office_id)
);

CREATE TABLE summons (
    summon_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    creation_date DATE NOT NULL,
    appearance_date DATE NOT NULL,
    description TEXT,
    worker_id INTEGER NOT NULL,
    military_office_id INTEGER NOT NULL,
    FOREIGN KEY (military_office_id) REFERENCES military_offices(military_office_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (worker_id) REFERENCES users(user_id)
);

CREATE TABLE health_reports (
    report_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    worker_id INTEGER NOT NULL,
    health_level VARCHAR(50) NOT NULL,
    health_description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (worker_id) REFERENCES users(user_id)
);

CREATE TABLE health_data (
    data_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE OR REPLACE FUNCTION increment_count_of_liables()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE military_offices
    SET count_of_liables = count_of_liables + 1
    WHERE military_office_id = NEW.military_office_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER liables_insert_trigger
AFTER INSERT ON liables
FOR EACH ROW
EXECUTE FUNCTION increment_count_of_liables();

