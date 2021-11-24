from re import sub
from APIManager import APIManager
from zenpy.lib.api_objects import Ticket


class Controller():
    def __init__(self) -> None:
        self.api_manager = APIManager()

    def list_tickets(self) -> None:
        l_ticket_list = self.api_manager.get_ticket_list()
        print_header()
        for ticket in l_ticket_list:
            print_ticket(ticket)

    def view_ticket(self) -> None:
        ticket = self.api_manager.get_ticket_by_id(input("Enter ticket ID: "))
        print_header()
        print_ticket(ticket)


def print_header() -> None:
    ls_cols = ["[ID]", "[Subject]", "[Requester]", "[Created]"]
    fmt_template = "{:>4} {:<40} {:20} {:16}"  # set fixed col width
    header = fmt_template.format(*ls_cols)

    print(header)


def print_ticket(ticket: Ticket) -> None:
    s_subject = ticket.subject
    if (len(s_subject) > 37):
        s_subject = s_subject[:37] + "..."  # shorten subject to 40 chars
    s_date = ticket.created.strftime("%m/%d/%Y %H:%M")  # format date

    ls_cols = [ticket.id, s_subject, ticket.requester.name, s_date]
    s_fmt_template = "{:>4} {:<40} {:20} {:16}"  # set fixed col width
    s_line = s_fmt_template.format(*ls_cols)

    print(s_line)
