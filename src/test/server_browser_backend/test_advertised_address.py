from server_browser_backend.models.base_models import Chivalry2Ports, Server


def make_server(local_ip_address: str | None = "gameserver.example.test") -> Server:
    return Server(
        unique_id="test-server",
        ip_address="10.167.0.1",
        local_ip_address=local_ip_address,
        ports=Chivalry2Ports(game=3075, a2s=7070, ping=3076),
        password_protected=False,
        last_heartbeat=0.0,
        name="Test server",
        description="",
        current_map="TO_Lionspire",
        player_count=0,
        max_players=64,
        is_verified=False,
        mods=[],
    )


def test_registered_address_is_returned_to_every_client_when_enabled(monkeypatch):
    monkeypatch.setenv("PREFER_REGISTERED_ADDRESS", "true")

    assert make_server().advertised_address("203.0.113.15") == "gameserver.example.test"


def test_upstream_same_address_policy_remains_available(monkeypatch):
    monkeypatch.delenv("PREFER_REGISTERED_ADDRESS", raising=False)
    server = make_server()

    assert server.advertised_address("203.0.113.15") == "10.167.0.1"
    assert server.advertised_address("10.167.0.1") == "gameserver.example.test"


def test_observed_address_is_fallback_when_no_registered_address(monkeypatch):
    monkeypatch.setenv("PREFER_REGISTERED_ADDRESS", "true")

    assert make_server(None).advertised_address("203.0.113.15") == "10.167.0.1"
