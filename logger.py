# pylint: disable-all
import datetime
import json


class Logger():
    def __init__(self) -> None:
        self.logs = []

    def load_json(self, file_path):
        with open(file_path, "r") as f:
            new_logs = json.load(f)
            for log in new_logs:
                self.append_log(log.get("data"), log.get("source_ip"), log.get("time"), log.get("format"))

    def dump_json(self, file_path):
        with open(file_path, "w") as f:
            json.dump(self.logs, f, cls=_encoder)

    def append_log(self, data, source_ip, time=datetime.datetime.now(), format="[$LOGTIME$: log entry from $LOGIP$] $LOGDATA$"):
        log = Log(data=data, source_ip=source_ip, time=time, format=format)
        self.logs.append(log)

    def __str__(self) -> str:
        return "\n".join([str(log) for log in self.logs])


class Log():
    def __init__(self, data, source_ip, time=datetime.datetime.now(), format="[$LOGTIME$: log entry from $LOGIP$] $LOGDATA$") -> None:
        self.data = data
        self.source_ip = source_ip
        self.time = time
        self.format = format

    def __str__(self) -> str:
        log = self.format
        log = log.replace("$LOGTIME$", str(self.time))
        log = log.replace("$LOGIP$", str(self.source_ip))
        log = log.replace("$LOGDATA$", str(self.data))
        return log
    

class _encoder(json.JSONEncoder):
    def default(self, o):
        if not isinstance(o, Log):
            return str(o)
        return o.__dict__
        
