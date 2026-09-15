-- Listrix database schema (MySQL 8+)
-- Note: the backend creates these tables automatically on startup via
-- SQLAlchemy (see database.py / main.py). This file is a reference /
-- for anyone who wants to provision the schema manually or via a
-- migration tool instead.

CREATE DATABASE IF NOT EXISTS listrix_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE listrix_db;

CREATE TABLE IF NOT EXISTS contacts (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  email       VARCHAR(255) NOT NULL,
  phone       VARCHAR(50)  NULL,
  message     TEXT         NULL,
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_contacts_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS knowledge_base (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  title       VARCHAR(255) NOT NULL,
  content     TEXT         NOT NULL,
  category    VARCHAR(100) NULL,
  INDEX idx_knowledge_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
