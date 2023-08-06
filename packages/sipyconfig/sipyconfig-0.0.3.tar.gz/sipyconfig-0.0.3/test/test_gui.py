# pylint: disable=C0114,C0115,C0116,invalid-name,too-few-public-methods,no-name-in-module,attribute-defined-outside-init

from typing import Union, List
from serial import SerialException, SerialTimeoutException

from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QLabel, QScrollArea,
                            QCheckBox, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget,
                            QSpinBox, QRadioButton, QPushButton, QButtonGroup, QComboBox,
                            QLineEdit, QErrorMessage)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QMouseEvent, QIcon

from sipyconfig import SiUSBStation
from sipyconfig.card import SICard
from sipyconfig.comms import ACK, NOACK, Command
from sipyconfig.station import SiError
from sipyconfig.enums import stationmode, com, com_rev
from sipyconfig.utils import is_siac_special_mode, evenhex

class ReadOutThread(QThread):
    cardRead = pyqtSignal(SICard)
    station: SiUSBStation
    should_stop: bool = False

    def setStation(self, station: SiUSBStation):
        self.station = station

    def run(self):
        self.station.ensure_readout()
        while not self.should_stop:
            try:
                ret = self.station.wait_for_si_card(0.1)
                if ret:
                    self.cardRead.emit(ret)
            except SiError:
                pass
        self.should_stop = False

    def setExit(self, do_exit: bool):
        self.should_stop = do_exit

