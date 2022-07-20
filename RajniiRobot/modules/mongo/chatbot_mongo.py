from RajniiRobot import mongodb as db_x

rajnii = db_x["CHATBOT"]


def add_chat(chat_id):
    stark = rajnii.find_one({"chat_id": chat_id})
    if stark:
        return False
    rajnii.insert_one({"chat_id": chat_id})
    return True


def remove_chat(chat_id):
    stark = rajnii.find_one({"chat_id": chat_id})
    if not stark:
        return False
    rajnii.delete_one({"chat_id": chat_id})
    return True


def get_all_chats():
    r = list(rajnii.find())
    if r:
        return r
    return False


def get_session(chat_id):
    stark = rajnii.find_one({"chat_id": chat_id})
    if not stark:
        return False
    return stark
