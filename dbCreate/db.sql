-- Database: flashdb

DROP DATABASE IF EXISTS flashdb;

CREATE DATABASE flashdb
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_IN'
    LC_CTYPE = 'en_IN'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
