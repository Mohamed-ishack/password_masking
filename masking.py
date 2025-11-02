import os
from dotenv import load_dotenv
from getpass import getpass
from cryptography.fernet import Fernet


DATA_PATH = os.getenv("DATA_PATH")
SEP = "|"
load_dotenv()




# def load_key(path=KEY_PATH):
#     if not os.path.exists(path):
#         return write_key(path)
#     with open(path, 'rb') as f:
#         return f.read()
# # master_pwd = input("Enter a master password : ")
key = os.getenv("encryption_key")
fer = Fernet(key)

def add():
    name = input("Enter Account Name: ").strip()
    pwd = getpass("Enter Password: ")
    token = fer.encrypt(pwd.encode()).decode()
    with open(DATA_PATH, "a", encoding="utf-8") as f:
        f.write(f"{name}{SEP}{token}\n")
    print("Saved.")

def view(mask=True)-> None:
    if not os.path.exists(DATA_PATH):
        print("No passwords stored yet.")
        return None
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    if not lines:
        print("No passwords stored yet.")
        return None
    for i, line in enumerate(lines, start=1):
        try:
            user, token = line.split(SEP, 1)
            user = user.strip()
            token = token.strip()
            # Decrypt token to get real password
            pwd = fer.decrypt(token.encode()).decode()
            display = ("*" * len(pwd)) if mask else pwd
            print(f"{i}. User: {user}  | Password: {display}")
        except Exception as e:
            print(f"{i}. Corrupt line or invalid token: {line!r}  (error: {e})")

def reveal_one():
    """Ask for index or account name to reveal the actual password."""
    if not os.path.exists(DATA_PATH):
        print("No passwords stored.")
        return
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    if not lines:
        print("No passwords stored.")
        return
    query = input("Enter entry number or account name to reveal: ").strip()
    # try by index
    try:
        idx = int(query) - 1
        line = lines[idx]
    except Exception:
        # try by name
        found = None
        for ln in lines:
            if ln.split(SEP, 1)[0].strip().lower() == query.lower():
                found = ln
                break
        if not found:
            print("No matching entry found.")
            return
        line = found
    try:
        user, token = line.split(SEP, 1)
        pwd = fer.decrypt(token.strip().encode()).decode()
        print(f"Account: {user.strip()}  | Password: {pwd}")
    except Exception as e:
        print("Could not decrypt/display password:", e)

def main():
    while True:
        mode = input("\n(view, add, reveal, q=quit): ").strip().lower()
        if mode == "q":
            break
        elif mode == "view":
            view(mask=True)
        elif mode == "add":
            add()
        elif mode == "reveal":
            reveal_one()
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()