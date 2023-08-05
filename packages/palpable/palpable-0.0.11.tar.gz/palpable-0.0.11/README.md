# Palpable

## Introduction

Palpable is a producer-consumer type of task server that uses multiprocessing to do parallel computing. If you need a
small asynchronous task server and would not like to go through the complication of setting up rabbitmq and Celery,
Palpable is the choice.

Palpable uses Clients to submit Tasks to a Server which manages several Workers. A Task is constructed given a Procedure
which defines what should be done in a task. Each Task has a unique task_id for querying.

## Install

```shell
pip install palpable
```

## ATTENTION Before Start Using

### Palpable do not offer on disk persistence
Palpable Server's data are all in memory. Once the server is shutdown, all data are lost.

### Palpable run each task in its own process
This ensures isolated environment for each task and multi-cpu usages. However, it adds overhead. Therefore,if each task 
is easy, running these tasks will be way slower than directly run them in one process.

### Python's `print` `multiprocessing` deadlock
Do not use `print` in the code send to the Palpable server. Doing so may cause palpable Workers to deadlock without
notice. Palpable is trying to catch the `print` statement in the code sent to the server, and change it to `log.info`, 
but this is not guaranteed to work well. If you are not sure whether `print` will be sent to your Palpable server, use 
`python -u` to start your Server, or set `PYTHONUNBUFFERED=1` as an environment variable, when starting your Server.

## Basic Usage

### Setup Customized Server and Client

```python

# configurations
SERVER_ADDRESS = ("127.0.0.1", 8089)
SERVER_FAMILY = "AF_INET"
SECRET = b"29r8in389rhd"
NUM_OF_WORKERS: int = 8
TASK_TIMEOUT_SECONDS: float = 3600 * 3
RESULT_RETENTION_CAPACITY: int = 100000
RESULT_RETENTION_SECONDS: float = 600

from palpable.servants.server import Server
from palpable.units.client import Client
import tempfile, shutil


class ExampleServer(Server):
    def __init__(self):
        super(ExampleServer, self).__init__(
            logging_folder=tempfile.mkdtemp(),
            address=SERVER_ADDRESS,
            family=SERVER_FAMILY,
            authkey=SECRET,
            num_workers=NUM_OF_WORKERS,
            task_timeout_seconds=TASK_TIMEOUT_SECONDS,
            result_retention_capacity=RESULT_RETENTION_CAPACITY,
            result_retention_seconds=RESULT_RETENTION_SECONDS,
        )

    def close(self):
        super(ExampleServer, self).close()
        shutil.rmtree(self._logging_folder)


class ExampleClient(Client):
    def __init__(self):
        super(ExampleClient, self).__init__(
            address=SERVER_ADDRESS,
            family=SERVER_FAMILY,
            authkey=SECRET
        )

```

### Define a Function

Suppose the following code is in the file `utils.py`

```python
from time import sleep


def square(x):
    sleep(1)
    return x * x

```

### Use Palpable to Map a Function or Call a Function

```python
from time import sleep
from utils import square

if __name__ == "__main__":
    with ExampleServer() as server:
        client = ExampleClient()

        result = client.map(square, range(1000))  # map function `square` with parameters [0, 1, ..., 999]
        print(result)
        result = client.run(square, 4)  # run function `square` with parameter `4`
        print(result)
```

NOICE: it is important to put the `square` function in a different module, otherwise imported function, like `sleep`,
may not be pickled correctly.

In this example, the `with` clause is used to start and stop the server. To do it without `with`:

```python
server = ExampleServer()

# start the server
server.start()

# signal the server to stop
server.stop()

# wait for all processes and threads to end
server.join()

# close the server
server.close()
```

## Advanced Usage

### Define a Customized Procedure

Subclass the Procedure class and implement the run method. The run method will be called by the Workers to do the job.

