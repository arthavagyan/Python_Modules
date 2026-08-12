#!/usr/bin/env python3
from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._entries: list[Any] = []
        self._released_count = 0

    @abstractmethod
    def validate(self, payload: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, payload: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        self._released_count += 1
        return (self._released_count - 1, self._entries.pop(0))


class NumericProcessor(DataProcessor):
    def validate(self, payload: Any) -> bool:
        if not isinstance(payload, (list, int, float)):
            return False
        if isinstance(payload, (int, float)):
            return True
        return all(isinstance(value, (int, float)) for value in payload)

    def ingest(self, payload: Any) -> None:
        try:
            if not self.validate(payload):
                raise ValueError("Improper numeric data")
            if isinstance(payload, (int, float)):
                self._entries.extend([str(payload)])
            else:
                self._entries.extend([str(value) for value in payload])
        except ValueError as error:
            print(f"Got exception: {error}")


class TextProcessor(DataProcessor):
    def validate(self, payload: Any) -> bool:
        if not isinstance(payload, (list, str)):
            return False
        if isinstance(payload, str):
            return True
        return all(isinstance(value, str) for value in payload)

    def ingest(self, payload: Any) -> None:
        try:
            if not self.validate(payload):
                raise ValueError("Improper Text data")
            if isinstance(payload, str):
                self._entries.extend([payload])
            else:
                self._entries.extend(payload)
        except ValueError as error:
            print(f"Got exception: {error}")


class LogProcessor(DataProcessor):
    def validate(self, payload: Any) -> bool:
        if not isinstance(payload, (dict, list)):
            return False
        if isinstance(payload, dict):
            return (all(isinstance(key, str) and isinstance(value, str)
                    for key, value in payload.items())
                    and len(payload) == 2
                    and 'log_level' in payload
                    and 'log_message' in payload)
        return all(isinstance(key, str) and isinstance(value, str)
                   and len(log_item) == 2
                   and 'log_level' in log_item
                   and 'log_message' in log_item
                   for log_item in payload
                   for key, value in log_item.items())

    def ingest(self, payload: Any) -> None:
        try:
            if not self.validate(payload):
                raise ValueError("Improper Log data")
            if isinstance(payload, dict):
                self._entries.extend([f"{payload['log_level']}:"
                                      f" {payload['log_message']}"])
            else:
                self._entries.extend(
                    [f"{log_item['log_level']}: {log_item['log_message']}"
                     for log_item in payload]
                )
        except ValueError as error:
            print(f"Got exception: {error}")


def test() -> None:
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    numeric_processor = NumericProcessor()
    is_valid = numeric_processor.validate(42)
    print(f" Trying to validate input '42': {is_valid}")
    is_valid = numeric_processor.validate('Hello')
    print(f" Trying to validate input 'Hello': {is_valid}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    print(" ", end="")
    numeric_processor.ingest('foo')
    print(" Processing data: [1, 2, 3, 4, 5]")
    numeric_processor.ingest([1, 2, 3, 4, 5])
    print(" Extracting 3 values...")
    for _ in range(3):
        entry = numeric_processor.output()
        print(f" Numeric value {entry[0]}: {entry[1]}")
    print("\nTesting Text Processor...")
    text_processor = TextProcessor()
    is_valid = text_processor.validate(42)
    print(f" Trying to validate input '42': {is_valid}")
    print(" Processing data: ['Hello', 'Nexus', 'World']")
    text_processor.ingest(['Hello', 'Nexus', 'World'])
    print(" Extracting 1 value...")
    entry = text_processor.output()
    print(f" Text value {entry[0]}: {entry[1]}")
    print("\nTesting Log Processor...")
    log_processor = LogProcessor()
    is_valid = log_processor.validate('Hello')
    print(f" Trying to validate input 'Hello': {is_valid}")
    print(" Processing data: [{'log_level': 'NOTICE', 'log_message': "
          "'Connection to server'}, {'log_level': 'ERROR', 'log_message': "
          "'Unauthorized access!!'}]")
    log_processor.ingest([
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'},
    ])
    print(" Extracting 2 values...")
    for _ in range(2):
        entry = log_processor.output()
        print(f" Log entry {entry[0]}: {entry[1]}")


if __name__ == "__main__":
    test()
