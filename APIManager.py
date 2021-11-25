from datetime import datetime

import requests

import config

URL_TEMPLATE = 'https://{}.zendesk.com/{}'


class Ticket:
    def __init__(self, id: int, subject: str, requester_id: str, created: datetime, group_id: str, status: str) -> None:
        self.id = id
        self.subject = subject
        self.requester_id = requester_id
        self.created = created
        self.group_id = group_id
        self.status = status


class Page:
    def __init__(self, ticket_list: list[Ticket], next_page_url: str, prev_page_url: str, has_more: bool) -> None:
        self.ticket_list = ticket_list
        self.next_page_url = next_page_url
        self.prev_page_url = prev_page_url
        self.has_more = has_more

    def is_empty(self) -> bool:
        return len(self.ticket_list) == 0

    def has_next(self) -> bool:
        return self.next_page_url is not None and self.has_more

    def has_prev(self) -> bool:
        return self.prev_page_url is not None


class APIManager:

    def __init__(self) -> None:
        if not config.creds or not config.creds['email'] or not config.creds['subdomain'] or not config.creds['token']:
            raise Exception("Credentials not set in config.py")

    def send_request(self, s_endpoint=None, s_url=None) -> dict:
        assert s_endpoint or s_url, "Must provide either an API endpoint or a url"

        if not s_url:
            s_url = URL_TEMPLATE.format(config.creds['subdomain'], s_endpoint)
        t_auth = (
            '{}/token'.format(config.creds['email']), config.creds['token'])

        r = requests.get(s_url, auth=t_auth)

        if r.status_code == 401:
            raise Exception("Invalid credentials")
        elif r.status_code == 403:
            raise Exception("Access denied")
        elif r.status_code == 404:
            raise Exception("Ticket not found")
        elif r.status_code < 200 or r.status_code >= 400:
            raise Exception(
                "Request failed with status code {}".format(r.status_code))

        return r.json()

    def get_ticket_count(self) -> int:
        s_endpoint = 'api/v2/tickets/count.json'
        res = self.send_request(s_endpoint)
        return int(res['count']['value'])

    def get_page(self, s_url=None, page_size=25) -> Page:
        if not s_url:
            s_endpoint = 'api/v2/tickets.json?page[size]={}'.format(page_size)
            res = self.send_request(s_endpoint=s_endpoint)
        else:
            res = self.send_request(s_url=s_url)

        ticket_list = []
        for ticket in res['tickets']:
            ticket_list.append(Ticket(
                id=ticket['id'],
                subject=ticket['subject'],
                requester_id=ticket['requester_id'],
                created=datetime.strptime(
                    ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
                group_id=ticket['group_id'],
                status=ticket['status']
            ))

        return Page(
            ticket_list=ticket_list,
            next_page_url=res['links']['next'],
            prev_page_url=res['links']['prev'],
            has_more=res['meta']['has_more']
        )

    def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        s_endpoint = 'api/v2/tickets/{}.json'.format(ticket_id)
        res = self.send_request(s_endpoint)
        ticket = res['ticket']
        return Ticket(
            id=ticket['id'],
            subject=ticket['subject'],
            requester_id=ticket['requester_id'],
            created=datetime.strptime(
                ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
            group_id=ticket['group_id'],
            status=ticket['status']
        )
