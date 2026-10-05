from models.user import User
from repositories.repository import Repository

class UserRepository(Repository[User]):
    def __init__(self, session):
        self.session = session

    def find_by_phone_number(self, phone_number):
        return self.session.query(User).filter_by(phone_number=phone_number).first()