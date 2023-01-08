from datetime import datetime, timedelta


class LogData:
    paramNames = ("Writing register norm",
                  "Attention_F",
                  "Attention_O",
                  "Average temperature",
                  "FMS no norm",
                  "FMS ready",
                  "GHe Bottles submerged",
                  "Lev_F",
                  "Lev_O",
                  "Level STOP F",
                  "Level STOP O",
                  "Network control",
                  "OE check norm",
                  "OE power off",
                  "OE power on",
                  "Overfill_F",
                  "Overfill_O",
                  "Power on OE",
                  "Power off OE",
                  "Program start",
                  "Program stop",
                  "Stop_F",
                  "Stop_O",
                  "Top-off",
                  "Top-off stop")

    def __init__(self):
        self._log = None
        self._log_started_date = None
        self._time_fms = None
        self._time_utc = None
        self._time_countdown = None
        self._param = None
        self._value = None
        self._prog_start_time = None
        self._ignition_time = None

    def _clear(self):
        """
        Erase all data for processing a new FMS log file
        :return:
        """
        self._log = None
        self._log_started_date = None
        self._time_fms = []
        self._time_utc = []
        self._time_countdown = []
        self._param = []
        self._value = []
        self._prog_start_time = None
        self._ignition_time = None

    def processing(self, log):
        """
        Processing log file data for optimal view in the table
        :param log: Data from FMS log file
        :return:
        """
        self._clear()
        self._log = log
        s_log = self._log.split('\n')
        # Verify opened file. Example of correct first line: Report of  01.10.20 21:32:37.072 net interface
        if not s_log[0].count('Report of') or not s_log[0].count('net interface'):
            return False
        # getting date and time from the log's first line
        t_line = s_log[0].split(' ')
        self._log_started_date = datetime.strptime(t_line[3] + ' ' + t_line[4], '%d.%m.%y %H:%M:%S.%f')

        for i in range(0, len(s_log)):
            s_line = s_log[i].split('\t')
            if len(s_line) == 4 and s_line[1].count("Network control") == 0:
                test_str = s_line[0].strip()
                if test_str.count('.'):
                    time_fms = datetime.strptime(self._log_started_date.date().strftime('%Y-%m-%d')
                                                 + ' ' + s_line[0].strip(), '%Y-%m-%d %H:%M:%S.%f')
                else:
                    time_fms = datetime.strptime(self._log_started_date.date().strftime('%Y-%m-%d')
                                                 + ' ' + s_line[0].strip(), '%Y-%m-%d %H:%M:%S')
                if self._log_started_date > time_fms:
                    time_fms += timedelta(days=1)
                self._time_fms.append(time_fms)
                self._time_utc.append(time_fms)
                self._param.append(s_line[1].strip())
                self._value.append(s_line[2].strip())

        # removing repeats
        for par_name in self.paramNames:
            if par_name.count("Level STOP F") == 0:
                # search first entry for parameter
                pos = -1
                for i in range(0, len(self._param)):
                    if self._param[i] == par_name:
                        pos = i
                        break
                # check for same value entry
                curr_pos = pos + 1
                while curr_pos < len(self._param):
                    if self._param[curr_pos] == par_name:
                        # removing records if value difference less than 0.02
                        if abs(float(self._value[pos]) - float(self._value[curr_pos])) < 0.02:
                            del (self._time_fms[curr_pos])
                            del (self._time_utc[curr_pos])
                            del (self._param[curr_pos])
                            del (self._value[curr_pos])
                        else:
                            pos = curr_pos
                            curr_pos += 1
                    else:
                        curr_pos += 1

        # Searching for appearing PROGRAM START command
        for i in range(len(self._param)):
            if self._param[i].count("Program start") == 1 and int(self._value[i]) == 1:
                self._prog_start_time = self._time_fms[i]
                break

        self._ignition_time_calc()
        # Calculating time for countdown
        for i in range(len(self._time_utc)-1):
            self._time_countdown.append(datetime.strptime(str(self._ignition_time - self._time_utc[i]), "%H:%M:%S.%f"))
        self._time_countdown.append(None)

        return True

    def set_prog_start_time(self, prog_start_time):
        """
        Detecting difference between FMS time and real UTC time via PROGRAM START time.
        Correcting UTC time for FMS log
        :param prog_start_time: The real UTC time of PROGRAM START command
        :return: IGNITION command time
        """
        dt = prog_start_time - self._prog_start_time
        for i in range(len(self._time_utc)):
            self._time_utc[i] = self.time_fms[i] + dt
        self._ignition_time_calc()
        return self._ignition_time

    def _ignition_time_calc(self):
        """
        Calculating time for IGNITION command
        :return:
        """
        for i in range(len(self._param)):
            if self._param[i].count("Power off OE") == 1 and int(self._value[i]) == 1:
                self._ignition_time = self._time_utc[i] + timedelta(seconds=11, milliseconds=247)
                break

    def size(self):
        """
        Size of optimised log (time_fms, time_utc, time_countdown, param, value)
        :return: integer
        """
        return len(self._time_fms)

    @property
    def log_start(self):
        """
        Date and time of FMS log (the first log record)
        :return: datetime
        """
        return self._log_started_date

    @property
    def time_fms(self):
        """
        Returns date and time records from FMS log
        :return: datetime[]
        """
        return self._time_fms

    @property
    def time_utc(self):
        """
        Returns UTC date and time records
        :return: datetime[]
        """
        return self._time_utc

    @property
    def time_countdown(self):
        """
        Returns countdown time records
        :return: datetime[]
        """
        return self._time_countdown

    @property
    def param(self):
        """
        Returns parameters records
        :return: string
        """
        return self._param

    @property
    def value(self):
        """
        Returns values records
        :return: string
        """
        return self._value

    @property
    def prog_start_time(self):
        """
        Returns PROGRAM_START command time
        :return: datetime
        """
        return self._prog_start_time

    @property
    def ignition_time(self):
        """
        Returns IGNITION command time
        :return: datetime
        """
        return self._ignition_time
