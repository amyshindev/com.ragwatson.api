from __future__ import annotations


class Booking:
    """타이타닉 승객 예약(티켓) 도메인 엔티티"""

    def __init__(
        self,
        passenger_id: int,
        pclass: str,
        ticket: str,
        fare: str,
        cabin: str,
        embarked: str,
    ) -> None:
        self.passenger_id = passenger_id
        self.pclass = pclass
        self.ticket = ticket
        self.fare = fare
        self.cabin = cabin
        self.embarked = embarked
