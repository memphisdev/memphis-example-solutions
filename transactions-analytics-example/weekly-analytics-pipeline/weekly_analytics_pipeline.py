import datetime as dt
import json

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
                             "bps-weekly",
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

# created key from year and week of year
def key_by_week(tx):
    year, week, _ = tx["timestamp"].isocalendar()
    key = f"{year}{week:02d}"
    return (key, tx)

flow.map(key_by_week)

# group by week
clock_config = EventClockConfig(lambda tx: tx["timestamp"],
                                wait_for_system_duration=dt.timedelta(days=1))
window_config = SlidingWindow(length=dt.timedelta(days=7),
                              offset=dt.timedelta(days=7),
                              align_to=dt.datetime(2021, 12, 27, tzinfo=dt.timezone.utc)) # a Monday
def build_empty_state():
    return {
        "tx_count" : 0
    }

def adder(state, tx):
    year, week, _ = tx["timestamp"].isocalendar()
    state["year"] = year
    state["week"] = week
    state["tx_count"] += 1
    return state

flow.fold_window("count_by_week", clock_config, window_config, build_empty_state, adder)

# drop key
flow.map(lambda kv: kv[1])

# serialize JSON document
flow.map(json.dumps)

# convert to bytearray
flow.map(lambda s: bytearray(s, "utf-8"))

flow.output("memphis-producer", memphis_sink)
