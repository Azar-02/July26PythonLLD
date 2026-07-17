

from abc import ABC, abstractmethod

# ABC (Abstract Base Class) is used to define abstract classes in Python.

class User(ABC) :

    _id_counter = 0      # class attribute 
    _total_users = 0     # class attribute to keep track of the number of users created

    def __init__(self, name, contact):

        User._id_counter += 1       # class attribute

        self._user_id = User._id_counter    # object attribute
        self.name = name    # object attribute
        self.contact = contact  # object attribute

        User._total_users += 1   # class attribute

    
    @property
    def user_id(self):
        return self._user_id
    
    # No setter for user_id, as it should be read-only

    # @property is only for instance attributes, not class attributes. 
    # So, we cannot use @property for _total_users and _id_counter.

    @classmethod
    def get_total_users(cls):
        return cls._total_users
    
    @abstractmethod
    def display_info(self):
        pass

    @abstractmethod
    def can_borrow(self, book):
        pass

    # def return_book(self, book):
    #    pass


class Member(User):

    MAX_BORROW_LIMIT = 5  # class attribute to define the borrowing limit for members

    def __init__(self, name, contact):
        super().__init__(name, contact)
        self._borrowed_count = 0

    def can_borrow(self, book):
        if self._borrowed_count < Member.MAX_BORROW_LIMIT:
            self._borrowed_count += 1
            print(f"{self.name} has borrowed the book: {book}. Total borrowed: {self._borrowed_count}")
            return True
        else:
            print(f"{self.name} has reached the borrowing limit of {Member.MAX_BORROW_LIMIT} books.")
            return False

    def display_info(self):
        print(f"Member ID: {self.user_id}, Name: {self.name}, Contact: {self.contact}, Borrowed Count: {self._borrowed_count}")
    

class Librarian(User):
    def __init__(self, name, contact, employee_number):
        super().__init__(name, contact)
        self._employee_number = employee_number  # object attribute

    def can_borrow(self, book):
        print(f"Librarian {self.name} can borrow any number of books.")

    def display_info(self):
        print(f"Librarian ID: {self.user_id}, Name: {self.name}, Contact: {self.contact}")


if __name__ == "__main__":
    brighty = Member("Brighty", "brighty@gmail.com")
    brighty.display_info()
    varsha = Librarian("Varsha", "varsha@gmail.com", "EMP123")
    varsha.display_info()