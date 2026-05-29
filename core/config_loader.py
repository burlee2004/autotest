from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"


def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def load_config():
    common_config = load_yaml(CONFIG_DIR / "config.yaml")
    env_name = common_config.get("environment", "dev")

    env_file = CONFIG_DIR / f"env.{env_name}.yaml"
    if not env_file.exists():
        raise FileNotFoundError(f"Không tìm thấy file config môi trường: {env_file}")

    env_config = load_yaml(env_file)
    return {**common_config, **env_config}


def get_config():
    return load_config()