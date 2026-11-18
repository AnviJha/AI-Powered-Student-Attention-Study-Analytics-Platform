"""Create a local .env once. Deployment uses the same variable names."""
from pathlib import Path
import secrets

backend = Path(__file__).resolve().parents[1]
target = backend / ".env"
if target.exists():
    print("Existing backend/.env left unchanged")
else:
    example = (backend / ".env.example").read_text(encoding="utf-8")
    example = example.replace("replace-with-a-long-random-secret", secrets.token_urlsafe(48))
    target.write_text(example, encoding="utf-8")
    print("Created backend/.env with a random JWT secret")
