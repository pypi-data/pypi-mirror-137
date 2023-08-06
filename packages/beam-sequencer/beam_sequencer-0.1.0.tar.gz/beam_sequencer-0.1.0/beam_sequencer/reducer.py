from typing import Tuple
from typing import List
from typing import TypeVar
from typing import Callable

import apache_beam as beam
# from apache_beam.transforms.combiners import Top
from apache_beam.transforms import window
from apache_beam.transforms import trigger


K = TypeVar("K")
V = TypeVar("V")


@beam.typehints.with_input_types(V)
@beam.typehints.with_output_types(List[V])
class CustomTopCombinerFn(beam.CombineFn):
    """
    Work-around to https://issues.apache.org/jira/browse/BEAM-12847
    This does not utilize optimized cython & heap-queue implementation,
    that the beam provided TopCombinerFn uses.
    """
    def __init__(self, top_n: int, key:Callable, reverse: bool, *unused_args, **unused_kwargs):
        super().__init__(*unused_args, **unused_kwargs)
        self._top_n = top_n
        self._key = key
        # heap-queue vs collection sort are opposites
        # which is why we do the not.
        self._reverse = not reverse
        self._top_values = []

    def create_accumulator(self, *args, **kwargs):
        mutable_accumulator = []
        return mutable_accumulator

    def add_input(self, mutable_accumulator: List[V], element: V, *args, **kwargs):
        mutable_accumulator.append(element)
        mutable_accumulator.sort(key=self._key, reverse=self._reverse)
        num_elements = len(mutable_accumulator)
        take_n = num_elements if self._top_n > num_elements else self._top_n
        return mutable_accumulator[0:take_n]

    def merge_accumulators(self, accumulators, *args, **kwargs):
        merged = []
        for accum in accumulators:
            merged += accum

        num_elements = len(merged)
        take_n = num_elements if self._top_n > num_elements else self._top_n
        merged.sort(key=self._key, reverse=self._reverse)
        return merged[0:take_n]

    def extract_output(self, accumulator, *args, **kwargs):
        return accumulator

@beam.typehints.with_input_types(Tuple[K, V])
@beam.typehints.with_output_types(Tuple[K, List[V]])
class CombineSequencesByKey(beam.PTransform):
    def __init__(self, key, n, sequence_time_to_live_s):
        super().__init__()
        self.key = key
        self.top_n = n
        self.duration = sequence_time_to_live_s

    def expand(self, pcoll):
        return (
            pcoll
            | "EventWindowing"
            >> beam.WindowInto(
                window.Sessions(self.duration),
                trigger=trigger.Repeatedly(trigger.AfterCount(1)),
                accumulation_mode=trigger.AccumulationMode.ACCUMULATING,
            )
            # | "LastSequence" >> Top().PerKey(self.top_n, key=self.key, reverse=True)
            | "LastSequence" >> beam.CombinePerKey(
                CustomTopCombinerFn(self.top_n, key=self.key, reverse=True)
            )
        )
