import math

from APIManager import APIManager, Page, Ticket


class Controller:
    def __init__(self, page_size=25) -> None:
        self.api_manager = APIManager()
        self.page_size = page_size

    def list_tickets(self) -> None:
        i_page_num = 1
        i_total_pages = math.ceil(
            self.api_manager.get_ticket_count() / self.page_size)
        i_total_tickets = self.api_manager.get_ticket_count()

        # print the first page
        curr_page = self.api_manager.get_page(page_size=self.page_size)
        print_page(curr_page, i_page_num, i_total_pages, i_total_tickets)

        # UI for pagination
        while True:
            print()
            if curr_page.has_next() and i_page_num < i_total_pages:
                # has next page
                print("\t* Press n to see next page")
            if curr_page.has_prev() and i_page_num > 1:
                # has previous page
                print("\t* Press p to see previous page")
            print("\t* Press b to go back\n")
            s_usr_in = input("Please enter your selection: ")

            if s_usr_in == 'n':
                if not (curr_page.has_next() and i_page_num < i_total_pages):
                    print("No next page")
                    continue
                i_page_num += 1
                curr_page = self.api_manager.get_page(
                    s_url=curr_page.next_page_url, page_size=self.page_size)
                print_page(curr_page, i_page_num, i_total_pages, i_total_tickets)
            elif s_usr_in == 'p':
                if not (curr_page.has_prev() and i_page_num > 1):
                    print("No previous page")
                    continue
                i_page_num -= 1
                curr_page = self.api_manager.get_page(
                    s_url=curr_page.prev_page_url, page_size=self.page_size)
                print_page(curr_page, i_page_num, i_total_pages, i_total_tickets)
            elif s_usr_in == 'b':
                break
            else:
                print("Invalid selection")

    def view_ticket(self) -> None:
        ticket_id = input("Please enter the ticket id: ")
        try:
            ticket_id = int(ticket_id)
        except ValueError:
            print("Invalid ticket id")
            return

        if ticket_id < 1 or ticket_id > self.api_manager.get_ticket_count():
            print("Invalid ticket id")
            return

        ticket = self.api_manager.get_ticket_by_id(ticket_id)
        print_header()
        print_ticket(ticket)


def print_header() -> None:
    ls_cols = ["[ID]", "[Subject]", "[Requester]",
               "[Created]", "[Group]", "[Status]"]
    # set fixed col width
    s_fmt_template = "{:>4} {:<40} {:<20} {:<20} {:<20} {:<10}"
    s_header = s_fmt_template.format(*ls_cols)

    print(s_header)


def print_ticket(t: Ticket) -> None:
    s_subject = t.subject
    if (len(s_subject) > 37):
        s_subject = s_subject[: 37] + "..."  # shorten subject to 40 chars
    s_date = t.created.strftime("%m/%d/%Y %H:%M")  # format date

    ls_cols = [t.id, s_subject, t.requester_id,
               s_date, t.group_id, t.status]
    # set fixed col width
    s_fmt_template = "{:>4} {:<40} {:<20} {:<20} {:<20} {:<10}"
    s_line = s_fmt_template.format(*ls_cols)

    print(s_line)


def print_page(p: Page, page_num, total_pages, total_tickets) -> None:
    print("[Page {}/{}, {} tickets total, {} on this page]".format(page_num,
          total_pages, total_tickets, len(p.ticket_list)))
    print_header()
    for ticket in p.ticket_list:
        print_ticket(ticket)
