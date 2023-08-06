import asyncio
import functools
import sys
from networktools.colorprint import gprint, bprint, rprint

VERSION = sys.version_info

# every coroutine
async def pause(sleep, *args, **kwargs):
    await asyncio.sleep(sleep)
    return [sleep, *args], kwargs

from typing import (
    List,
    Tuple,
    Dict,
    Any,
    Callable)

# from collections.abc import (Coroutine, Awaitable, Callable)
# from mypy_extensions import Expand

# ArgsInput = List[Any]
# KwargsInput = Dict[str, Any]
# ArgsOutput = List[Any]
# KwargsOutput = Dict[str, Any]
# AllInput = Tuple[]
# ResultOutput = Tuple[ArgsOutput, KwargsOutput]
# AwaitableResult = Awaitable[]
# CoroutineFunctionInput = Callable[[Expand[ArgsInput],
#                                    Expand[KwargsInput]], ]]

async def coromask(
        coro,
        args,
        kwargs,
        fargs):
    """
    A coroutine that mask another coroutine  callback with args, and a
    function callbacks who manage input/output of corotine callback

    :param coro: is a coroutine object defined by the developer
    :param args: the list of arguments to run on the corotine *coro*
    :param fargs: the function that process the input and create an output
    related with the coro result

    :returns: a result, is a list of the elements for future argument
    """
    try:
        _in = args
        msg = f"Coromask args {args}, kwargs {kwargs}, in coro {coro}"
        obtained = await coro(*args, **kwargs)
        result = fargs(_in, obtained)
        return result
    except Exception:
        raise Exception(msg)
    except asyncio.TimeoutError as te:
        raise te
    except asyncio.CancelledError as ce:
        raise ce


def renew(task, coro, fargs, *args, **kwargs):
    """
    A simple function who manages the scheduled task and set the
    renew of the task

    :param task: is a Future initialized coroutine but not executed yet
    :param coro: is the corutine to renew when the first is finished
    :param fargs: the function to process input/output
    :param args: the unpacked list of extra arguments
    """
    if not task.cancelled():
        try:
            result = task.result()
            result_args, result_kwargs = result
            loop = asyncio.get_event_loop()
            stop = result_kwargs.get('stop')
            if not stop:
                task = loop.create_task(
                    coromask(coro, result_args, result_kwargs, fargs), )
                task.add_done_callback(
                    functools.partial(renew, task, coro, fargs))
            else:
                return "STOPPED"
        except asyncio.InvalidStateError as ie:
            msg = f"Coro {coro} args {args} kargs {kwargs}"
            print(msg, ie)
            raise ie
        except Exception as e:
            msg = f"Resultado  cancelled {task.cancelled()}, {task}, coro {coro}, fargs {fargs}" 
            print(msg, e)
            raise e
    else:
        try:
            result = task.result()
            return result
        except Exception as e:
            raise e


def simple_fargs(_in, obtained):
    """
    Simple function who can be used in callback on coromask, the
    inputs are /_in/ and /obtained/ value from the coroutine executed.
    Return _in

    :_in: the input list
    :param obtained: the object that came from the result of coroutine
    execution

    :returns: _in
    """
    return _in


def simple_fargs_out(_in, obtained):
    """
    Simple function who can be used in callback on coromask, the
    inputs are /_in/ and /obtained/ value from the coroutine executed.
    Return obtained

    :param _in: the input list
    :param obtained: the object that came from the result of coroutine
    execution

    :returns: obtained
    """
    return obtained


