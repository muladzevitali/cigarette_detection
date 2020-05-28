from .config_parser import (Application, FaissConfiguration, Media, ApplicationDatabase)

# Define configuration for further usage
app_config = Application
database_config = ApplicationDatabase
faiss_config = FaissConfiguration
media_config = Media
# Prefix for all tables in the app context
table_prefix = database_config.table_prefix
