"""Extract the official MongoDB Community ZIP into ignored .local/mongodb."""
from pathlib import Path
from zipfile import ZipFile

root = Path(__file__).resolve().parents[2]
archive = root / ".local" / "mongodb.zip"
destination = root / ".local" / "mongodb"
if not archive.is_file():
    raise SystemExit(f"Missing {archive}")
destination.mkdir(parents=True, exist_ok=True)
with ZipFile(archive) as bundle:
    for member in bundle.infolist():
        resolved = (destination / member.filename).resolve()
        if not resolved.is_relative_to(destination.resolve()):
            raise SystemExit(f"Unsafe archive path: {member.filename}")
    bundle.extractall(destination)
servers = list(destination.glob("**/mongod.exe"))
if len(servers) != 1:
    raise SystemExit(f"Expected one mongod.exe, found {len(servers)}")
print(f"MongoDB server ready: {servers[0]}")
