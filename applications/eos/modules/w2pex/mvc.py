#!/usr/bin/env python
# coding: utf8

from gluon import current
from gluon.http import HTTP

class ActionHandler(object):
    def __init__(self,
                 on_action_executing = None,
                 on_action_executed = None,
                 on_view_rendering = None,
                 on_view_rendered = None,
                 on_action_finished = None,
                 on_exception = None):
        self._action_executing_handlers = []
        if on_action_executing:
            self._action_executing_handlers.append(on_action_executing)
        self._action_executed_handlers = []
        if on_action_executed:
            self._action_executed_handlers.append(on_action_executed)
        self._view_rendering_handlers = []
        if on_view_rendering:
            self._view_rendering_handlers.append(on_view_rendering)
        self._view_rendered_handlers = []
        if on_view_rendered:
            self._view_rendered_handlers.append(on_view_rendered)
        self._action_finished_handlers = []
        if on_action_finished:
            self._action_finished_handlers.append(on_action_finished)
        self._exception_handlers = []
        if on_exception:
            self._exception_handlers.append(on_exception)

    def _my_caller(self, func):
        try:
            # Before calling action
            if len(self._action_executing_handlers) > 0:
                for f in self._action_executing_handlers:
                    f()
            # Call action
            ret = func()
            # After calling action
            if len(self._action_executed_handlers) > 0:
                for f in self._action_executed_handlers:
                    f()
            # If a view is available
            if isinstance(ret, dict):
                # Before view render
                if len(self._view_rendering_handlers) > 0:
                    for f in self._view_rendering_handlers:
                        f()
                # Render view
                ret = self._response.render(ret)
                # After view render
                if len(self._view_rendered_handlers) > 0:
                    for f in self._view_rendered_handlers:
                        f()
            # Return response
            return ret
        except Exception as e:
            if len(self._exception_handlers) > 0:
                for f in self._exception_handlers:
                   f(e)
            raise
        finally:
            # After everything
            if len(self._action_finished_handlers) > 0:
                for f in self._action_finished_handlers:
                    f()

    def attach(self, response):
        self._response = response
        response._caller = self._my_caller

    def add_action_executing_handler(self, f):
        self._action_executing_handlers.append(f)

    def add_action_executed_handler(self, f):
        self._action_executed_handlers.append(f)

    def add_view_rendering_handler(self, f):
        self._view_rendering_handlers.append(f)

    def add_view_rendered_handler(self, f):
        self._view_rendered_handlers.append(f)

    def add_action_finished_handler(self, f):
        self._action_finished_handlers.append(f)

    def add_exception_handler(self, f):
        self._exception_handlers.append(f)
