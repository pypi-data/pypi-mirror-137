from conductor.automator.parallel_task_handler import ParallelTaskHandler
from conductor.worker.worker_interface import WorkerInterface
import logging
import multiprocessing
import socket


class SimplePythonWorker(WorkerInterface):
    def get_task_definition_name(self):
        return 'simple_python_worker'

    def execute(self, task_result):
        task_result.add_output_data('hostname', socket.gethostname())
        task_result.add_output_data('cpu_cores', multiprocessing.cpu_count())
        return task_result

    def get_polling_interval(self):
        return 2


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    workers = [SimplePythonWorker()] * 8
    task_runner = ParallelTaskHandler(workers)
    task_runner.start()


if __name__ == '__main__':
    main()
