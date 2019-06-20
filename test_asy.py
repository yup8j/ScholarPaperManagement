from flask import Flask
from time import sleep
from concurrent.futures import ThreadPoolExecutor

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
executor = ThreadPoolExecutor(10)

app = Flask(__name__)


@app.route('/jobs')
def run_jobs():
    executor.submit(some_long_task1).result()
    executor.submit(some_long_task2, 'hello', 123)
    return 'Two jobs was launched in background!'


def some_long_task1():
    print("Task #1 started!")
    sleep(10)
    print("Task #1 is done!")
    return 1


def some_long_task2(ar, arg2):
    print("Task #2 started with args: %s %s!" % (ar, arg2))
    sleep(5)
    print("Task #2 is done!")


if __name__ == '__main__':
    app.run()