""" 
Sets up a new application by initializing the database.

This script, when run directly, performs the following actions:
- Imports the database object (`db`) from the `app` module.
- Creates an empty database by dropping existing tables (if any)
   and creating new tables based on the application's models.
- Prints a confirmation message upon successful initialization.

Raises:
    Exception: Any exceptions encountered during database initialization.
"""
from app import db
import logging
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        db.create_empty_db()
        logger.info('Created an empty DB')
    except Exception as e:
        logger.error(f'Error creating database: {e}')
