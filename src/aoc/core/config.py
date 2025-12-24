from pathlib import Path

import yaml
from platformdirs import user_config_dir
from pydantic import BaseModel, ConfigDict


class Config(BaseModel):
    year: int = 2026

    model_config = ConfigDict(str_max_length=10)

    def set(self, key: str, value: any, save: bool = True):
        try:
            # Cast value to attr type
            attr_type = type(getattr(self, key))
            value = attr_type(value)

            setattr(self, key, value)
            if save:
                self.save_model()
        except AttributeError:
            return None
        return self.get(key)

    def get(self, key: str):
        if not hasattr(self, key):
            return None
        return getattr(self, key)

    def save_model(self):
        config_path = Path(user_config_dir("aoc")) / "config.yaml"
        with config_path.open("w") as f:
            yaml.dump(self.dict(), f, default_flow_style=False)


def load_config() -> Config:
    config_path = Path(user_config_dir("aoc")) / "config.yaml"

    if config_path.exists():
        with config_path.open("r") as f:
            config_data = yaml.safe_load(f) or {}
    else:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_data = {}
    return Config(**config_data)
