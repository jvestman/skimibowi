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

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtWidgets
from generator import generate

class QIComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(QIComboBox, self).__init__(parent)

class Skimibowi(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(Skimibowi, self).__init__(parent)
        self.addPage(MCU(self))
        self.addPage(PowerManagementPage(self))
        self.addPage(PeripheralsPage(self))
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
        for id in self.pageIds():
            pagename = self.page(id).title()
            if id == self.currentId():
                pagename = '<b>' + pagename + '</b>'
            titles += '<p>' + pagename + '</p>'
        self.label.setText(titles)

class MCU(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(MCU, self).__init__(parent)
        self.setTitle("Microcontroller")
        self.comboBox = QIComboBox(self)
        self.comboBox.addItem("ESP-12E")
        self.comboBox.addItem("ESP-07")
        self.comboBox.addItem("Wemos D1 Mini")
        self.comboBox.addItem("ATmega328P")
        self.comboBox.addItem("No MCU")
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
    def __init__(self, parent=None):
        super(PowerManagementPage, self).__init__(parent)
        self.setTitle('Power Management')
        self.label1 = QtWidgets.QLabel('Battery')
        self.powersource = QIComboBox(self)
        self.powersource.addItem("No battery")
        self.powersource.addItem("2xAA - Keystone 2462")
        self.powersource.addItem("2xAAA - Keystone 2468")
        self.powersource.addItem("18650 - Keystone 1042")
        self.powersource.addItem("JST PH S2B")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.powersource)
        self.layout.addWidget(QtWidgets.QLabel("Regulator"))
        self.regulator = QIComboBox(self)
        self.regulator.addItem("No regulator")
        self.regulator.addItem("LD1117S33TR")
        self.regulator.addItem("LD1117S50TR")
        self.regulator.addItem("LP2985-30")
        self.regulator.addItem("LP2985-33")
        self.regulator.addItem("LP2985-50")
        self.layout.addWidget(self.regulator)
        self.layout.addWidget(QtWidgets.QLabel('Battery management'))
        self.battery_management = QIComboBox(self)
        self.battery_management.addItem('No battery management ic')
        self.battery_management.addItem('MCP73871-2AA')
        self.layout.addWidget(self.battery_management)
        self.layout.addWidget(QtWidgets.QLabel("MCU power rail"))
        self.mcurail = QIComboBox(self)
        self.mcurail.addItem("+VBatt")
        self.mcurail.addItem("+3V")
        self.mcurail.addItem("+3V3")
        self.mcurail.addItem("+5V")
        self.layout.addWidget(self.mcurail)
        self.fuse = QtWidgets.QCheckBox("Add fuse holder to batteryline")
        self.layout.addWidget(self.fuse)
        self.switch = QtWidgets.QCheckBox("Add power switch")
        self.layout.addWidget(self.switch)
        self.setLayout(self.layout)
        self.registerField("mcurail", self.mcurail, "currentText")
        self.registerField("powersource", self.powersource, "currentText")
        self.registerField("regulator", self.regulator, "currentText")
        self.registerField("battery_management", self.battery_management, "currentText")
        self.registerField("fuse", self.fuse)
        self.registerField("switch", self.switch)

class FootprintsPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(FootprintsPage, self).__init__(parent)
        self.setTitle("Footprints")
        self.resistor_footprint_label = QtWidgets.QLabel()
        self.resistor_footprint = QIComboBox(self)
        self.resistor_footprint.addItem("THT")
        self.resistor_footprint.addItem("SMD 0402")
        self.resistor_footprint.addItem("SMD 0603")
        self.resistor_footprint.addItem("SMD 0805")
        self.resistor_footprint.addItem("SMD 1206")
        self.resistor_footprint.addItem("SMD 1210")
        self.registerField('resistor_footprint', self.resistor_footprint, 'currentText')
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
        layout.addWidget(self.resistor_footprint_label)
        layout.addWidget(self.resistor_footprint)
        layout.addWidget(self.button_footprint_label)
        layout.addWidget(self.button_footprint)
        layout.addWidget(self.board_footprint_label)
        layout.addWidget(self.board_footprint)
        self.setLayout(layout)

    def initializePage(self):
        self.resistor_footprint_label.setText("Capasitor, resistor and diode form factor")
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
        self.registerField("usb_uart", self.usb_uart, "currentText")
        self.usb_connector_label = QtWidgets.QLabel()
        self.usb_connector_label.setText("USB Connector")
        self.usb_connector = QIComboBox(self)
        self.usb_connector.addItem("No USB connector")
        self.usb_connector.addItem("USB B")
        self.usb_connector.addItem("USB B Mini")
        self.usb_connector.addItem("USB B Micro")
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
        self.onewire_connector.addItem("No Onewire connector")
        self.onewire_connector.addItem("1x3 Pin Header")
        self.onewire_connector.addItem("Screw terminal")
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

class FinalPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(FinalPage, self).__init__(parent)
        self.setTitle("Generate netlist")
        self.filename = QtWidgets.QLineEdit()
        self.filename.setText("mcu.py")
        self.registerField("filename", self.filename)
        self.generate = QtWidgets.QPushButton("&Generate")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.filename)
        layout.addWidget(self.generate)
        self.generate.clicked.connect(self.generate_skidl)
        self.setLayout(layout)

    def generate_skidl(self):

        footprints = {
            'ESP-07': 'RF_Module:ESP-07',
            'ESP-12E': 'RF_Module:ESP-12E',
            'Wemos D1 Mini': 'RF_Module:WEMOS_D1_mini_light',
            'ATmega328P': 'Package_DIP:DIP-28_W7.62mm',
            'No MCU': ''
        }

        battery_footprints = {
            'No battery': '',
            '2xAA - Keystone 2462':'Battery:BatteryHolder_Keystone_2462_2xAA',
            '2xAAA - Keystone 2468': 'Battery:BatteryHolder_Keystone_2468_2xAAA',
            '18650 - Keystone 1042': 'Battery:BatteryHolder_Keystone_1042_1x18650',
            'JST PH S2B': 'JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal'
        }

        regulators = {
            'No regulator': None,
            'LD1117S33TR': { 'module': 'Regulator_Linear', 'part': 'LD1117S33TR_SOT223', 'footprint': 'Package_TO_SOT_SMD:SOT-223-3_TabPin2', 'output': '+3V3'},
            'LD1117S50TR': {'module': 'Regulator_Linear', 'part': 'LD1117S50TR_SOT223', 'footprint': 'Package_TO_SOT_SMD:SOT-223-3_TabPin2', 'output': '+5V'},
            'LP2985-30': {'module': 'Regulator_Linear', 'part': 'LP2985-3.0', 'footprint': 'Package_TO_SOT_SMD:SOT-23-5', 'output': '+3V'},
            'LP2985-33': {'module': 'Regulator_Linear', 'part': 'LP2985-3.3', 'footprint': 'Package_TO_SOT_SMD:SOT-23-5', 'output': '+3V3'},
            'LP2985-50': {'module': 'Regulator_Linear', 'part': 'LP2985-5.0', 'footprint': 'Package_TO_SOT_SMD:SOT-23-5', 'output': '+5V'}
        }

        resistor_footprints = {
            'THT': 'R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal',
            'SMD 0402': 'Resistor_SMD:R_0402_1005Metric',
            'SMD 0603': 'Resistor_SMD:R_0603_1608Metric',
            'SMD 0805': 'Resistor_SMD:R_0805_2012Metric',
            'SMD 1206': 'Resistor_SMD:R_1206_3216Metric',
            'SMD 1210': 'Resistor_SMD:R_1210_3225Metric'
        }

        capacitor_footprints = {
            'THT': '',
            'SMD 0402': 'Capacitor_SMD:C_0402_1005Metric',
            'SMD 0603': 'Capacitor_SMD:C_0603_1608Metric',
            'SMD 0805': 'Capacitor_SMD:C_0805_2012Metric',
            'SMD 1206': 'Capacitor_SMD:C_1206_3216Metric',
            'SMD 1210': 'Capacitor_SMD:C_1210_3225Metric'
        }

        led_footprints = {
            'THT': 'LED_THT:LED_D3.0mm',
            'SMD 0402': 'LED_SMD:LED_0402_1005Metric',
            'SMD 0603': 'LED_SMD:LED_0603_1608Metric',
            'SMD 0805': 'LED_SMD:LED_0805_2012Metric',
            'SMD 1206': 'LED_SMD:LED_1206_3216Metric',
            'SMD 1210': 'LED_SMD:LED_1210_3225Metric'
        }

        usb_connector_footprints = {
            'No USB connector': '',
            'USB B': 'USB_B_OST_USB-B1HSxx_Horizontal',
            'USB B Micro': 'USB_Micro-B_Amphenol_10103594-0001LF_Horizontal',
            'USB B Mini': 'USB_Mini-B_Lumberg_2486_01_Horizontal'
        }

        onewire_connector_footprints = {
            'No Onewire connector': '',
            '1x3 Pin Header': 'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical',
            'Screw terminal': 'TerminalBlock_TE-Connectivity:TerminalBlock_TE_282834-3_1x03_P2.54mm_Horizontal'
        }

        variables = {
            'mcu': self.field("mcu"),
            'mcu_footprint': footprints[self.field("mcu")],
            'mcurail': self.field('mcurail'),
            'powersource': self.field('powersource'),
            'powersource_footprint': battery_footprints[self.field('powersource')],
            'resistor_footprint': resistor_footprints[self.field('resistor_footprint')],
            'capacitor_footprint': capacitor_footprints[self.field('resistor_footprint')],
            'led_footprint': led_footprints[self.field('resistor_footprint')],
            'regulator': regulators[self.field('regulator')],
            'usb_connector_footprint': usb_connector_footprints[self.field('usb_connector')],
            'onewire_connector_footprint': onewire_connector_footprints[self.field('onewire_connector')]
            }

        code = generate(variables, self)

        with open(self.field('filename'), 'w') as file:
            file.write(code)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wizard = Skimibowi()
    wizard.show()
    sys.exit(app.exec_())
