# SDD-Demo Development Guidelines

注意：除憲章外，使用者面向的規格與說明文件應以繁體中文 (zh-TW) 撰寫。

Auto-generated from all feature plans. Last updated: 2025-12-08

## Active Technologies

- Python 3.14 (use project's virtualenv; compatible with macOS dev and Linux deploy) + FastAPI (HTTP API), SQLAlchemy (ORM), Alembic (migrations), Jinja2 (email templates), `smtplib` (standard library) for synchronous SMTP in MVP (001-release-announcements)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.14 (use project's virtualenv; compatible with macOS dev and Linux deploy): Follow standard conventions

## Recent Changes

- 001-release-announcements: Added Python 3.14 (use project's virtualenv; compatible with macOS dev and Linux deploy) + FastAPI (HTTP API), SQLAlchemy (ORM), Alembic (migrations), Jinja2 (email templates), `smtplib` (standard library) for synchronous SMTP in MVP

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
