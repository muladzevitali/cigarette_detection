import json


def create_users(user_model, db):
    """Inserting users when starting the server"""
    with open("media/database/users_tree.json") as input_stream:
        users_tree = json.load(input_stream)

    for user_meta in users_tree:
        user = user_model()
        user.username = user_meta["username"]
        user.password = user_meta['password']

        db.session.add(user)

    db.session.commit()