class TaskLoop:
    """
    Esta clase encapsula corrutinas que serán definidas
    para ejecutarse en loop

    Ofrese las siguientes acciones:

    - pause : entra a una pausa hasta que un controlador le diga continuar
    - task_continue : hace continuar la tarea si se ha pausado
    - stop : detiene definitivamente la tarea
    - close : cancela definitivamente la tarea

    Parámetros necesario:

    - coro: la corrtina a ejecutarse, debe aceptar *args,**kwargs para operar
      correctamente

    Parámetros alternativos:

    - coro_args :: lista o secuencia de entradas ordenadas
    - coro_kwargs :: diccionario con parámetros extra

    Parámetros adicionales alternativos:

    - fargs :: la funcion de operacion de las salidas
    - time_pause :: cantidad de tiempo en pause por cada iteración de loop

    """
    control_words = {"START", "PAUSE", "CONTINUE", "STOP"}
    _name = "taskloop"

    def __init__(self, coro, coro_args=[], coro_kwargs={}, *args, **kwargs):
        self.control = 'START'
        self.coro = coro
        self.coro_args = coro_args
        self.coro_kwargs = coro_kwargs
        self.coro_kwargs['taskloop'] = self
        self._name = kwargs.get('name', 'taskloop')
        self.fargs = kwargs.get('fargs', simple_fargs_out)
        self.loop = kwargs.get('loop', asyncio.get_event_loop())
        asyncio.set_event_loop(self.loop)
        self.time_pause = kwargs.get('time_pause', .1)

    def __str__(self):
        return f'''Taskloop {self.name},
        coro {self.coro}, args {self.coro_args},
        kwargs {self.coro_kwargs}'''

    def __repr__(self):
        return f"Taskloop({self.coro},{self.coro_args},{self.coro_kwargs})"

    def close(self):
        task = asyncio.current_task()
        task.cancel()

    def stop(self):
        self.control = "STOP"

    def pause(self):
        self.control = "PAUSE"

    def task_continue(self):
        self.control = "CONTINUE"

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def create(self):
        if VERSION.major == 3 and VERSION.minor >= 8:
            task = self.loop.create_task(
                coromask(
                    self.coro,
                    self.coro_args,
                    self.coro_kwargs,
                    self.fargs))
            task.add_done_callback(
                 functools.partial(self.renew, task, self.coro, self.fargs))
            return task
        if VERSION.major == 3 and VERSION.minor == 7:
            task = self.loop.create_task(
                coromask(
                    self.coro,
                    self.coro_args,
                    self.coro_kwargs,
                    self.fargs))
            task.add_done_callback(
                 functools.partial(self.renew, task, self.coro, self.fargs))
            return task


    def renew(self, task, coro, fargs, *args, **kwargs):
        """
        A simple function who manages the scheduled task and set the
        renew of the task

        :param task: is a Future initialized coroutine but not executed yet
        :param coro: is the corutine to renew when the first is finished
        :param fargs: the function to process input/output
        :param args: the unpacked list of extra arguments
        """
        result_kwargs = {}
        if not task.cancelled():
            try:
                result = task.result()
                result_args, result_kwargs = result
                loop = asyncio.get_event_loop()
                exception = result_kwargs.get("exception")
                if exception:
                    raise exception
                if self.control == "STOP" or result_kwargs.get('stop'):
                    return "STOPPED"
                elif self.control in {"START", "CONTINUE"}:
                    if self.control == 'CONTINUE':
                        coro = self.coro
                    task = None
                    if VERSION.major == 3 and VERSION.minor >= 8:
                        task = loop.create_task(
                            coromask(coro, result_args,
                                     result_kwargs, fargs), name=self._name)
                    if VERSION.major == 3 and VERSION.minor == 7:
                        task = loop.create_task(
                            coromask(coro, result_args,
                                     result_kwargs, fargs))
                    task.add_done_callback(
                        functools.partial(self.renew, task, coro, fargs))
                elif self.control == "PAUSE":
                    pause_args = [self.time_pause]
                    pause_kwargs = {}
                    task = None
                    if VERSION.major == 3 and VERSION.minor >= 8:
                        task = loop.create_task(
                            coromask(pause, pause_args,
                                     pause_kwargs, fargs), name=self._name)
                    if VERSION.major == 3 and VERSION.minor == 7:
                        task = loop.create_task(
                            coromask(pause, pause_args,
                                     pause_kwargs, fargs))
                    task.add_done_callback(
                        functools.partial(self.renew, task, pause,
                                          fargs))
            except asyncio.CancelledError as ce:
                rprint(f"Error de cancelación fargs {fargs}")
                raise ce
            except asyncio.IncompleteReadError as incomplete_read:
                print("IncompleteReadError {incomplete_read}")
                print("Result incomplete: {incomplete_read.partial}")
                raise incomplete_read
            except asyncio.InvalidStateError as ie:
                print("Invalid State Error", ie, "Coro", coro, "args", args,
                      "kargs", kwargs)
                raise ie
            except Exception as e:
                log = None
                if result_kwargs:
                    log = result_kwargs.get('log')
                msg = f"""TaskLoop. Result cancelled {task.cancelled()},
                    task {task},
                    coro {coro},
                    fargs {fargs}"""
                if task.done():
                    msg_done = f"TaskLoop exception, Task done {task}"
                    if log:
                        log.exception(msg_done)
                if log:
                    log.exception(msg)
                raise e
        else:
            try:
                result = task.result()
                return result
            except Exception as e:
                raise e
