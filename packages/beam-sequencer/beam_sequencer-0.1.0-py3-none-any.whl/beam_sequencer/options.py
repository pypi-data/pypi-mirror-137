from apache_beam.options.pipeline_options import PipelineOptions

from beam_sequencer.utils import iso8601_duration_parser


class SequencerOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        input = parser.add_mutually_exclusive_group(required=True)

        input.add_argument(
            "--input_topic",
            help=(
                "Input PubSub topic of the form " '"projects/<PROJECT>/topics/<TOPIC>".'
            ),
        )

        input.add_argument(
            "--input_subscription",
            help=(
                "Input PubSub subscription of the form "
                '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."'
            ),
        )

        parser.add_argument(
            "--output_topic",
            required=True,
            help=(
                "Output PubSub topic of the form "
                '"projects/<PROJECT>/topics/<TOPIC>".'
            ),
        )

        parser.add_argument(
            "--sequence_length",
            type=int,
            metavar="N",
            default=20,
            help=("The max elements per key to output (default is 20)."),
        )

        parser.add_argument(
            "--sequence_ttl",
            type=iso8601_duration_parser,
            metavar="D",
            default="P30D",
            help=(
                "The duration in time before sequence is evicted,"
                " expected string format according to ISO-8601."
            ),
        )
