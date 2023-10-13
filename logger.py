# pylint: disable-all
import datetime
import json


class Logger:
    def __init__(self) -> None:
        self.logs = []

    def load_json(self, file_path):
        with open(file_path, "r") as f:
            new_logs = json.load(f)
            for log in new_logs:
                self.append_log(data=log.get("data"), source_ip=log.get("source_ip"), time=log.get("time"), id=log.get("id"), format=log.get("format"))

    def dump_json(self, file_path):
        with open(file_path, "w") as f:
            json.dump(self.logs, f, cls=_encoder)

    def append_log(self, data, source_ip, time=datetime.datetime.now(), id=None, format="[$LOGTIME$: log entry from $LOGIP$ ($LOGID$)] $LOGDATA$"):
        log = Log(data=data, source_ip=source_ip, time=time, id=id, format=format)
        self.logs.append(log)

    def __str__(self) -> str:
        return "\n".join([str(log) for log in self.logs])


class Log:
    def __init__(self, data, source_ip, time=datetime.datetime.now(), id=None, format="[$LOGTIME$: log entry from $LOGIP$ ($LOGID$)] $LOGDATA$") -> None:
        self.data = data
        self.source_ip = source_ip
        self.time = time
        self.format = format
        self.id = id

    def __str__(self) -> str:
        log = self.format
        log = log.replace("$LOGTIME$", str(self.time))
        log = log.replace("$LOGIP$", str(self.source_ip))
        log = log.replace("$LOGDATA$", str(self.data))
        log = log.replace("$LOGID$", str(self.id))
        return log
    

class _encoder(json.JSONEncoder):
    def default(self, o):
        if not isinstance(o, Log):
            return str(o)
        return o.__dict__
