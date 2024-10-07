import pytest
from sqlalchemy.testing.plugin.plugin_base import config

from app.config import get_config



def test_config_loading(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgresql+psycopg2://')

    config = get_config()
    assert config is not None, "Config shouldnt be None"
    assert config.DATABASE_URL == 'postgresql+psycopg2://', 'DATABASE_URL should be postgresql+psycopg2://'