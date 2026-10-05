from dtos.settle_up_dtos import (
    SettleUpRequestDto, SettleUpResponseDto, 
    SettleUpGroupResponseDto, SettleUpGroupRequestDto
    )

class SettleUpController:
    def __init__(self, settle_up_service):
        self.settle_up_service = settle_up_service

    def settle_up_user(self, request_dto: SettleUpRequestDto) -> SettleUpResponseDto:
        expenses = self.settle_up_service.settle_up_user(request_dto.user_id)
        return SettleUpResponseDto(expenses=expenses)

    def settle_up_group(self, request_dto: SettleUpGroupRequestDto) -> SettleUpGroupResponseDto:
        expenses = self.settle_up_service.settle_up_group(request_dto.group_id)
        return SettleUpGroupResponseDto(expenses=expenses)


# Always have a try catch block in the controller layer to handle exceptions 
# and return appropriate error responses.