#!/usr/bin/env python

#    Skimibowi - SKiDL Microcontroller Board Wizard
#    Copyright (C) 2019  Jussi Vestman
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from controller import footprints, battery_footprints, regulators, resistor_footprints, usb_connector_footprints, fuse_footprints, onewire_connector_footprints, load_settings, generate_skidl, generate_from_settings

class QIComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(QIComboBox, self).__init__(parent)


class Skimibowi(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(Skimibowi, self).__init__(parent)
        self.addPage(MCU(self))
        self.addPage(PowerManagementPage(self))
        self.addPage(PeripheralsPage(self))
        self.addPage(SerialSettingsPage(self))
        self.addPage(FootprintsPage(self))
        self.addPage(FinalPage(self))
        self.setWindowTitle("Skidl Microcontroller Board  Wizard")
        self.label = QtWidgets.QLabel("")
        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.setSideWidget(self.label)
        self.currentIdChanged.connect(self.id_changed)
        self.resize(640, 480)


    def id_changed(self):
        """Update wizard pages list in the left side pane of the Wizard"""
        titles = ""
        for page_id in self.pageIds():
            pagename = self.page(page_id).title()
            if page_id == self.currentId():
                pagename = '<b>' + pagename + '</b>'
            titles += '<p>' + pagename + '</p>'
        self.label.setText(titles)


class MCU(QtWidgets.QWizardPage):
    """Wizard page for configuring the MCU being used"""

    def __init__(self, parent=None):
        super(MCU, self).__init__(parent)
        self.setTitle("Microcontroller")
        self.comboBox = QIComboBox(self)
        self.comboBox.addItems(footprints.keys())
        self.resetButton = QtWidgets.QCheckBox("Reset button")
        self.resetLine = QtWidgets.QCheckBox("Reset line")
        self.flashButton = QtWidgets.QCheckBox("Flash button")
        self.ftdi_header = QtWidgets.QCheckBox("FTDI header")
        self.led = QtWidgets.QCheckBox("Power-on led on GPIO0")
        self.icsp = QtWidgets.QCheckBox("ICSP header")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(self.resetButton)
        layout.addWidget(self.resetLine)
        layout.addWidget(self.flashButton)
        layout.addWidget(self.ftdi_header)
        layout.addWidget(self.led)
        layout.addWidget(self.icsp)
        self.registerField("mcu", self.comboBox, "currentText")
        self.registerField("reset", self.resetLine)
        self.registerField("Reset button", self.resetButton)
        self.registerField("Flash button", self.flashButton)
        self.registerField("FTDI header", self.ftdi_header)
        self.registerField("led", self.led)
        self.registerField("icsp", self.icsp)
        self.setLayout(layout)


class PowerManagementPage(QtWidgets.QWizardPage):
    """Wizard page for configuring board power management devices and networks"""

    def __init__(self, parent=None):
        super(PowerManagementPage, self).__init__(parent)
        self.setTitle('Power Management')
        self.label1 = QtWidgets.QLabel('Battery')
        self.powersource = QIComboBox(self)
        self.powersource.addItems(battery_footprints.keys())
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.powersource)
        self.layout.addWidget(QtWidgets.QLabel("Regulator"))
        self.regulator = QIComboBox(self)
        self.regulator.addItems(regulators.keys())
        self.layout.addWidget(self.regulator)
        self.caps = QtWidgets.QGroupBox("Regulator bypass capasitors")
        self.caps.layout = QtWidgets.QHBoxLayout()
        self.caps.setLayout(self.caps.layout)
        self.layout.addWidget(self.caps)
        self.caps.layout.addWidget(QtWidgets.QLabel("Vin"))
        self.vin_bypass_cap = QtWidgets.QLineEdit()
        self.caps.layout.addWidget(self.vin_bypass_cap) 
        self.caps.layout.addWidget(QtWidgets.QLabel("Vout"))
        self.vout_bypass_cap = QtWidgets.QLineEdit()
        self.caps.layout.addWidget(self.vout_bypass_cap)
        self.layout.addWidget(QtWidgets.QLabel('Battery management')) 
        self.battery_management = QIComboBox(self)
        self.battery_management.addItem('No battery management ic')
        self.battery_management.addItem('MCP73871-2AA')
        self.battery_management.addItem('MCP73831')
        self.layout.addWidget(self.battery_management)
        self.layout.addWidget(QtWidgets.QLabel("MCU power rail"))
        self.mcurail = QIComboBox(self)
        self.mcurail.addItems(["+VBatt", "+3V", "+3V3", "+5V"])
        self.layout.addWidget(self.mcurail)
        self.layout.addWidget(QtWidgets.QLabel("Fuse"))
        self.fuse = QIComboBox(self)
        self.fuse.addItems(fuse_footprints.keys())
        self.layout.addWidget(self.fuse)
        self.switch = QtWidgets.QCheckBox("Add power switch")
        self.layout.addWidget(self.switch)
        self.autoselect = QtWidgets.QCheckBox("+5V/USB Auto Selector")
        self.layout.addWidget(self.autoselect)
        self.setLayout(self.layout)
        self.registerField("mcurail", self.mcurail, "currentText")
        self.registerField("powersource", self.powersource, "currentText")
        self.registerField("regulator", self.regulator, "currentText")
        self.registerField("regulator_vin_bypass_cap", self.vin_bypass_cap)
        self.registerField("regulator_vout_bypass_cap", self.vout_bypass_cap)
        self.registerField("battery_management", self.battery_management, "currentText")
        self.registerField("fuse", self.fuse, "currentText")
        self.registerField("switch", self.switch)
        self.registerField("autoselect", self.autoselect)


