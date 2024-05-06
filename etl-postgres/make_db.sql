CREATE DATABASE tutoring_db;

\connect tutoring_db;

SET timezone = 'America/New_York';

CREATE TABLE lesson(
    studentid INTEGER,
    timeid INTEGER,
    courseid INTEGER,
    duration INTEGER,
    effective_rate FLOAT,
    paymethodid INTEGER,
    rating FLOAT,
    subjectid INTEGER,
    PRIMARY KEY(studentid, timeid)
);

CREATE TABLE student(
    studentid INTEGER PRIMARY KEY,
    student_name TEXT,
    timezone INTEGER,
    account TEXT,
    source TEXT,
    email TEXT,
    level TEXT
);

CREATE TABLE time(
    timeid INTEGER PRIMARY KEY,
    start_timestamp TIMESTAMP,
    year INTEGER,
    month INTEGER,
    week INTEGER,
    day INTEGER
);

CREATE TABLE subject(
    subjectid INTEGER PRIMARY KEY,
    subject TEXT
);

CREATE TABLE pay_method(
    paymethodid INTEGER PRIMARY KEY,
    pay_method TEXT,
    tax_rate FLOAT
);


CREATE USER tutor WITH PASSWORD 'tutorpass';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tutor;

