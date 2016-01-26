# -*- coding: utf8 -*-

from mock import patch, MagicMock
from default import with_context, Test
from pybossa.model.task_run import TaskRun
from factories import TaskRunFactory
from sqlalchemy import event

from libcrowds_statistics import event_listeners


class TestEventListener(Test):

    def setUp(self):
        self.ip_listener = event_listeners.record_new_task_run_ip_event
        event.listen(TaskRun, 'before_insert', self.ip_listener)

    def tearDown(self):
        func = event_listeners.record_new_task_run_ip_event
        event.remove(TaskRun, 'before_insert', self.ip_listener)


    @with_context
    @patch('libcrowds_statistics.event_listeners.request')
    def test_ip_address_set_for_new_task_run(self, mock_request):
        mock_target = MagicMock()
        mock_conn = MagicMock()
        mock_request.remote_addr = '1.2.3.4'
        mock_request.headers.getlist.return_value = False

        event_listeners.record_new_task_run_ip_event(None, mock_conn,
                                                     mock_target)
        tr_info_args = mock_target.info.__setitem__.call_args_list

        assert tr_info_args[0][0] == ('ip_address', '1.2.3.4')


    @with_context
    @patch('libcrowds_statistics.event_listeners.request')
    def test_ip_address_still_set_when_behind_proxy(self, mock_request):
        mock_target = MagicMock()
        mock_conn = MagicMock()
        mock_request.remote_addr = '1.2.3.4'
        mock_request.headers.getlist.return_value = ['1.2.3.4']

        event_listeners.record_new_task_run_ip_event(None, mock_conn,
                                                     mock_target)
        tr_info_args = mock_target.info.__setitem__.call_args_list

        assert tr_info_args[0][0] == ('ip_address', '1.2.3.4')
