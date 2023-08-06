import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import StandardOptions

from beam_sequencer.domain import EventAction
from beam_sequencer.options import SequencerOptions
from beam_sequencer.mapper import ParseValidJson
from beam_sequencer.mapper import UserSequenceJson
from beam_sequencer.reducer import CombineSequencesByKey


def run(argv=None):
    pipeline_options = SequencerOptions(argv)
    # for now, only streaming is supported
    pipeline_options.view_as(StandardOptions).streaming = True
    with beam.Pipeline(options=pipeline_options) as p:
        if pipeline_options.input_topic:
            messages = p | "ReadPubSub" >> beam.io.ReadFromPubSub(
                topic=pipeline_options.input_topic, with_attributes=False
            )
        else:
            messages = p | "ReadPubSub" >> beam.io.ReadFromPubSub(
                subscription=pipeline_options.input_subscription, with_attributes=False
            )

        def access_ts(elem: EventAction):
            return elem.timestamp

        combiner = CombineSequencesByKey(
            key=access_ts,
            n=pipeline_options.sequence_length,
            sequence_time_to_live_s=pipeline_options.sequence_ttl,
        )

        output = (
            messages
            | "parseJson" >> beam.ParDo(ParseValidJson())
            | "aggregate" >> combiner
            | "formatOutput" >> beam.ParDo(UserSequenceJson())
        )

        output | beam.io.WriteToPubSub(pipeline_options.output_topic)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
