import datetime as dt
import json

from bytewax.connectors.stdio import StdOutput
from bytewax.dataflow import Dataflow
from bytewax.window import EventClockConfig
from bytewax.window import SlidingWindow

from memphis.connectors.bytewax import MemphisInput
from memphis.connectors.bytewax import MemphisOutput

memphis_src = MemphisInput("localhost",
                           "testuser",
                           "%o3sH$Qfae",
                           "bps-transactions",
                           "weekly-pipeline",
                           replay_messages = True)

memphis_sink = MemphisOutput("localhost",
                             "testuser",
                             "%o3sH$Qfae",
                             "bps-wow-tx-volume",
                             "weekly-pipeline")

flow = Dataflow()
flow.input("memphis-consumer", memphis_src)

# bytearray to UTF-8 string
flow.map(lambda m: m.decode("utf-8"))

# deserialize JSON document
flow.map(json.loads)

# parse datetime
def parse_datetime(tx):
    tx["timestamp"] = dt.datetime.fromisoformat(tx["timestamp"]).astimezone(dt.timezone.utc)
    return tx

flow.map(parse_datetime)

# windowing functions need a key
# but we have just one stream
def create_kv_pair(tx):
    return ("ALL", tx)

flow.map(create_kv_pair)

# calculate tx counts over pairs of consecutive weeks
clock_config = EventClockConfig(lambda tx: tx["timestamp"],
                                wait_for_system_duration=dt.timedelta(days=1))
window_config = SlidingWindow(length=dt.timedelta(days=14),
                              offset=dt.timedelta(days=7),
                              align_to=dt.datetime(2021, 12, 27, tzinfo=dt.timezone.utc)) # a Monday
def build_empty_state():
    return { }

def adder(state, tx):
    year, week, _ = tx["timestamp"].isocalendar()
    key = (year, week)
    state[key] = state.get(key, 0) + 1
    return state

flow.fold_window("count_by_week", clock_config, window_config, build_empty_state, adder)

# drop key
def extract_value(kv_pair):
    key, value = kv_pair
    return value
flow.map(extract_value)

# only keep records which include 2 weeks
flow.filter(lambda wow_ratios: len(wow_ratios) == 2)

def calculate_wow(kv_pair):
    week_counts = list(kv_pair.items())
    week_counts.sort()

    first_week, second_week = week_counts

    wow = first_week[1] / second_week[1]
    first_year, first_week = first_week[0]
    second_year, second_week = second_week[0]

    return {
        "wow" : wow,
        "week1_start_date" : dt.date.fromisocalendar(first_year, first_week, 1).isoformat(),
        "week1_end_date" : dt.date.fromisocalendar(first_year, first_week, 7).isoformat(),
        "week2_start_date" : dt.date.fromisocalendar(second_year, second_week, 1).isoformat(),
        "week2_end_date" : dt.date.fromisocalendar(second_year, second_week, 7).isoformat()
    }

flow.map(calculate_wow)

flow.output("print-sliding-wow", StdOutput())

# serialize JSON document
flow.map(json.dumps)

# convert to bytearray
flow.map(lambda s: bytearray(s, "utf-8"))

flow.output("memphis-producer", memphis_sink)
