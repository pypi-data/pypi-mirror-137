import json

from typing import List
from typing import Tuple

import apache_beam as beam

from beam_sequencer.domain import User
from beam_sequencer.domain import EventAction


@beam.typehints.with_input_types(bytes)
@beam.typehints.with_output_types(Tuple[User, EventAction])
class ParseValidJson(beam.DoFn):
    def process(self, element):
        data = json.loads(element.decode("utf-8"))
        userid = data["uId"] if data["uId"] != "" else data["sId"]
        timestamp = int(data["timestamp"])
        for field in data["parameters"]:
            if field["name"] == "article":
                yield User(id=userid), EventAction(
                    timestamp=timestamp, article=field["value_string"],
                )


@beam.typehints.with_input_types(Tuple[User, List[EventAction]])
@beam.typehints.with_output_types(bytes)
class UserSequenceJson(beam.DoFn):
    def process(self, element):
        action_history = [e.article for e in element[1]]
        yield json.dumps(
            {"id": element[0].id, "seq": action_history}
        ).encode("utf-8")
