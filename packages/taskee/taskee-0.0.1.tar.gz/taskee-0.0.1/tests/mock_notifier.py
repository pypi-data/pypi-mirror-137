from taskee.notifiers.notifier import Notifier


class MockNotifier(Notifier):
    def send(self, title, message):
        return title, message
