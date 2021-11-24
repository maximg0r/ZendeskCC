import config
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket


class APIManager():
    def __init__(self) -> None:
        if not config.creds:
            raise Exception("Credentials not set in config.py")

        self.zenpy_client = Zenpy(**config.creds)  # init the API client

    def get_ticket_count(self) -> int:
        return self.zenpy_client.tickets().count

    def get_ticket_list(self) -> list[Ticket]:
        ticket_generator = self.zenpy_client.tickets()
        # get first 25 tickets; TODO: pagination
        tickets = ticket_generator[0:25]

        return tickets

    def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        ticket = self.zenpy_client.tickets(id=ticket_id)

        return ticket
