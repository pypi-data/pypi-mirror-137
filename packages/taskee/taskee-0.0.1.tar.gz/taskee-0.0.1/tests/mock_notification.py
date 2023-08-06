from tests.mock_taskee import MockTaskee

t = MockTaskee(notifiers=("native", "pushbullet"))
# t = MockTaskee(notifiers=["native"])

t.dispatcher.notify(
    title="Task Completed",
    message="Task 's2_nbr' completed successfully! It ran for 14 minutes.",
)
