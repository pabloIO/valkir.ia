from chatterbot.storage.mongodb import MongoDatabaseAdapter
from config.config import env
mongo = MongoDatabaseAdapter(database=env['NO_SQL_CONF']['DB_NAME'], database_uri=env['NO_SQL_CONF']['DB_URI'])