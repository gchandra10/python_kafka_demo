import yaml


def load_config():
    """Load configuration from the YAML file.

    Returns:
        dict: Configuration data.
    """
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)


config = load_config()


def get_credentials():
    return (
        config["kafka_credentials"]["sasl_plain_username"],
        config["kafka_credentials"]["sasl_plain_password"],
        config["kafka_credentials"]["broker"],
    )
