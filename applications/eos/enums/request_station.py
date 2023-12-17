class RequestStationApproveStatus:
    WAITING = 0
    APPROVED = 1
    REJECTED = 2

    def arr(self):
        return [
            self.WAITING,
            self.APPROVED,
            self.REJECTED
        ]


class RequestStationApproveAction:
    APPROVE = 0
    REJECT = 1

    def arr(self):
        return [
            self.APPROVE,
            self.REJECT,
        ]