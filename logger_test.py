# pylint: disable-all
import logger


log = logger.Logger()
log.append_log("hi, cool, wtf", "1.1.1.1")
log.append_log("hi, cool, wtf1", "1.1.1.1")
log.append_log("hi, cool, wtf2", "1.1.1.1")
print(str(log))
log.dump_json("loggerlog.json")
log.logs = []
log.load_json("loggerlog.json")
print(log)
