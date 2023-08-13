import datetime as dt
import json

from bytewax.connectors.stdio import StdOutput
from bytewax.dataflow import Dataflow
from bytewax.window import EventClockConfig
from bytewax.window import TumblingWindow

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
                             "bps-weekly-tx-volume",
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

# group by week
clock_config = EventClockConfig(lambda tx: tx["timestamp"],
                                wait_for_system_duration=dt.timedelta(days=1))
window_config = TumblingWindow(length=dt.timedelta(days=7),
                               align_to=dt.datetime(2021, 12, 27, tzinfo=dt.timezone.utc)) # a Monday
def build_empty_state():
    return {
        "tx_count" : 0
    }

def adder(state, tx):
    year, week, _ = tx["timestamp"].isocalendar()
    # get first day of that week
    week_start = dt.date.fromisocalendar(year, week, 1).isoformat()
    state["week_start"] = week_start
    state["tx_count"] += 1
    return state

flow.fold_window("count_by_week", clock_config, window_config, build_empty_state, adder)

flow.output("print-windows", StdOutput())

# drop key
def extract_value(kv_pair):
    key, value = kv_pair
    return value
flow.map(extract_value)

# serialize JSON document
flow.map(json.dumps)

# convert to bytearray
flow.map(lambda s: bytearray(s, "utf-8"))

flow.output("memphis-producer", memphis_sink)
