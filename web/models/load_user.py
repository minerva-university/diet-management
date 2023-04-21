from .. import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from logger import info_logger, error_logger
from User import User

@login_manager.user_loader
def load_user(user_id):
    """
    Load the user object for the given user ID.

    Parameters:
    user_id (int): The user ID.

    Returns:
    User: The User object for the given user ID.
    """
    return User.query.get(int(user_id))

