

class SettleUpUserRequestDTO:
    def __init__(self, user_id: int):
        self.user_id = user_id

class SettleUpUserResponseDTO:
    def __init__(self, expenses):
        self.expenses = expenses # our dummy settlement expenses

class SettleUpGroupRequestDTO:
    def __init__(self, group_id: int):
        self.group_id = group_id

class SettleUpGroupResponseDTO:
    def __init__(self, expenses):
        self.expenses = expenses # our dummy settlement expenses