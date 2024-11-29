from log_analyser.io.output.base import OutputWriter
from log_analyser.io.output.json import JSONOutputWriterStrategy

output_writer = OutputWriter()
output_writer.register("json", JSONOutputWriterStrategy())

__all__ = ["output_writer"]
