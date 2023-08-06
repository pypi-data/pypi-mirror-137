import datetime
import random
from typing import List, Tuple, Type

import ee  # type: ignore

from taskee import events, states
from taskee.dispatcher import Dispatcher
from taskee.notifiers.notifier import Notifier
from taskee.tasks import TaskManager
from taskee.utils import _datetime_to_millis
from tests.mock_tasks import MockTask


class MockTaskee:
    """A mock version of the Taskee class that generates fake, randomized tasks and events.
    This class isn't designed for rigorous testing or to create realistic outputs, and is for
    visualization purposes only.
    """

    def __init__(
        self,
        notifiers: Tuple[str, ...] = ("native",),
        n_tasks: int = 25,
    ):
        """
        Parameters
        ----------
        notifiers : Tuple[str, ...]
            Notifier objects for handling notifications, by name or class.
        """
        self.manager = TaskManager(
            [self.generate_random_task()._status for _ in range(n_tasks)]
        )
        self.dispatcher = Dispatcher(notifiers)

    def _update(self, watch_for: List[Type[events.Event]]) -> List[events.Event]:
        """Update tasks and return any events that occured. Dispatch notifications for events of interest."""
        new_events = []
        max_events = 2
        num_events = 0

        for task in self.manager.tasks:
            rand_event = self.generate_random_event(task)

            if (
                random.random() < 0.2
                and num_events <= max_events
                and rand_event is not None
            ):
                num_events += 1
                task.event = rand_event
                new_events.append(rand_event)

                # if isinstance(event, tuple(watch_for)):
                # self.dispatcher.notify(event.title, event.message)
            else:
                task.event = None

        return new_events

    def generate_random_event(self, task):
        """Choose a random event that would be appropriate to apply to a given task."""
        if task.state == states.RUNNING:
            event_options = (
                events.Attempted,
                events.Cancelled,
                events.Completed,
                events.Failed,
            )
        elif task.state == states.READY:
            event_options = (events.Started,)
        else:
            return None
        return random.choice(event_options)(task)

    def generate_random_task(self):
        state_options = states.ALL
        dataset_options = ["landsat", "s2", "MODIS"]
        variable_options = ["NDVI", "tasseledcap", "burn_severity"]
        year_options = range(2000, 2022)

        rand_dataset = random.choice(dataset_options)
        rand_var = random.choice(variable_options)
        rand_year = str(random.choice(year_options))
        delimiter = random.choice(["_", "."])
        rand_version = random.randint(0, 4)

        task_name = (
            delimiter.join((rand_dataset, rand_var, rand_year, f"v{rand_version}"))
            if rand_version > 0
            else delimiter.join((rand_dataset, rand_var, rand_year))
        )

        rand_state = random.choice(state_options)

        time_since_creation_ms = random.randint(60000, 60000000)

        if rand_state in states.ACTIVE:
            update_timestamp_ms = None
        else:
            elapsed_millis = random.randint(10000, 10000000)
            update_timestamp_ms = (
                _datetime_to_millis(datetime.datetime.now())
                - time_since_creation_ms
                + elapsed_millis
            )

        return MockTask(
            rand_state,
            description=task_name,
            time_since_creation_ms=time_since_creation_ms,
            update_timestamp_ms=update_timestamp_ms,
        )
