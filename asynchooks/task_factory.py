import asyncio

_create_listeners = []
_start_listeners = []
_finish_listeners = []


def register(create_listener=None, start_listener=None, finish_listener=None):
    if create_listener:
        _create_listeners.append(create_listener)
    if start_listener:
        _start_listeners.append(start_listener)
    if finish_listener:
        _finish_listeners.append(finish_listener)


def unregister(create_listener=None, start_listener=None, finish_listener=None):
    if create_listener:
        _create_listeners.remove(create_listener)
    if start_listener:
        _start_listeners.remove(start_listener)
    if finish_listener:
        _finish_listeners.remove(finish_listener)


def _notify_listeners(listeners, *args, **kwargs):
    for l in listeners:
        l(*args, **kwargs)


class TaskFactory(object):
    def __init__(self, orig_task_factory):
        self.orig_task_factory = orig_task_factory

    def __call__(self, loop, coro, *args, **kwargs):
        async def wrapper():
            task = asyncio.tasks.Task.current_task(loop)
            _notify_listeners(_start_listeners, task)
            try:
                result = await coro
                return result
            finally:
                _notify_listeners(_finish_listeners, task)

        parent_task = asyncio.tasks.Task.current_task(loop)
        if self.orig_task_factory:
            task = self.orig_task_factory(loop, wrapper, *args, **kwargs)
        else:
            task = asyncio.tasks.Task(wrapper(), *args, loop=loop, **kwargs)
        _notify_listeners(_create_listeners, task, parent_task)

        return task


def install(loop=None):
    loop = loop or asyncio.get_event_loop()
    orig_task_factory = loop.get_task_factory()
    loop.set_task_factory(TaskFactory(orig_task_factory))
