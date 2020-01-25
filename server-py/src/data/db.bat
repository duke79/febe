@echo off
REM set PYTHONPATH=%~dp0/VilokanLabs
REM python %~dp0\VilokanLabs\data\alembic\__main__.py %~dp0\Output
REM SET /p sqlite_path=<Output
REM DEL Output
REM REM echo %errorlevel%
REM sqlite_web %sqlite_path%

start pg_ctl -D "C:\Program Files\PostgreSQL\11\data" start