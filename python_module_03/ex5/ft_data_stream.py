import random
import typing

PLAYER_NAMES = ["bob", "alice", "charlie", "dylan"]
ACTIONS = [
    "run", "eat", "sleep", "grab", "move",
    "climb", "swim", "release", "use",
]

Event = tuple[str, str]


def gen_event() -> typing.Generator[Event, None, None]:
    while True:
        yield random.choice(PLAYER_NAMES), random.choice(ACTIONS)


def consume_event(events: list[Event]) -> typing.Generator[Event, None, None]:
    while events:
        index = random.randrange(len(events))
        yield events.pop(index)


def main() -> None:
    print("=== Game Data Stream Processor ===")

    stream = gen_event()
    for event_number in range(1000):
        name, action = next(stream)
        print(f"Event {event_number}: Player {name} did action {action}")

    ten_events: list[Event] = []
    for _ in range(10):
        ten_events.append(next(stream))
    print(f"Built list of 10 events: {ten_events}")

    for event in consume_event(ten_events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {ten_events}")


if __name__ == "__main__":
    main()