class ReadOutWidget(QScrollArea):
    lineSelected = pyqtSignal(int)
    cardSelected = pyqtSignal(SICard)

    _cards: List[SICard]

    def __init__(self,) -> None:
        super().__init__()
        self._cards = []

        self.main_lay = QGridLayout()

        self._addHeader()

        wid = QWidget()
        wid.setLayout(self.main_lay)
        self.setWidget(wid)

        self.setWidgetResizable(True)

    def _addHeader(self):
        for i, wid in enumerate([QLabel(x) for x in ["#", "Read At", "SI-ID", "First Name", "Last Name", "Records", "Voltage"]]):
            self.main_lay.addWidget(wid, 0, i)
        self.main_lay.setRowStretch(1, 1)
        self.main_lay.setColumnStretch(1, 1)
        self.main_lay.setColumnStretch(3, 1)
        self.main_lay.setColumnStretch(4, 1)

    def _addLine(self, data: 'list'):
        line = self.main_lay.rowCount() # 2
        self.main_lay.setRowStretch(line - 1, 0)

        def mouseEvent(ev: QMouseEvent, line: int = line) -> None:
            if ev.button() == QMouseEvent.LeftButton: # type: ignore
                self.lineSelected.emit(line - 1)

        widgets = [QLabel(str(line - 1))] + [QLabel(str(dat)) for dat in data]
        for i, wid in enumerate(widgets):
            wid.mousePressEvent = mouseEvent # type: ignore
            self.main_lay.addWidget(wid, line - 1, i)
        self.main_lay.setRowStretch(line, 1)

    def addSiCard(self, card: 'SICard'):
        data = [card.read_at, card.number, "", "", len(card.punches), ""]
        self._addLine(data)

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("SPORTident Py-Config")
        try:
            self.setWindowIcon(QIcon("sportident_logo_klein.png"))
        except FileNotFoundError:
            pass

        self.initUI()
        self.initSerial()

    def initUI(self):
        self.main_wid = QTabWidget()

        self.initControlWid()
        self.initSiReadOut()
        self.initDebugWid()

        self.setCentralWidget(self.main_wid)

    def initControlWid(self):
        self.control_lay = QGridLayout()

        select = QButtonGroup()
        self.direct_select = QRadioButton("Direct")
        select.addButton(self.direct_select)
        remote_select = QRadioButton("Remote")
        select.addButton(remote_select)
        self.direct_select.click()
        self.direct_select.toggled.connect(self.switchRemote)
        self.control_lay.addWidget(self.direct_select, 0, 0)
        self.control_lay.addWidget(remote_select, 0, 1)

        reread = QPushButton("read again")
        reread.pressed.connect(self.updateGui)
        self.control_lay.addWidget(reread, 0, 2)

        self.time_wid = QLabel()
        self.control_lay.addWidget(self.time_wid, 1, 0, 1, 2)
        self.time_set_wid = QPushButton("Set Time")
        self.time_set_wid.pressed.connect(self.setTime)
        self.control_lay.addWidget(self.time_set_wid, 1, 2)

        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.updateTime)
        self.time_timer.start(500)

        self.control_lay.addWidget(QLabel("Control Number:"), 2, 0)
        self.control_num_wid = QSpinBox()
        self.control_num_wid.setMinimum(1)
        self.control_num_wid.setMaximum(511)
        self.control_lay.addWidget(self.control_num_wid, 2, 1)

        self.station_mode_wid = QComboBox()
        self.station_mode_wid.addItems(stationmode.__members__.keys())
        self.station_mode_wid.currentTextChanged.connect(lambda x: self.control_num_wid.setDisabled(is_siac_special_mode(getattr(stationmode, x))))
        self.control_lay.addWidget(self.station_mode_wid, 3, 0, 1, 2)

        self.turn_off_wid = QPushButton("Turn Off")
        self.turn_off_wid.pressed.connect(self.turnOff)
        self.control_lay.addWidget(self.turn_off_wid, 3, 2)

        apply = QPushButton("Apply changes")
        apply.pressed.connect(self.applyChanges)
        self.control_lay.addWidget(apply, 4, 0, 1, 2)

        self.control_lay.setRowStretch(self.control_lay.rowCount(), 1)
        self.control_lay.setColumnStretch(self.control_lay.columnCount(), 1)
        self.control_wid = QWidget()
        self.control_wid.setLayout(self.control_lay)

        self.main_wid.addTab(self.control_wid, "SI-Station")

    def initSiReadOut(self):
        self.read_out_lay = QVBoxLayout()

        self.read_out_wid = QWidget()
        self.read_out_wid.setLayout(self.read_out_lay)

        self.read_out_enable_wid = QCheckBox("Enable Read Out")
        self.read_out_enable_wid.toggled.connect(self.toggleReadOut)
        self.read_out_lay.addWidget(self.read_out_enable_wid)

        self.read_out_sub_lay = QHBoxLayout()
        self.read_out_table = ReadOutWidget()
        self.read_out_details = QLabel()
        self.read_out_sub_lay.addWidget(self.read_out_table)
        self.read_out_sub_lay.addWidget(self.read_out_details)
        self.read_out_details.hide()
        self.read_out_lay.addLayout(self.read_out_sub_lay)

        self.read_out_thread = ReadOutThread()
        self.read_out_thread.cardRead.connect(self.read_out_table.addSiCard)

        self.main_wid.currentChanged.connect(lambda x: self.toggleReadOut(False) if x != 1 else '')

        self.main_wid.addTab(self.read_out_wid, "Read Out")

    def initDebugWid(self):
        self.debug_lay = QGridLayout()

        self.debug_command_wid = QComboBox()
        self.debug_command_wid.addItems(com.__members__.keys())
        self.debug_lay.addWidget(self.debug_command_wid, 0, 0)

        self.debug_lay.addWidget(QLabel("Value"), 1, 0)
        self.debug_value_wid = QLineEdit()
        self.debug_lay.addWidget(self.debug_value_wid, 2, 0)

        self.debug_apply_wid = QPushButton("Write!")
        self.debug_apply_wid.pressed.connect(self.debugApply)
        self.debug_lay.addWidget(self.debug_apply_wid, 3, 0)

        self.debug_read_output = QLabel()
        self.debug_read_output.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.debug_lay.addWidget(self.debug_read_output, 4, 0)
        self.debug_read_wid = QPushButton("Read!")
        self.debug_read_wid.pressed.connect(self.debugRead)
        self.debug_lay.addWidget(self.debug_read_wid, 5, 0)

        self.debug_lay.setRowStretch(self.debug_lay.rowCount(), 1)
        self.debug_wid = QWidget()
        self.debug_wid.setLayout(self.debug_lay)

        self.main_wid.addTab(self.debug_wid, "Debug")

    def initSerial(self):
        self.si = SiUSBStation()
        self.si.max_command_tries = 10

        self.read_out_thread.setStation(self.si)

        self.updateGui()

    def updateGui(self):
        try:
            self.si.get_system_info()
            self.si.trigger_feedback(1)
        except SiError as e:
            self.showError(e)
            return
        except SerialException:
            self.initSerial()

        self.control_num_wid.setValue(self.si.control_number)
        self.control_num_wid.setDisabled(self.si.mode == stationmode.SIAC_SPECIAL or self.si.mode == stationmode.SIAC_TEST)
        self.station_mode_wid.setCurrentText(self.si.mode_string)
        self.turn_off_wid.setDisabled(bool(self.si.direct_mode))

    def switchRemote(self, direct: bool):
        try:
            self.si.set_mode_direct(direct)
            self.updateGui()
        except SiError as e:
            self.showError(e)
        except SerialException:
            self.initSerial()

    def turnOff(self):
        try:
            self.si.turn_off()
        except SiError as e:
            self.showError(e)

    def setTime(self):
        try:
            self.si.set_time()
            self.updateGui()
        except SiError as e:
            self.showError(e)

    def updateTime(self):
        new_time = self.si.time
        if new_time:
            new_time.replace(microsecond=0)
            self.time_wid.setText(str(new_time))

    def toggleReadOut(self, enable: bool):
        try:
            if enable:
                self.read_out_thread.setExit(False)
                self.read_out_thread.start()
            else:
                if self.read_out_enable_wid.isChecked():
                    self.read_out_enable_wid.setChecked(False)
                self.read_out_thread.setExit(True)
        except SiError as e:
            self.showError(e)

    def showError(self, ex: Exception):
        dia = QErrorMessage(self)
        dia.showMessage(str(ex))

    def applyChanges(self):
        try:
            self.si.mode = getattr(stationmode, self.station_mode_wid.currentText())
            if self.si.mode != stationmode.SIAC_SPECIAL and self.si.mode != stationmode.SIAC_TEST:
                self.si.control_number = self.control_num_wid.value()
        except SiError as e:
            self.showError(e)
        self.updateGui()

    def debugApply(self):
        command = getattr(com, self.debug_command_wid.currentText())
        a = self.debug_value_wid.text()
        if len(a) % 2 != 0:
            self.showError(ValueError("Need even number of characters to convert to bytes!"))
            return
        value = [int(a[x:x+2], 16) for x in range(0,len(a),2)]
        try:
            self.writeDebugRead(self.si.send_command(command, value, True))
        except SiError as e:
            self.showError(e)
        self.updateGui()

    def writeDebugRead(self, ret: Union[ACK, NOACK, Command]):
        if isinstance(ret, ACK):
            self.debug_read_output.setText("ACK")
        elif isinstance(ret, NOACK):
            self.debug_read_output.setText("NOACK")
        else:
            self.debug_read_output.setText(com_rev.get(ret.command_code, evenhex(ret.command_code)) + " - " + " ".join(evenhex(x) for x in ret.data))

    def debugRead(self):
        try:
            self.writeDebugRead(self.si.receive_command())
        except (SiError, SerialException, SerialTimeoutException) as e:
            self.showError(e)


if __name__ == "__main__":
    import sys
    from os import environ

    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
