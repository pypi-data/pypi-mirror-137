from typing import Callable, List, Dict, Tuple, TypeVar, Union
import views_schema
import pandas as pd
from . import legacy

T = TypeVar("T")
NestedDicts = Dict[str,Dict[str,T]]
TimePeriodGetter = NestedDicts[Callable[[pd.DataFrame], pd.DataFrame]]
PartitionsDicts = NestedDicts[Tuple[int,int]]

gtzero = lambda x: x if x > 0 else 0

class DataPartitioner():
    """
    DataPartitioner
    ===============

    parameters:
        partitions (Union[Dict[str,Dict[str,[Tuple[int,in]]]], views_schema.Partitions])

    A DataPartitioner is a class used to describe and perform time-subsetting
    of doubly-indexed pandas dataframes (Time-Unit). The class also has several
    methods that can be used to manipulate the partitioning definition, like
    padding or trimming the partition sizes, and shifting them left and right.

    The DataPartitioner is callable, and is used like this:

    example:
        partitioner = DataPartitioner({"A":{"train":(1,100)}})
        partitioner("A","train",dataset)

    For more information about the time-partitioning scheme used by the views
    team, see this page:

    https://github.com/prio-data/viewser/wiki/TimePartitioning
    """

    def __init__(self, partitions: Union[PartitionsDicts, views_schema.Partitions]):
        if isinstance(partitions, dict):
            partitions = views_schema.Partitions.from_dict(partitions)

        self.partitions = partitions

    def _map(self, fn):
        return DataPartitioner(self.partitions.map(fn))

    def _pmap(self, fn):
        return DataPartitioner(self.partitions.pmap(fn))

    def _pad(self, size: int):
        sub_from_start = abs(size) if size < 0 else 0
        add_to_end = size if size > 0 else 0
        return self._map(lambda s,e: (s - sub_from_start, e + add_to_end))

    def _trim(self, size: int):
        add_to_start = size if size > 0 else 0
        sub_from_end = abs(size) if size < 0 else 0
        return self._map(lambda s,e: (s + add_to_start, e - sub_from_end))

    def trim(self, size: int):
        """
        trim
        ====

        parameters:
            size (int)

        Trim the right-hand side of the partitions by size steps.
        """
        return self._trim(-gtzero(size))

    def ltrim(self, size):
        """
        trim
        ====

        parameters:
            size (int)

        Trim the left-hand side of the partitions by size steps.
        """
        return self._trim(gtzero(size))

    def pad(self, size: int):
        """
        trim
        ====

        parameters:
            size (int)

        Grow the right-hand side of the partitions by size steps.
        """
        size = size if size > 0 else 0
        return self._pad(size)

    def lpad(self, size: int):
        """
        trim
        ====

        parameters:
            size (int)

        Grow the left-hand side of the partitions by size steps.
        """
        size = size if size > 0 else 0
        return self._pad(-size)

    def no_overlap(self, rev:bool = False):
        """
        no_overlap
        ==========

        parameters:
            rev (bool)

        Ensure that there is no overlap between the contained partitions.
        """
        return self._pmap(lambda p: p.no_overlap(rev = rev))

    def in_extent(self, start: int, end: int):
        """
        in_extent
        =========

        parameters:
            start (int)
            end (int)

        Ensure that partitions are within the extent start --- end
        """
        return self._map(lambda s,e: (s if s > start else start, e if e < end else end))

    def extent(self) -> views_schema.TimeSpan:
        """
        extent
        ======

        Return the extent of the contained partitions as a views_schema.partitioning.TimeSpan.
        """
        return self.partitions.extent()

    def shift_left(self, size: int) -> 'DataPartitioner':
        """
        shift_left
        ==========

        parameters:
            size (int)

        Shifts the contained partitions size steps to the left.
        """
        start,end = self.extent()
        return (self
                .lpad(size)
                .no_overlap(rev = True)
                .in_extent(start, end))

    def shift_right(self, size: int)-> 'DataPartitioner':
        """
        shift_left
        ==========

        parameters:
            size (int)

        Shifts the contained partitions size steps to the right.
        """
        start,end = self.extent()
        return (self
                .pad(size)
                .no_overlap()
                .in_extent(start, end))

    def __call__(self,
            partition_name: str,
            time_period_name: str,
            data: pd.DataFrame)-> pd.DataFrame:
        timespan = self.partitions.partitions[partition_name].timespans[time_period_name]
        return data.loc[timespan.start : timespan.end, :]

    @classmethod
    def from_legacy_periods(cls, periods: List[legacy.Period]):
        for p in periods:
            try:
                legacy.period_object_is_valid(p)
            except AssertionError:
                raise ValueError(f"Period {p} is not a valid time period object")

        partitions = {}
        for period in periods:
            partitions[period.name] = {
                    "train": (period.train_start, period.train_end),
                    "predict": (period.predict_start, period.predict_end),
                    }

        return cls(partitions)
