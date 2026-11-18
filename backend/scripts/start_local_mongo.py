"""Run the project-local MongoDB Community Server on loopback only."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
matches = list((root / ".local" / "mongodb").glob("**/mongod.exe"))
if len(matches) != 1:
    raise SystemExit("Expected one .local/mongodb/**/mongod.exe; see README setup")
data = root / ".local" / "mongo-data"
data.mkdir(parents=True, exist_ok=True)
command = [str(matches[0]), "--dbpath", str(data), "--bind_ip", "127.0.0.1", "--port", "27017"]
print("Starting local MongoDB at 127.0.0.1:27017 (Ctrl+C to stop)", flush=True)
sys.exit(subprocess.call(command))
