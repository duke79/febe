from flask import request, jsonify
from flask_socketio import emit, Namespace

from lib.py.auth.permission import ensure_condition
from lib.py.cli.run import FireCLI
from lib.py.core.env import EnvCounter

from flask_socketio import SocketIO

from lib.py.core.traces import println
from lib.py.data.redis_session import RedisSession
from ...app import app

socketio = SocketIO(app)


@socketio.on('my event', namespace='/test')
def test_message(message):
    print(message)
    emit('my response', {'data': message['data']})


@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


class SocketNamespace(Namespace):
    # Catch all events
    # For JS | https://stackoverflow.com/questions/10405070/socket-io-client-respond-to-all-events-with-one-handler
    def trigger_event(self, event, *args):
        """Dispatch an event to the proper handler method.
        In the most common usage, this method is not overloaded by subclasses,
        as it performs the routing of events to methods. However, this
        method can be overriden if special dispatching rules are needed, or if
        having a single method that catches all events is desired.
        """
        handler_name = 'on_' + event
        print(handler_name)
        if not hasattr(self, handler_name):
            # This is a custom event, let on_fire try to handle it with req_id
            args = args + (event,)
            handler = getattr(self, "on_fire")
        else:
            handler = getattr(self, handler_name)
        return self.socketio._handle_event(handler, event, self.namespace,
                                           *args)

    def on_connect(self):
        emit('my response', {'data': 'welcome!'})

    def on_disconnect(self):
        print('Client disconnected')

    def on_fire(self, cmd, req_id=None):
        emit('fireout', {'state': 'begin', 'req_id': req_id, 'counter': EnvCounter(req_id).increment().value})
        FireCLI().run_threaded(cmd, emit, req_id)
        emit('fireout', {'state': 'end', 'req_id': req_id, 'counter': EnvCounter(req_id).increment().value})

    def on_echo(self, message):
        emit('my response', {'data': message['data']})


socketio.on_namespace(SocketNamespace('/websocket'))


# REST endpoint (in case websocket is too much)
@app.route("/fire", methods=["POST", "GET"])
def fire():
    try:
        # ensure_condition(RedisSession().USER_INFO["id"] is not None)

        post_data = request.get_json(silent=True)
        cmd = post_data["cmd"]
        ret = FireCLI().run_and_return_json(cmd, "/fire")
        println(ret)
        return jsonify(ret)
    except PermissionError as e:
        return "How dare you?!", 403
