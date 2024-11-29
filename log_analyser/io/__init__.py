from log_analyser.io.input.base import InputParser
from log_analyser.io.input.csv import CSVInputParserStrategy
from log_analyser.io.output.base import OutputWriter
from log_analyser.io.output.json import JSONOutputWriterStrategy

output_writer = OutputWriter()
output_writer.register("json", JSONOutputWriterStrategy)

input_parser = InputParser()
input_parser.register("csv", CSVInputParserStrategy)
input_parser.register("log", CSVInputParserStrategy)

__all__ = ["output_writer", "input_parser"]
