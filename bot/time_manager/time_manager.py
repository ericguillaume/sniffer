import time
import threading


class TimeManager:

  mode = "" # "debug", "offline", "live"
  timestamp = None
  end_timestamp = None

  time_changed_event = threading.Event()

  @classmethod
  def set_live(cls):
    TimeManager.mode = "live"

  @classmethod
  def set_offline(cls, timestamp, end_timestamp):
    TimeManager.mode = "offline"
    TimeManager.timestamp = timestamp
    TimeManager.end_timestamp = end_timestamp

  @classmethod
  def set_debug(cls, timestamp, end_timestamp):
    TimeManager.mode = "debug"
    TimeManager.timestamp = timestamp
    TimeManager.end_timestamp = end_timestamp

  @classmethod
  def is_live(cls):
    if TimeManager.mode == "":
      raise Exception("ERROR TimeManager was called but was not set in any mode")
    return TimeManager.mode == "live"

  @classmethod
  def is_offline(cls):
    if TimeManager.mode == "":
      raise Exception("ERROR TimeManager was called but was not set in any mode")
    return TimeManager.mode == "offline"

  @classmethod
  def is_debug(cls):
    if TimeManager.mode == "":
      raise Exception("ERROR TimeManager was called but was not set in any mode")
    return TimeManager.mode == "debug"

  @classmethod
  def get_end_timestamp(cls):
    if TimeManager.mode == "live":
      raise Exception("ERROR TimeManager.get_end_timestamp() was called in live mode")
    return TimeManager.end_timestamp

  @classmethod
  def add_seconds(cls, seconds):
    if TimeManager.mode == "":
      raise Exception("ERROR TimeManager was called but was not set in any mode")
    if TimeManager.is_live():
      should_continue = True
      return should_continue
    else:
      TimeManager.timestamp += seconds
      should_continue = not (TimeManager.timestamp > TimeManager.end_timestamp)
      if should_continue:
        TimeManager.time_changed_event.set()
        TimeManager.time_changed_event.clear()
      else:
        TimeManager.time_changed_event.set() # to unblock all waiting threads and enable them to terminate
      return should_continue

  @classmethod
  def should_continue(cls):
    return not (TimeManager.timestamp > TimeManager.end_timestamp)

  @classmethod
  def time(cls):
    if TimeManager.mode == "":
      raise Exception("ERROR TimeManager was called but was not set in any mode")
    elif TimeManager.mode == "live":
      return time.time()
    else:
      return TimeManager.timestamp


