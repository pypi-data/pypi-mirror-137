from conductor.automator.task_runner import TaskRunner
from conductor.http.api.task_resource_api import TaskResourceApi
import multiprocessing


class ParallelTaskHandler:
    task_runner_processes = []
    task_client = TaskResourceApi()

    def __init__(self, workers):
        for worker in workers:
            task_runner = TaskRunner(worker)
            process = multiprocessing.Process(
                target=task_runner.run
            )
            self.task_runner_processes.append(process)

    def start(self):
        for task_runner_process in self.task_runner_processes:
            task_runner_process.start()
        for task_runner_process in self.task_runner_processes:
            task_runner_process.join()
