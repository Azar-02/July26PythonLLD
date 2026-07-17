
from abc import ABC, abstractmethod
from User import Member


class Borrowable(ABC):
    @abstractmethod
    def borrow(self, member):
        pass

    @abstractmethod
    def return_item(self, member):
        pass

    @abstractmethod
    def isBorrowable(self):
        pass

class Book (Borrowable, ABC) :

    def __init__(self, title, author, is_available):
        self.title = title
        self.author = author
        self.is_available = True

    @abstractmethod
    def display_info(self):
        pass

    def borrow(self, member):
        if self.is_available and member.can_borrow(self):
            self.is_available = False
            print(f"The book '{self.title}' has been borrowed.")
            return True
        else:
            print(f"The book '{self.title}' is not available for borrowing.")
            return False
    
    def return_item(self, member):
        self.is_available = True
        member._borrowed_count -= 1

    def isBorrowable(self):
        return self.is_available




class Novel (Book):

    def __init__(self, title, author, is_available, genre):
        super().__init__(title, author, is_available)
        self.genre = genre

    def display_info(self):
        print(f"Novel Title: {self.title}, Author: {self.author}, Available: {self.is_available}")

class Textbook (Book):

    def __init__(self, title, author, is_available, subject):
        super().__init__(title, author, is_available)
        self.subject = subject

    def display_info(self):
        print(f"Textbook Title: {self.title}, Author: {self.author}, Available: {self.is_available}")

# Duck Typing: 
def lend_item(book, member):
    return book.borrow(member)

class MagazineArchive:
    
    def __init__(self, title):
        self.title = title

    def borrow(self, member):
        print(f"Borrowing from Magazine Archive: {self.title}")
        return True  # Assuming borrowing is always successful for the archive

# Now only objects that are instances of Borrowable can be passed to lend_item_v2 function.
def lend_item_v2(item, member):
    if isinstance(item, Borrowable):
        return item.borrow(member)
    else:
        print(f"The item '{item}' is not borrowable.")
        return False
    

## PROTOCOL ------------------------ Homework: Implement a protocol for Borrowable items and use it in the lend_item_v2 function.
# @runtime_checkable

subrata = Member("Subrata", "subrata@gmail.com")
print(lend_item(Novel("The Great Gatsby", "F. Scott Fitzgerald", True, "Fiction"), subrata))  # Should return True

# Example of duck typing: MagazineArchive does not inherit from Book, but it has a borrow method,
#  so it can be used with lend_item function.
print(lend_item(MagazineArchive("National Geographic"), subrata))  # Should return True

# We can use the abstract base class Book to enforce the contract 
# so that only book type objects can be passed to the lend_item function.

print(lend_item_v2(MagazineArchive("Time"), subrata))  # Should print that the item is not borrowable