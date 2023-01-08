from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QDateTimeAxis, QValueAxis
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import Qt
from fmsreplay import Ui_FMSReplay
from datetime import datetime
from log_data import LogData


class MainWindow(QMainWindow, Ui_FMSReplay):
    Success = False

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pBtn_Open.pressed.connect(self.open_log)
        self.lnEd_SetProgStartTime.editingFinished.connect(self.prog_start_time_correction)
        self.pBtn_ZoomReset.clicked.connect(self.zoom_reset)
        self.pBtn_Help.clicked.connect(self.info)
        self.setWindowTitle("FMS Antares Log Viewer")
        self.show()
        self.ld = LogData()

    def info(self):
        """
        Show message window
        :return:
        """
        QMessageBox.about(self, "Info", self.get_help())

    def zoom_reset(self):
        """
        Reset zoom for chart in the current tab
        :return:
        """
        index = self.tabWidget.currentIndex()
        if index == 2:
            self.graphView_F.chart().zoomReset()
        if index == 3:
            self.graphView_O.chart().zoomReset()
        if index == 4:
            self.graphView_FU.chart().zoomReset()
        if index == 5:
            self.graphView_OU.chart().zoomReset()
        if index == 6:
            self.graphView_TFU.chart().zoomReset()

    def open_log(self):
        """Reads FMS log file"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        f_name, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                "All Files (*);;FMS log files (*.txt)", options=options)
        if f_name:
            log = self.read_file(f_name)
            if log == "Oops!":
                QMessageBox.about(self, "Info", "Error reading the FMS log file!")
            else:
                self.lbl_FileName.setText(f_name)
                self.pTxtEd.clear()
                self.pTxtEd.appendPlainText(log)

                if self.ld.processing(log):
                    self.lnEd_SetProgStartTime.setText(self.ld.prog_start_time.strftime('%d.%m.%Y / %H:%M:%S.%f')[:-3])
                    self.lbl_IgnitionTime.setText(self.ld.ignition_time.strftime('%d.%m.%Y / %H:%M:%S.%f')[:-3])
                    self.visualization()
                else:
                    self.clear()
                    QMessageBox.about(self, "Info", "This file is not an FMS log file!")

    def clear(self):
        """
        Hide the all visual data
        :return:
        """
        self.tblWidget.horizontalHeader().hide()
        self.tblWidget.setRowCount(0)
        self.pTxtEd_Report.clear()
        self.graphView_F.hide()
        self.graphView_FU.hide()
        self.graphView_O.hide()
        self.graphView_OU.hide()
        self.graphView_TFU.hide()

    def visualization(self):
        """
        Puts log data into table, calls report method and method for charts plotting.
        :return:
        """
        self.tblWidget.clear()
        self.tblWidget.setColumnCount(5)
        header = ("FMS time", "UTC time", "Countdown", "Parameter", "Value")
        for i in range(0, 5):
            self.tblWidget.setHorizontalHeaderItem(i, QTableWidgetItem(header[i]))
        self.tblWidget.setShowGrid(True)
        self.tblWidget.horizontalHeader().show()
        self.tblWidget.setRowCount(self.ld.size())

        start = True
        for i in range(0, self.ld.size()):
            col_fue = "Attention_F, Average temperature, Lev_F, Level STOP F, Overfill_F, Stop_F"
            col_oxy = "Attention_O, GHe Bottles submerged, Lev_O, Level STOP O, Overfill_O, Stop_O, Top-off, " \
                      "Top-off stop"
            if start:
                color = QBrush(QColor('lightgray'))
                if "Writing register norm".count(self.ld.param[i]):
                    start = False
            elif col_fue.count(self.ld.param[i]):
                color = QBrush(QColor(135, 108, 20))
            elif col_oxy.count(self.ld.param[i]):
                color = QBrush(QColor(29, 128, 161))
            else:
                color = QBrush(QColor('black'))
            # FMS log time
            item = QTableWidgetItem(self.ld.time_fms[i].strftime("%H:%M:%S.%f")[:-3])
            item.setForeground(color)
            self.tblWidget.setItem(i, 0, item)
            # UTC time
            item = QTableWidgetItem(self.ld.time_utc[i].strftime("%H:%M:%S.%f")[:-3])
            item.setForeground(color)
            self.tblWidget.setItem(i, 1, item)
            # Countdown time
            if self.ld.time_countdown[i]:
                item = QTableWidgetItem(self.ld.time_countdown[i].strftime("-%H:%M:%S.%f")[:-3])
                item.setForeground(color)
                self.tblWidget.setItem(i, 2, item)
            # Parameter
            item = QTableWidgetItem(self.ld.param[i])
            item.setForeground(color)
            self.tblWidget.setItem(i, 3, item)
            # Value
            if "Average temperature".count(self.ld.param[i]):
                item = QTableWidgetItem(str(round(float(self.ld.value[i]), 2)) + ' °C')
            else:
                item = QTableWidgetItem(self.ld.value[i])
            item.setForeground(color)
            self.tblWidget.setItem(i, 4, item)
        self.tblWidget.resizeColumnsToContents()

        # Detect abnormal FMS log ending (the launch has been canceled)
        if self.get_first_entry_position(0, "Power off OE", 1) == len(self.ld.param) - 2:
            self.Success = False
            self.lbl_IgnitionTime.setText('Canceled!')
        else:
            self.Success = True
        # Display report data and charts
        self.report()
        self.chart_level("Lev_F", self.graphView_F, True)
        self.chart_level("Lev_O", self.graphView_O, True)
        self.chart_level("Lev_F", self.graphView_FU, False)
        self.chart_level("Lev_O", self.graphView_OU, False)
        self.temper_f_utc()

    def report(self):
        """
        Make report data
        :return:
        """
        self.pTxtEd_Report.clear()
        if not self.Success:
            self.pTxtEd_Report.appendPlainText('\n\t\tTHE LAUNCH HAS BEEN CANCELED!\n')
        rep = "\n********************************************************************************\n" \
              "Parameter\t\t\t\t  UTC time\t\t Countdown\n" \
              "********************************************************************************\n"
        for item in ("Program start", "Power on OE", "OE power on", "FMS ready",
                     "GHe Bottles submerged", "Average temperature", "Level STOP F",
                     "Attention_F", "Stop_F", "Attention_O", "Stop_O", "Power off OE"):
            rep += self.report_line(item)
        rep += "********************************************************************************\n"
        work_ge = self.ld.time_fms[self.get_first_entry_position(0, "Power off OE", 1)] - self.ld.log_start
        rep += f'\nThe operation duration of the FMS GE in the prelaunch operations:\t {str(work_ge)[:-7]}\n'
        work_oe = self.ld.time_fms[self.get_first_entry_position(0, "Power off OE", 1)] \
                  - self.ld.time_fms[self.get_first_entry_position(0, "Power on OE", 1)]
        rep += f'The operation duration of the FMS onboard equipment:\t\t {str(work_oe)[:-7]}'
        self.pTxtEd_Report.appendPlainText(rep)

    def report_line(self, param_name, value=1):
        """
        Returns a line for the report
        :param param_name: Parameter name
        :param value: Value for parameter
        :return: string
        """
        # Specific line for AVERAGE_TEMPERATURE parameter
        if param_name.count("Average temperature") == 1:
            pos = self.get_first_entry_position(0, "Attention_F", 1)
            if pos != -1:
                while self.ld.param[pos].count("Average temperature") != 1 and pos != -1:
                    pos -= 1
                if pos != -1:
                    return "Average temperature".ljust(27, ' ') \
                        + f'\t{self.ld.value[pos][:-3]} °C\t{self.ld.time_utc[pos].strftime("%H:%M:%S.%f")[:-3]}\t' \
                          f'{self.ld.time_countdown[pos].strftime("-%H:%M:%S.%f")[:-3]}\n'
        # Specific line for LEVEL_STOP_F parameter
        elif param_name.count("Level STOP F") == 1:
            pos = -1
            for i in range(0, len(self.ld.time_utc)):
                if self.ld.param[i].count("Level STOP F") == 1:
                    pos = i
            if pos != -1:
                return "Level STOP F".ljust(34, ' ') \
                    + f'\t{self.ld.value[pos]}\t{self.ld.time_utc[pos].strftime("%H:%M:%S.%f")[:-3]}\t' \
                      f'{self.ld.time_countdown[pos].strftime("-%H:%M:%S.%f")[:-3]}\n'
        # Other regular parameters
        else:
            pos = self.get_first_entry_position(0, param_name, value)
            if pos != -1:
                st = param_name
                st = st.ljust(46 - len(param_name), ' ')
                return st + f'\t\t{self.ld.time_utc[pos].strftime("%H:%M:%S.%f")[:-3]}\t' \
                            f'{self.ld.time_countdown[pos].strftime("-%H:%M:%S.%f")[:-3]}\n'

        return f'Параметр <{param_name}> не найден!\n'

    def get_first_entry_position(self, start, param_name, value):
        """
        Searching first entry position for the parameter with given value
        :param start: Position from which search will be started
        :param param_name: Parameter for search (with value)
        :param value: Value for search (with parameter)
        :return: Position of first entry or -1 if search is fail
        """
        for i in range(start, len(self.ld.time_utc)):
            if self.ld.param[i].count(param_name) and int(self.ld.value[i]) == value:
                return i
        return -1

    def chart_level(self, param_name, chart_holder, reverse):
        """
        Plot level charts
        :param param_name: One of these parameters: "Lev_F", "Lev_O"
        :param chart_holder: QChartView object
        :param reverse: False - chart for UTC / True - chart for countdown
        :return:
        """
        series = QLineSeries(self)
        curr_level = 0
        max_level = 0
        times = self.ld.time_countdown if reverse else self.ld.time_utc

        for i in range(0, len(self.ld.param)):
            if "Power off OE".count(self.ld.param[i]):
                series.append(QDateTime(times[i]).toMSecsSinceEpoch(), curr_level)
                break
            if param_name.count(self.ld.param[i]):
                qdt = QDateTime(times[i])
                series.append(qdt.toMSecsSinceEpoch(), curr_level)
                series.append(qdt.toMSecsSinceEpoch(), int(self.ld.value[i]))
                curr_level = int(self.ld.value[i])
                max_level = max([max_level, curr_level])

        max_level = max_level + 1 if max_level < 17 else max_level

        chart = QChart()
        chart.addSeries(series)

        axis_x = QDateTimeAxis()
        axis_x.setFormat("H:mm:ss")
        if reverse:
            axis_x.setRange(QDateTime(1900, 1, 1, 0, 0, 0),
                            QDateTime(self.ld.time_countdown[self.get_first_entry_position(0, param_name, 1)]))
        else:
            axis_x.setRange(QDateTime(self.ld.time_utc[self.get_first_entry_position(0, param_name, 1)]),
                            self.ld.ignition_time)
        axis_x.setTickCount(13)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        chart.axisX().setReverse(True if reverse else False)

        axis_y = QValueAxis()
        axis_y.setLabelFormat("%i")
        axis_y.setRange(0, max_level)
        axis_y.setTickCount(max_level + 1)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart.setTitle("Fuel level" if param_name.count("Lev_F") else "Oxidizer level")
        chart.legend().hide()
        if param_name.count("Lev_F"):
            series.setPen(QPen(Qt.darkYellow, 2))
        chart.legend().setAlignment(Qt.AlignBottom)
        chart_holder.setChart(chart)
        chart_holder.setRubberBand(QChartView.HorizontalRubberBand)
        chart_holder.show()

    def temper_f_utc(self):
        """
        Plot temperature chart
        :return:
        """
        series = QLineSeries()
        prev_value = -200
        max_level = 0
        min_level = 100
        start_time = None
        got_start = False
        for i in range(0, len(self.ld.param)):
            if "Average temperature".count(self.ld.param[i]) and float(self.ld.value[i]) >= 0:
                qdt = QDateTime(self.ld.time_utc[i])
                curr_value = float(self.ld.value[i])
                if round(curr_value * 100) != round(prev_value * 100) and prev_value != -200:
                    series.append(qdt.toMSecsSinceEpoch(), float(prev_value))
                prev_value = float(self.ld.value[i])
                series.append(qdt.toMSecsSinceEpoch(), float(prev_value))
                max_level = max(max_level, prev_value)
                if not got_start:
                    start_time = qdt
                    got_start = True
                else:
                    min_level = min(min_level, prev_value)

        chart = QChart()
        chart.addSeries(series)

        axis_x = QDateTimeAxis()
        axis_x.setFormat("H:mm:ss")
        axis_x.setRange(start_time, self.ld.ignition_time)
        axis_x.setTickCount(13)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        min_level = round(min_level) - 1 if round(min_level) > min_level else round(min_level)
        max_level = round(max_level) + 1 if round(max_level) < max_level else round(max_level)
        axis_y = QValueAxis()
        axis_y.setLabelFormat("%i")
        axis_y.setRange(min_level, max_level)
        axis_y.setTickCount(max_level - min_level + 1)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart.setTitle("Fuel temperature,°C")
        chart.legend().hide()
        series.setPen(QPen(Qt.darkYellow, 2))
        chart.legend().setAlignment(Qt.AlignBottom)
        self.graphView_TFU.setChart(chart)
        self.graphView_TFU.setRubberBand(QChartView.HorizontalRubberBand)
        self.graphView_TFU.show()

    def prog_start_time_correction(self):
        """
        Callback for PROGRAM_START command time correction.
        :return:
        """
        prog_start = datetime.strptime(self.lnEd_SetProgStartTime.text(), '%d.%m.%Y / %H:%M:%S.%f')
        self.lbl_IgnitionTime.setText(
            self.ld.set_prog_start_time(prog_start).strftime('%d.%m.%Y / %H:%M:%S.%f')[:-3])
        self.visualization()

    @staticmethod
    def read_file(filename):
        try:
            f = open(filename, "r")
        except:
            return 'Open file error!'
        else:
            try:
                data = f.read()
            except:
                data = 'Read file error!'
            finally:
                f.close()
        return data

    def get_help(self):
        """
        Reads manual from file and puts in message window
        :param lang:Info language (ua, ru, en)
        :return:
        """
        return self.read_file('Info.txt') + '\n<FMS Antares Log Viewer / Version 0.10.0 / G.Z.>'


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()
