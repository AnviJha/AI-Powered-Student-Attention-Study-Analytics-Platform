"""Run the opt-in MongoDB integration test against the configured local server."""
import os
from pathlib import Path
import subprocess
import sys

backend = Path(__file__).resolve().parents[1]
environment = os.environ.copy()
environment["RUN_REAL_MONGO_TESTS"] = "1"
raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", "-q", "tests/test_real_mongo.py"], cwd=backend, env=environment))
