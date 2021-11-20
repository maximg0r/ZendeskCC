from Controller import Controller


class UI:
    def __init__(self) -> None:
        self.auth_credentials = None
        self.controller = Controller()

    def run(self) -> None:
        self.print_welcome_msg()
        self.auth()
        self.repl()
        self.print_goodbye_msg()

    def print_welcome_msg(self) -> None:
        print("Welcome to Zendesk Ticket Viewer!\n")

    def print_goodbye_msg(self) -> None:
        print("\nThank you for using Zendesk Ticket Viewer!")

    def auth(self) -> None:
        # print("Authentication options:")
        s_subdomain = input("Please enter your subdomain: ")
        s_oauthtoken = input("Please enter your OAuth token: ")

        self.auth_credentials = {
            "subdomain": s_subdomain,
            "oauth_token": s_oauthtoken
        }

    def repl(self) -> None:
        print("\nMenu:")
        print("1. List tickets")
        print("2. View ticket")
        print("3. Exit\n")

        s_usr_in = input("Please enter your selection: ")

        while s_usr_in != "3":
            if s_usr_in == "1":
                self.controller.list_tickets()
            elif s_usr_in == "2":
                self.controller.view_ticket()
            else:
                print("Invalid selection")

            s_usr_in = input("Please enter your selection: ")
