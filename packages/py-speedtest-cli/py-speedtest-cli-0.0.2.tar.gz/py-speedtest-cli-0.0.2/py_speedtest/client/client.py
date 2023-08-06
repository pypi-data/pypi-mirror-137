import subprocess
import json

from py_speedtest.models import SpeedtestRun
from py_speedtest.exceptions import SpeedtestError


class SpeedtestClient:
    default_args = [
        "-f",
        "json",
        "-p",
        "no",
    ]

    def __init__(self, *args):
        self.extra_args = args

    @property
    def args(self) -> list[str]:
        return [*self.default_args, *self.extra_args]

    def run(self) -> SpeedtestRun:
        results = subprocess.run(["speedtest", *self.args], stdout=subprocess.PIPE)
        output_serialized = results.stdout.decode("utf-8").strip().split("\n")
        output_deserialized = [json.loads(result) for result in output_serialized]
        parsed_result = {"logs": []}
        for result in output_deserialized:
            if result.get("error"):
                raise SpeedtestError(result)
            result_type = result.pop("type")
            if result_type == "log":
                parsed_result["logs"].append(result)
                continue
            parsed_result[result_type] = result
        return SpeedtestRun(**parsed_result)
