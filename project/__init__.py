# Make the config package importable
from config.settings import verify_config

# Verify configuration on import
config_valid = verify_config()