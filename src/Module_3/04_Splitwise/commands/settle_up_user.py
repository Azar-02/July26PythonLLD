from click import Command
from dtos.settle_up_dtos import SettleUpRequestDto


class SettleUpuser(Command):
    def __init__(self, settle_up_controller):
        self.settle_up_controller = settle_up_controller

    # settleup U21
    def matches(self, input_str: str) -> bool:
        # Check if the input string matches the command for settling up a user
        words = input_str.strip().split(" ") 
        return (
            len(words) == 2 and
            words[0].lower() == "settleup" and
            words[1].startswith("U") and
            words[1][1:].isdigit()  # Check if the part after 'U' is a number
        )
    
    def execute(self, input_str: str) -> None:
        # Logic to settle up the user's balance
        words = input_str.strip().split(" ")
        user_id = int(words[1][1:])  # Extract the user ID from the input

        request_dto = SettleUpRequestDto(user_id=user_id)
        response = self.settle_up_controller.settle_up_user(request_dto)