```python

class Procedure(Immutable):

    def run(self, messenger):
        """
        This method will be called by the Worker to execute in a process.

        Override this method.
        Use __init__ to set any params needed for this call
        The messenger parameter is a Messenger instance

        Use messenger.debug/info/warning/error to send logs
        Use messenger.submit_tasks to submit sub tasks to the server
        Use messenger.query_results to query for results of the submitted sub tasks

        If you call predefined functions in this method, to catch possible `print` in the function, do:
            predefined_function.__globals__["print"] = messenger.print  # inject messenger.print as print
        See the RunFunction procedure as an example

        ATTENTION: do not use multiprocessing in this method.

        :param messenger: Messenger
        :return: The data if the task is successful. The data will be constructed to a successful
            TaskResult by the TaskWorker.
        :raise raise TaskFailed exception with the failed data if the task is unsuccessful. e.g.
            raise TaskFailed("ID not found"). The "ID not found" will be constructed to a failed TaskResult.
            Other exceptions will be caught by the Worker and be constructed to a unsuccessful TaskResult using
            the Exception instance as data
        """
        raise NotImplementedError
```

In the run method, you can submit more tasks or run procedures using the messenger. You can also submit blocking tasks
(that means you wait for the results of these tasks before moving on) in the run method. Palpable will handle and run
the blocking tasks to get the results, even when all the workers are blocked and waiting for results.

Example:

```python

from palpable.units.task import Task
from palpable.procedures.procedure import Procedure


def double(x):
    print(f"processing {x}")
    return 2 * x


class CheckIfOdd(Procedure):
    def __init__(self, nums):
        """
        Check if all the nums are odd numbers
        """
        self.nums = nums

    def run(self, messenger):
        for n in self.nums:
            if n % 2 == 0:
                return False
        return True


class DoubleOddNumberProc(Procedure):
    def __init__(self, nums):
        """
        Check if the nums are all odd, if so double the value of the nums
        :param nums: odd numbers
        """
        self.nums = nums

    def run(self, messenger):
        double.__globals__["print"] = messenger.print  # inject messenger.print as print

        messenger.info("check if the numbers are all odd numbers")
        # submit new CheckIfOdd procedure and wait for results
        check_if_odd_task_result = messenger.run_procedure(CheckIfOdd(self.nums))

        if not check_if_odd_task_result:
            raise Exception("Error: the given numbers are not all odd")

        res = [double(x) for x in self.nums]

        return res


```

### Run the Customized Procedure with parameters

```python
if __name__ == "__main__":
    with ExampleServer() as server:
        client = ExampleClient()

        # this task will succeed
        task_result = client.run_procedure(DoubleOddNumberProc(range(1, 10, 2)))
        print(task_result.is_successful, task_result.data)

        # this task will fail
        task_result = client.run_procedure(DoubleOddNumberProc(range(2, 10, 2)))
        print(task_result.is_successful, task_result.data)
```

### More Usage

Check the source codes, test codes, and examples for more usage
https://github.com/XiaoMutt/palpable

## Mechanism

### How it works

Here is how it works at a high level:

- you start a Palpable Server with n workers
- you submit a Procedure through Client to the Server for the workers to finish
- the Procedure will be wrapped into a Task with a unique task id, and the Task is put into the TaskQueue
- you receive a task ID for future reference
- if any worker is available, it will run the task and put the TaskResult into the ResultCache
- you can query the result cache at any time, using a task ID, to asking for the result of a Task
    - if there is no such Task with the task ID, None will be returned
    - if the task is still running, then you will get a TaskResult whose is_successful attribute is None
    - if the task finished and the result is ready, you will get a TaskResult that has the following attributes:
        - task_id: the task ID
        - is_successful: a boolean to indicate whether the task is successful
        - data: the result data if the task is successful, else the error message
        - followup_task_ids: the task may initiate new tasks. This is a list of task_ids initiated by this task to
          followup. Attention: this TaskResult will then be removed from the ResultCache.

### Architecture

There are three classes that do the heavy lifting: Server, Manager, and Worker. Each of them has a main thread loop that
do some jobs:

- Server: the main thread listens incoming commands and starts a new short-lived thread to handle every received
  commands
- Manager: the main thread periodically prunes the ResultCache
- Worker: the main thread periodically checks for available Tasks to run, if so start the Task in a different Process
  and monitors it

The three classes have the following ownership Server --> Manager --> Worker (TaskQueue & Lock / ResultCache & Lock)

- The Server owns Manager & its thread lock: the threads spawned by the Server use the lock to access the Manager
  concurrently
- The Manager owns several Workers, TaskQueue & its thread lock, ResultCache & its thread lock. The Manager shares the
  TaskQueue & its thread lock and ResultCache & its thread lock with the Workers. Workers and the Manager communicate
  through the TaskQueue and ResultCache
    
