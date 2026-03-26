from config import PREMIUM_USERS, BANNED_USERS

def add_premium(user_id):
    PREMIUM_USERS.add(user_id)

def remove_premium(user_id):
    PREMIUM_USERS.discard(user_id)

def is_premium(user_id):
    return user_id in PREMIUM_USERS

def ban_user(user_id):
    BANNED_USERS.add(user_id)

def unban_user(user_id):
    BANNED_USERS.discard(user_id)

def is_banned(user_id):
    return user_id in BANNED_USERS