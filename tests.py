import unittest
from unittest import TestCase, mock

import Controller
import UI
from APIManager import APIManager, Page, Ticket


class TestAPIManager(TestCase):
    def setUp(self):
        self.api_manager = APIManager()

    def test_send_request(self):
        # test sending a tickets count request
        res = self.api_manager.send_request(
            s_endpoint='api/v2/tickets/count.json')
        self.assertIsInstance(res, dict)
        self.assertTrue('count' in res)

        # test getting an error from request
        def error_request():
            self.api_manager.send_request(
                s_endpoint='api/v2/tickets/helloworld.json')
        self.assertRaises(Exception, error_request)

    def test_get_ticket_count(self):
        # test getting tickets count
        count = self.api_manager.get_ticket_count()
        self.assertIsInstance(count, int)

    def test_get_page(self):
        # test getting a page of tickets
        page = self.api_manager.get_page()
        self.assertIsInstance(page, Page)

    def test_get_ticket_by_id(self):
        # test getting a ticket by id
        ticket = self.api_manager.get_ticket_by_id(1)
        self.assertIsInstance(ticket, Ticket)

        # test invalid id
        def invalid_id_1():
            self.api_manager.get_ticket_by_id('abc123')
        self.assertRaises(Exception, invalid_id_1)

        def invalid_id_2():
            self.api_manager.get_ticket_by_id(-1)
        self.assertRaises(Exception, invalid_id_2)


class TestController(TestCase):
    def setUp(self):
        self.controller = Controller.Controller()

    @mock.patch('Controller.input', create=True)
    def test_list_tickets(self, mocked_input):
        # test list tickets and page navigation
        mocked_input.side_effect = ['n', 'n', 'p', 'p', 'p', 'b']
        self.controller.list_tickets()

    @mock.patch('Controller.input', create=True)
    def test_view_ticket(self, mocked_input):
        # test view ticket and invalid id handling
        mocked_input.side_effect = ['1', '-5', '123xyz']
        self.controller.view_ticket()
        self.controller.view_ticket()
        self.controller.view_ticket()


class TestUI(TestCase):
    def setUp(self):
        self.ui = UI.UI()

    @mock.patch('UI.input', create=True)
    @mock.patch('Controller.input', create=True)
    def test_run(self, mocked_input_ctrl, mocked_input_ui):
        # test top-level program execution
        mocked_input_ui.side_effect = ['1', '2', '2', '3']
        mocked_input_ctrl.side_effect = ['n', 'p', 'b', '5', '4221']
        self.ui.run()


if __name__ == '__main__':
    unittest.main()
