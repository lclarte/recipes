#!/usr/bin/env python3
"""Create a user. Usage: python create_user.py <username> <password>"""
import sys
from app.database import SessionLocal, Base, engine
from app.models import User
from app.auth import get_password_hash

Base.metadata.create_all(bind=engine)


def create_user(username: str, password: str) -> None:
    db = SessionLocal()
    try:
        if db.query(User).filter(User.username == username).first():
            print(f"Error: user '{username}' already exists.")
            sys.exit(1)
        db.add(User(username=username, password_hash=get_password_hash(password)))
        db.commit()
        print(f"User '{username}' created.")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_user.py <username> <password>")
        sys.exit(1)
    create_user(sys.argv[1], sys.argv[2])
