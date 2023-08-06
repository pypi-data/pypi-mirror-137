from operator import and_
from dataclasses import dataclass
from toolz.functoolz import reduce, curry, compose

@dataclass
class Period:
    """
    A named timeperiod for dividing data into a training and a predicting partition.
    """
    name: str
    train_start: int
    train_end: int
    predict_start: int
    predict_end: int

as_time_periods = lambda p: ((p.train_start,p.train_end), (p.predict_start, p.predict_end))

valid_time_periods = lambda periods: reduce(and_, map(
    lambda p: (p[0] < p[1]) & (p[0] >= 0),
    periods))
period_gt = lambda periods: periods[0][1]<periods[1][0]

period_object_is_valid = compose(
        lambda periods: reduce(and_,map(lambda fn: fn(periods),[
            period_gt,
            valid_time_periods
            ])),
        as_time_periods)
