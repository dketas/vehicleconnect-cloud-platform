import os

def pytest_configure():
    # Local tests run on your Mac, so Postgres is reachable via localhost:5432
    os.environ.setdefault(
        "DATABASE_URL",
        "postgresql://vc_user:vc_password@localhost:5432/vehicleconnect",
    )
