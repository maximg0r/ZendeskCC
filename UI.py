from Controller import Controller


class UI:
    def __init__(self) -> None:
        self.controller = Controller()

    def run(self) -> None:
        self.print_welcome_msg()
        # self.auth() # set creds in config.py instead
        self.repl()
        self.print_goodbye_msg()

    def print_welcome_msg(self) -> None:
        print("Welcome to Zendesk Ticket Viewer!")

    def print_goodbye_msg(self) -> None:
        print("\nThank you for using Zendesk Ticket Viewer!")

    def repl(self) -> None:
        print("\nMenu:")
        print("1. List tickets")
        print("2. View ticket")
        print("3. Exit\n")
        s_usr_in = input("Please enter your selection: ")

        while s_usr_in != "3":
            if s_usr_in == "1":
                try:
                    self.controller.list_tickets()
                except Exception as e:
                    print("Error: {}".format(e))
            elif s_usr_in == "2":
                try:
                    self.controller.view_ticket()
                except Exception as e:
                    print("Error: {}".format(e))
            else:
                print("Invalid selection")

            print("\nMenu:")
            print("1. List tickets")
            print("2. View ticket")
            print("3. Exit\n")
            s_usr_in = input("Please enter your selection: ")
