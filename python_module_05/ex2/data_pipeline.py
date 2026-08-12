#!/usr/bin/env python3
from typing import Any, Protocol
from abc import ABC, abstractmethod


class ExportPlugin(Protocol):
    def process_output(self, entries: list[tuple[int, str]]) -> None:
        pass


class JsonExportPlugin:
    def process_output(self, entries: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        mapping = {f"item_{entry[0]}": f"{entry[1]}" for entry in entries}
        print(mapping)


class CsvExportPlugin:
    def process_output(self, entries: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        for entry in entries:
            print(entry[1], end="")
            if entry != entries[-1]:
                print(",", end="")
        print()


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._entries: list[Any] = []
        self._released_count: int = 0

    @abstractmethod
    def validate(self, payload: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, payload: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        self._released_count += 1
        return (self._released_count - 1, self._entries.pop(0))

    def get_counter(self) -> int:
        return self._released_count


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


class DataStream():
    def __init__(self) -> None:
        self._numeric_processor: NumericProcessor
        self._text_processor: TextProcessor
        self._log_processor: LogProcessor
        self._numeric_registered: bool = False
        self._text_registered: bool = False
        self._log_registered: bool = False
        self._numeric_received: int = 0
        self._text_received: int = 0
        self._log_received: int = 0

    def register_processor(self, processor: DataProcessor) -> None:
        if type(processor) is NumericProcessor \
                and not self._numeric_registered:
            self._numeric_processor = processor
            self._numeric_registered = True
        elif type(processor) is TextProcessor and not self._text_registered:
            self._text_processor = processor
            self._text_registered = True
        elif type(processor) is LogProcessor and not self._log_registered:
            self._log_processor = processor
            self._log_registered = True
        else:
            print(f"Procesor {processor} exist or wrong type procesor")

    def process_stream(self, batch: list[Any]) -> None:
        for element in batch:
            if (self._numeric_registered
                    and self._numeric_processor.validate(element)):
                self._numeric_processor.ingest(element)
                if type(element) is list:
                    self._numeric_received += len(element)
                else:
                    self._numeric_received += 1
            elif (self._text_registered
                    and self._text_processor.validate(element)):
                self._text_processor.ingest(element)
                if type(element) is list:
                    self._text_received += len(element)
                else:
                    self._text_received += 1
            elif (self._log_registered
                    and self._log_processor.validate(element)):
                self._log_processor.ingest(element)
                if type(element) is list:
                    self._log_received += len(element)
                else:
                    self._log_received += 1
            else:
                print("DataStream error - Can't process "
                      f"element in stream: {element}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if self._numeric_registered:
            remaining = (self._numeric_received
                         - self._numeric_processor.get_counter())
            print(
                f"Numeric Processor: total {self._numeric_received} items "
                f"processed, remaining {remaining} on processor"
            )
        if self._text_registered:
            remaining = (self._text_received
                         - self._text_processor.get_counter())
            print(
                f"Text Processor: total {self._text_received} items "
                f"processed, remaining {remaining} on processor"
            )
        if self._log_registered:
            remaining = (self._log_received
                         - self._log_processor.get_counter())
            print(
                f"Log Processor: total {self._log_received} items "
                f"processed, remaining {remaining} on processor"
            )
        if (not self._numeric_registered
            and not self._text_registered
                and not self._log_registered):
            print("No processor found, no data")

    def output_pipeline(self, count: int, plugin: ExportPlugin) -> None:
        collected: list[tuple[int, str]] = []
        if self._numeric_registered:
            collected.clear()
            for _ in range(count):
                pending = (self._numeric_received
                           - self._numeric_processor.get_counter())
                if pending:
                    collected.append(self._numeric_processor.output())
            plugin.process_output(collected)
        if self._text_registered:
            collected.clear()
            for _ in range(count):
                pending = (self._text_received
                           - self._text_processor.get_counter())
                if pending:
                    collected.append(self._text_processor.output())
            plugin.process_output(collected)
        if self._log_registered:
            collected.clear()
            for _ in range(count):
                pending = (self._log_received
                           - self._log_processor.get_counter())
                if pending:
                    collected.append(self._log_processor.output())
            plugin.process_output(collected)


def test() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")
    print("\nInitialize Data Stream...\n")
    pipeline = DataStream()
    pipeline.print_processors_stats()
    print("Registering Processors\n")
    numeric_processor = NumericProcessor()
    text_processor = TextProcessor()
    log_processor = LogProcessor()
    pipeline.register_processor(numeric_processor)
    pipeline.register_processor(text_processor)
    pipeline.register_processor(log_processor)
    initial_batch = [
        'Hello world', [3.14, -1, 2.71],
        [{'log_level': 'WARNING',
          'log_message': 'Telnet access! Use ssh instead'},
         {'log_level': 'INFO', 'log_message': 'User wil isconnected'}],
        42, ['Hi', 'five'],
    ]
    print(f"Send first batch of data on stream: {initial_batch}\n")
    pipeline.process_stream(initial_batch)
    pipeline.print_processors_stats()
    print("\nSend 3 processed data from each processor to a CSV plugin:")
    pipeline.output_pipeline(3, CsvExportPlugin())
    print()
    pipeline.print_processors_stats()
    second_batch = [
        21, ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [{'log_level': 'ERROR', 'log_message': '500 server crash'},
         {'log_level': 'NOTICE',
          'log_message': 'Certificate expires in 10 days'}],
        [32, 42, 64, 84, 128, 168], 'World hello',
    ]
    print(f"\nSend another batch of data: {second_batch}\n")
    pipeline.process_stream(second_batch)
    pipeline.print_processors_stats()
    print("\nSend 5 processed data from each processor to a JSON plugin:")
    pipeline.output_pipeline(5, JsonExportPlugin())
    print()
    pipeline.print_processors_stats()


if __name__ == "__main__":
    test()
