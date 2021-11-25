# Zendesk Ticket Viewer

Ticket Viewer is a Python CLI tool that allows viewing Zendesk support tickets for your account.

Made for the 2022 Intern Coding Challenge.
Author: Maxim Gorshkov

## Installation

* Make sure you have python3 and pip installed on your machine.
* Use git to clone this repository to a local directory of your choice.
* Install the dependencies listed in requirements.txt.

```bash
git clone https://github.com/maximg0r/ZendeskCC.git
cd ZendeskCC
pip install -r requirements.txt
```

## Usage

Set your own auth credentials (API token) in config.py, then use

```bash
python TicketViewer.py
```

## Unit tests

To run unit tests (which are located in tests.py), use

```bash
python -m unittest
```

or

```bash
python tests.py
```

## Design overview

The program consists of 3 modules:
* UI module
    - Responsible for top-level program navigation and running the main I/O loop.
    - UI.run() is called from TicketViewer.main (the main entrypoint) to start the program loop.
    - Calls methods in the Controller module correspoinding to the required operations.

* Controller module
    - Responsible for executing the required operations (including doing operation-specific I/O).
    - The two main operations it implements are list_tickets() and view_ticket().
    - Calls methods in the APIManager to perform these operations.

* APIManager module
    - Responsible for making requests to the Zendesk API, processing the responses, and returning the results.
    - The three main operations it implements are get_ticket_count(), get_page(), and get_ticket_by_id().
    - Also contains the definitions of Ticket and Page classes, which are wrappers for relevant fields in the raw json objects.

For the sake of efficiency (especially when dealing with large numbers of tickets), I used cursor-based pagination when listing tickets. That means that tickets are requested one page at a time (with page size set to 25 tickets), instead of pulling all tickets at once. This helps keep memory usage low and reduce the delay when displaying the ticket list.

I also chose to make requests to the Zendesk API manually, instead of using a 3rd-party Python library (like Zenpy). This allowed me to have better control of how requests are made and pagination is done.