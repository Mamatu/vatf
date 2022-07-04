import datetime
import threading
import logging

from vatf.utils import utils

class LoggerThread(threading.Thread):
    def __init__(self, now, inpath, outpath, config_path, delta = 0.5):
        threading.Thread.__init__(self)
        cfg = config_loader.load(config_path)
        self.now = cfg.convert_to_log_zone(now)
        self.inpath = inpath
        self.outpath = outpath
        self.delta = delta
        self.finish = False
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)
        self.start_line = -1
    def stop(self):
        self.lock.acquire()
        self.finish = True
        logging.debug(f"{self.stop.__name__} invoked")
        self.cv.notifyAll()
        self.lock.release()
        self.join()
    def waitForLine(self):
        self.lock.acquire()
        if self.finish == False and self.start_line == -1:
            self.cv.wait()
        self.lock.release()
    def _sleep(self):
        self.lock.acquire()
        predicate = lambda: not (self.finish == False and self.start_line == -1)
        self.cv.wait_for(predicate = predicate,  timeout = self.delta)
        self.lock.release()
    def run(self):
        logging.debug(f"{self.run.__name__}")
        while not self.finish:
            logging.debug(f"{self.run.__name__} loop again...")
            if self.start_line == -1:
                logging.debug(f"{self.run.__name__} start line not found")
                results = utils.grep_regex_in_line(self.inpath, grep_regex = ".*", match_regex = utils.DATE_REGEX)
                logging.debug(f"{self.run.__name__} founds {len(results)} results")
                for result in results:
                    dt = datetime.datetime.strptime(result.matched[0], utils.DATE_FORMAT)
                    logging.debug(f"{self.run.__name__} founds datetime in line {dt} and compares to {self.now}")
                    diff = dt - self.now
                    logging.debug(f"{self.run.__name__} {diff} > {datetime.timedelta()}")
                    if diff >= datetime.timedelta():
                        self.lock.acquire()
                        self.start_line = result.line_number - 1
                        logging.debug(f"{self.run.__name__} found start line {self.start_line}")
                        self.cv.notifyAll()
                        self.lock.release()
                        break
            if self.start_line > -1:
                with open(self.inpath, "r") as fin:
                    lines = fin.readlines()
                    lines_count = len(lines)
                    lines = lines[self.start_line:]
                    with open(self.outpath, "w") as fout:
                        logging.debug(f"{self.run.__name__} writing {len(lines)} from {lines_count} into {self.outpath}")
                        fout.writelines(lines)
            self._sleep()
