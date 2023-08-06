from typing import List
import abc
import json

def report_to_json(report: 'ProgressReport') -> dict:
    return {
        'step_message': report.step_message,
        'steps': report.steps,
        'completed': report.completed,
        'children': [report_to_json(child) for child in report.children]
    }


class FormalProgressInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        self.__root_progress = None

    def set_root_progress_report(self, progress_report_root: 'ProgressReport'):
        self.__root_progress = progress_report_root
        self.submit()

    def has_root(self) -> bool:
        return self.__root_progress is not None

    def submit(self):
        if self.__root_progress:
            self.send(json.dumps(report_to_json(self.__root_progress)))

    def get_data(self):
        return report_to_json(self.__root_progress)

    @abc.abstractmethod
    def send(self, progress_json: str):
        pass


class ProgressReport:
    def __init__(self, step_message: str, send_handler: FormalProgressInterface, steps: int = 0):
        self.step_message = step_message
        self.steps = steps
        self.send_handler = send_handler
        self.completed = False
        self.children: List[ProgressReport] = []

        if not send_handler.has_root():
            # this is the first report for the given send handler
            # so it automatically becomes the root report
            send_handler.set_root_progress_report(self)

    def complete(self):
        self.completed = True
        # re-submit the now completed report
        self.send_handler.submit()

    def create_subreport(self, step_message: str, steps: int = 0) -> 'ProgressReport':
        child = ProgressReport(step_message=step_message, send_handler=self.send_handler, steps=steps)
        self.children.append(child)
        self.send_handler.submit()
        return child

