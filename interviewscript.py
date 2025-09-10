import requests
#Fiie: interviewscript.py
#Author: Jace Yarborough
#Purpose: This file will add the 5 already set up users 
#in okta to the remediation group and then delete those
#same 5 users.
#Too run just insert api token into empty API Token variable

# CONFIG — update these values!!!



#insert ockta domain below
OKTA_DOMAIN = "" 

# api key in email from jace_yarborough1@baylor.edu
API_TOKEN = ""                


GROUP_NAME = "Remediation"                       # The group we target
USER_EMAIL_PREFIX = "sgnl-training+"        
USER_EMAIL_SUFFIX = "@sgnl.ai"                  
NUM_USERS = 5                               

HEADERS = {
    "Authorization": f"SSWS {API_TOKEN}",
    "Content-Type": "application/json"
}


# FUNCTIONS

def get_group_id():
    """Fetch the group ID for the Remediation group"""
    url = f"{OKTA_DOMAIN}/api/v1/groups?q={GROUP_NAME}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    groups = resp.json()
    for g in groups:
        if g["profile"]["name"] == GROUP_NAME:
            return g["id"]
    raise Exception(f"Group '{GROUP_NAME}' not found")

def get_user_id(email):
    """Fetch a user ID from an email address"""
    url = f"{OKTA_DOMAIN}/api/v1/users/{email}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()["id"]
    else:
        print(f"User {email} not found")
        return None

def add_users_to_group(group_id, user_ids):
    """Add each user to the Remediation group"""
    for uid in user_ids:
        if not uid:
            continue
        url = f"{OKTA_DOMAIN}/api/v1/groups/{group_id}/users/{uid}"
        resp = requests.put(url, headers=HEADERS)
        if resp.status_code in [200, 204]:
            print(f" Added user {uid} to group")
        else:
            print(f" Failed to add {uid}: {resp.text}")

def remove_users_from_group(group_id, user_ids):
    """Remove each user from the Remediation group"""
    for uid in user_ids:
        if not uid:
            continue
        url = f"{OKTA_DOMAIN}/api/v1/groups/{group_id}/users/{uid}"
        resp = requests.delete(url, headers=HEADERS)
        if resp.status_code in [200, 204]:
            print(f"✅ Removed user {uid} from group")
        else:
            print(f"❌ Failed to remove {uid}: {resp.text}")


# MAIN

if __name__ == "__main__":
    group_id = get_group_id()

    # Build user email list
    user_emails = [
        f"{USER_EMAIL_PREFIX}{i}{USER_EMAIL_SUFFIX}"
        for i in range(1, NUM_USERS + 1)
    ]

    # Get user IDs from emails
    user_ids = [get_user_id(email) for email in user_emails]

    print("\n--- Adding users to Remediation group ---")
    add_users_to_group(group_id, user_ids)

    print("\n--- Removing users from Remediation group ---")
    remove_users_from_group(group_id, user_ids)




