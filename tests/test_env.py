from core.config import Config


def test_env_loaded():
    assert Config.DATABASE_PATH.endswith(".db")