class FootprintsPage(QtWidgets.QWizardPage):
    """Wizard page for configuring default footprints for classes of devices and board footprint"""

    def __init__(self, parent=None):
        super(FootprintsPage, self).__init__(parent)
        self.setTitle("Footprints")
        self.common_footprint_label = QtWidgets.QLabel()
        self.common_footprint = QIComboBox(self)
        self.common_footprint.addItems(resistor_footprints.keys())
        self.registerField('common_footprint', self.common_footprint, 'currentText')

        self.transistor_footprint_label = QtWidgets.QLabel()
        self.transistor_footprint_label.setText("Transistor footprint")
        self.transistor_footprint = QIComboBox(self)
        self.transistor_footprint.addItems(["THT", "SOT-223", "SOT-23"])
        self.registerField('transistor_footprint', self.transistor_footprint, 'currentText')

        self.button_footprint_label = QtWidgets.QLabel()
        self.button_footprint_label.setText("Tactile button footprint")
        self.button_footprint = QIComboBox(self)
        self.button_footprint.addItem("b3u-1000")
        self.registerField('button_footprint', self.button_footprint, 'currentText')
        self.board_footprint_label = QtWidgets.QLabel()
        self.board_footprint = QIComboBox(self)
        self.board_footprint.addItem("None")
        self.board_footprint.addItem("Arduino Uno R3")
        self.board_footprint.addItem("Arduino Nano")
        self.board_footprint.addItem("Wemos D1 Mini")
        self.board_footprint.addItem("Adafruit Feather")
        self.registerField('board_footprint', self.board_footprint, 'currentText')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.common_footprint_label)
        layout.addWidget(self.common_footprint)
        layout.addWidget(self.transistor_footprint_label)
        layout.addWidget(self.transistor_footprint)
        layout.addWidget(self.button_footprint_label)
        layout.addWidget(self.button_footprint)
        layout.addWidget(self.board_footprint_label)
        layout.addWidget(self.board_footprint)
        self.setLayout(layout)


    def initializePage(self):
        self.common_footprint_label.setText("Capasitor, resistor and diode form factor")
        self.board_footprint_label.setText("Board outline footprint")


class PeripheralsPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(PeripheralsPage, self).__init__(parent)
        self.setTitle("Peripherals")
        self.peripherals = {}
        self.usb_uart_label = QtWidgets.QLabel()
        self.usb_uart_label.setText("USB Uart")
        self.usb_uart = QIComboBox(self)
        self.usb_uart.addItem("No USB")
        self.usb_uart.addItem("FT231")
        self.usb_uart.addItem("FT232RL")
        self.usb_uart.addItem("CP2102N-A01-GQFN24")
        self.usb_uart.addItem("CP2104")
        self.registerField("usb_uart", self.usb_uart, "currentText")
        self.usb_connector_label = QtWidgets.QLabel()
        self.usb_connector_label.setText("USB Connector")
        self.usb_connector = QIComboBox(self)
        self.usb_connector.addItems(usb_connector_footprints.keys())
        self.registerField("usb_connector", self.usb_connector, "currentText")
        self.adc_label = QtWidgets.QLabel()
        self.adc_label.setText("ADC pin")
        self.adc_voltage_divider = QtWidgets.QComboBox()
        self.adc_voltage_divider.addItems(['1.0V', '3.0V', '3V3', '4.5V', '5V', '6V', '9V', '12V', '24V'])
        self.onewire_label = QtWidgets.QLabel()
        self.onewire_label.setText("Onewire")
        self.peripherals["DS18B20"] = QtWidgets.QCheckBox("DS18B20")
        self.registerField("DS18B20", self.peripherals["DS18B20"])
        self.peripherals["DS18B20U"] = QtWidgets.QCheckBox("DS18B20U")
        self.registerField("DS18B20U", self.peripherals["DS18B20U"])
        self.onewire_connector_label = QtWidgets.QLabel()
        self.onewire_connector_label.setText("Onewire connector")
        self.onewire_connector = QtWidgets.QComboBox()
        self.onewire_connector.addItems(onewire_connector_footprints.keys())
        self.registerField("onewire_connector", self.onewire_connector, "currentText")
        self.spi_label = QtWidgets.QLabel()
        self.spi_label.setText("SPI")
        self.i2c_label = QtWidgets.QLabel()
        self.i2c_label.setText("I2C")
        self.peripherals["ina219"] = QtWidgets.QCheckBox("INA219")
        self.registerField("ina219", self.peripherals["ina219"])
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.usb_uart_label)
        layout.addWidget(self.usb_uart)
        layout.addWidget(self.usb_connector_label)
        layout.addWidget(self.usb_connector)
        layout.addWidget(self.adc_label)
        layout.addWidget(self.adc_voltage_divider)
        layout.addWidget(self.onewire_label)
        layout.addWidget(self.peripherals["DS18B20"])
        layout.addWidget(self.peripherals["DS18B20U"])
        layout.addWidget(self.onewire_connector_label)
        layout.addWidget(self.onewire_connector)
        layout.addWidget(self.spi_label)
        layout.addWidget(self.i2c_label)
        layout.addWidget(self.peripherals["ina219"])
        self.setLayout(layout)


class SerialSettingsPage(QtWidgets.QWizardPage):
    """Wizard page for configuring serial bus connected peripherals"""
    def __init__(self, parent=None):
        super(SerialSettingsPage, self).__init__(parent)
        self.setTitle("Serial devices")
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QtWidgets.QLabel('HC-12'))
        self.hc12 = QtWidgets.QCheckBox("HC-12")
        self.layout.addWidget(self.hc12)
        self.registerField('hc12', self.hc12)


class FinalPage(QtWidgets.QWizardPage):
    """Wizard page for generating SKiDL source code"""
    def __init__(self, parent=None):
        super(FinalPage, self).__init__(parent)
        self.setTitle("Generate Skidl")
        self.filename_label = QtWidgets.QLabel("Filename")
        self.filename = QtWidgets.QLineEdit()
        self.filename.setText("mcu.py")
        self.pcb_title_label = QtWidgets.QLabel("Title")
        self.pcb_title = QtWidgets.QLineEdit()
        self.author_label = QtWidgets.QLabel("Author")
        self.author = QtWidgets.QLineEdit()
        self.generate_labels = QtWidgets.QCheckBox("Generate subcircuit labels")
        self.registerField("filename", self.filename)
        self.registerField("generate_labels", self.generate_labels)
        self.registerField("title", self.pcb_title)
        self.registerField("author", self.author)
        self.generate = QtWidgets.QPushButton("&Generate")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.filename_label)
        layout.addWidget(self.filename)
        layout.addWidget(self.pcb_title_label)
        layout.addWidget(self.pcb_title)
        layout.addWidget(self.author_label)
        layout.addWidget(self.author)
        layout.addWidget(self.generate_labels)
        layout.addWidget(self.generate)
        self.generate.clicked.connect(self.generate_handler)
        self.setLayout(layout)


    def generate_handler(self):
        generate_skidl(self)


if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser(description='Skimibowi - SKiDL Microcontroller Board Wizard')
    parser.add_argument('--no-window', metavar='FILE', help='Do not show ui, but generate SKiDL from settings.yml')
    parser.add_argument('-f', metavar='settings.yml', help='Settings.yml filename')
    args = parser.parse_args()
    settings_file = args.f or 'settings.yml'

    if args.no_window:
        generate_from_settings(args.no_window, settings_file)
    else:
        app = QtWidgets.QApplication(sys.argv)
        wizard = Skimibowi()
        wizard.show()
        load_settings(wizard, settings_file)
        sys.exit(app.exec_())
