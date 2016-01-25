# -*- coding: utf8 -*-

from libcrowds_statistics import event_listeners
from mock import patch, MagicMock
from default import with_context, Test


class TestEventListener(Test):

    @with_context
    @patch('libcrowds_statistics.event_listeners.request')
    def test_ip_address_set_for_new_task_run(self, mock_request):
        mock_request = MagicMock()
        mock_request.access_route = None
        mock_ip = '1.2.3.4'
        mock_request.remote_addr = mock_ip
        mock_info = MagicMock()
        mock_target = MagicMock()
        mock_target.info = mock_info
        mock_conn = MagicMock()
        event_listeners.add_task_run_event(None, mock_conn, mock_target)

        assert mock_info.__setitem__.called_with('ip_address', mock_ip)


    @with_context
    @patch('libcrowds_statistics.event_listeners.request')
    def test_ip_address_still_set_when_proxy(self, request):
        mock_request = MagicMock()
        mock_request.access_route = '127.0.0.1'
        mock_ip = '1.2.3.4'
        mock_request.remote_addr = mock_ip
        mock_info = MagicMock()
        mock_target = MagicMock()
        mock_target.info = mock_info
        mock_conn = MagicMock()
        event_listeners.add_task_run_event(None, mock_conn, mock_target)

        assert mock_info.__setitem__.called_with('ip_address', mock_ip)
