# tests/test_config.py
def test_load_config(config):
    assert config["environment"] in ["dev", "staging"]
    assert "base_url" in config
    assert "browser" in config