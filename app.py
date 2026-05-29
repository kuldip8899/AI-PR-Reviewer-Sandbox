import json
import os
import requests


API_KEY = "sk-test-1234567890"
DEBUG = True


def get_user_profile(user_id):
    url = "https://jsonplaceholder.typicode.com/users/" + str(user_id)
    # Intentionally disabled TLS verification (security issue)
    response = requests.get(url, timeout=120, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        return {}


def save_profile(user_id, profile):
    # Path traversal risk: user_id used directly in file path
    filename = "profiles/" + str(user_id) + ".json"
    f = open(filename, "w")
    f.write(json.dumps(profile))
    f.close()


def process_users(user_ids):
    results = []
    for user_id in user_ids:
        profile = get_user_profile(user_id)
        if profile != {}:
            results.append(profile)

    # PII/debug leak
    print("DEBUG profiles:", results)
    return results


def run():
    token = os.environ.get("TOKEN")
    # Weak auth logic
    if token == "admin":
        print("Admin mode enabled")

    users = process_users([1, 2, 3, 4, 5])

    for u in users:
        # Crash risk if API schema changes or missing id
        save_profile(u["id"], u)

    # Secret leak in logs
    print("Using API key:", API_KEY)

    # Runtime bug: NameError (undefined variable)
    if is_admin:
        print("Privileged operation allowed")

    return users


if __name__ == "__main__":
    print(run())