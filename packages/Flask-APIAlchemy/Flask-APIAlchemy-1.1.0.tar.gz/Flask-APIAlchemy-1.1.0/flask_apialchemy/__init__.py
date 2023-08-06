import warnings

import apialchemy

from flask import current_app

from threading import Lock

__version__ = '1.1.0'


def get_state(app):
    """Gets the state for the application"""
    assert 'apialchemy' in app.extensions, \
        'The apialchemy extension was not registered to the current ' \
        'application.  Please make sure to call init_app() first.'

    return app.extensions['apialchemy']


class _APIAlchemyState:
    """Remembers configuration for the (service, app) tuple."""
    def __init__(self, service):
        self.service = service
        self.connectors = {}


class _ServiceConnector:
    def __init__(self, aa, app, bind):
        self._aa = aa
        self._app = app
        self._service = None
        self._connected_for = None
        self._bind = bind
        self._lock = Lock()

    def get_uri(self):
        if self._bind is None:
            return self._app.config['APIALCHEMY_SERVICE_URI']

        binds = self._app.config.get('APIALCHEMY_BINDS') or ()

        assert self._bind in binds, \
            'Bind %r is not specified.  Set it in the APIALCHEMY_BINDS ' \
            'configuration variable' % self._bind

        return binds[self._bind]

    def get_service(self):
        with self._lock:
            uri = self.get_uri()

            if uri == self._connected_for:
                return self._service

            self._service = rv = self._aa.create_service(uri)

            self._connected_for = uri

            return rv


class APIAlchemy:
    def __init__(self, app=None):
        self._service_lock = Lock()
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if (
            'APIALCHEMY_SERVICE_URI' not in app.config and
            'APIALCHEMY_BINDS' not in app.config
        ):
            warnings.warn(
                'Neither APIALCHEMY_SERVICE_URI nor APIALCHEMY_BINDS is set.'
            )

        app.extensions['apialchemy'] = _APIAlchemyState(self)

    @property
    def service(self):
        """Gives access to the service.  If the service configuration is bound
        to a specific application (initialized with an application) this will
        always return a service handle.  If however the current application
        is used this might raise a :exc:`RuntimeError` if no application is
        active at the moment."""
        return self.get_service()

    def make_connector(self, app=None, bind=None):
        """Creates the connector for a given state and bind."""
        return _ServiceConnector(self, self.get_app(app), bind)

    def get_service(self, app=None, bind=None):
        """Returns a specific service."""
        app = self.get_app(app)
        state = get_state(app)

        with self._service_lock:
            connector = state.connectors.get(bind)

            if connector is None:
                connector = self.make_connector(app, bind)
                state.connectors[bind] = connector

            return connector.get_service()

    def create_service(self, uri):
        """Override this method to have final say over how the APIAlchemy
        service is created."""
        return apialchemy.create_service(uri)

    def get_app(self, reference_app=None):
        """Helper method that implements the logic to look up an
        application."""
        if reference_app is not None:
            return reference_app

        if current_app:
            return current_app._get_current_object()

        if self.app is not None:
            return self.app

        raise RuntimeError(
            'No application found. Either work inside a view function or push an application context.'
        )
