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
        self.addPage(GeneralPage(self))
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
        self.resetButton = QtWidgets.QCheckBox("Reset button")
        self.resetLine = QtWidgets.QCheckBox("Reset line")
        self.flashButton = QtWidgets.QCheckBox("Flash button")
        self.ftdi_header = QtWidgets.QCheckBox("FTDI header")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(self.resetButton)
        layout.addWidget(self.resetLine)
        layout.addWidget(self.flashButton)
        layout.addWidget(self.ftdi_header)
        self.registerField("mcu", self.comboBox, "currentText")
        self.registerField("reset", self.resetLine)
        self.registerField("Reset button", self.resetButton)
        self.registerField("Flash button", self.flashButton)
        self.registerField("FTDI header", self.ftdi_header)
        self.setLayout(layout)

class PowerManagementPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(PowerManagementPage, self).__init__(parent)
        self.setTitle('Power Management')
        self.label1 = QtWidgets.QLabel('Battery')
        self.powersource = QIComboBox(self)
        self.powersource.addItem("No battery")
        self.powersource.addItem("2x1.5V AA - Keystone 2462")
        self.powersource.addItem("2x1.5V AAA battery holder")
        self.powersource.addItem("3.7V Li-ion 18650 battery holder")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.powersource)
        self.layout.addWidget(QtWidgets.QLabel("Regulator"))
        self.regulator = QIComboBox(self)
        self.regulator.addItem("LD1117S33TR")
        self.regulator.addItem("LD1117S50TR")
        self.regulator.addItem("LP2985-33DBVR")
        self.regulator.addItem("LP2985-50DBVR")
        self.layout.addWidget(self.regulator)
        self.layout.addWidget(QtWidgets.QLabel("MCU power rail"))
        self.mcurail = QIComboBox(self)
        self.mcurail.addItem("+VBatt")
        self.mcurail.addItem("+3V")
        self.mcurail.addItem("+3V3")
        self.mcurail.addItem("+5V")
        self.layout.addWidget(self.mcurail)
        self.setLayout(self.layout)
        self.registerField("mcurail", self.mcurail, "currentText")
        self.registerField("powersource", self.powersource, "currentText")
        self.registerField("regulator", self.regulator, "currentText")

class GeneralPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(GeneralPage, self).__init__(parent)
        self.setTitle("Passive footprints")
        self.label1 = QtWidgets.QLabel()
        self.componentType = QIComboBox(self)
        self.componentType.addItem("THT")
        self.componentType.addItem("SMD 0402")
        self.componentType.addItem("SMD 0603")
        self.componentType.addItem("SMD 0805")
        self.componentType.addItem("SMD 1206")
        self.componentType.addItem("SMD 1210")
        self.registerField('resistor_footprint', self.componentType, 'currentText')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.componentType)
        self.setLayout(layout)

    def initializePage(self):
        self.label1.setText("Capasitor, resistor and diode form factor")
        
class PeripheralsPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(PeripheralsPage, self).__init__(parent)
        self.setTitle("Peripherals")
        self.peripherals = {}
        self.serial_label = QtWidgets.QLabel()
        self.serial_label.setText("Serial")
        self.usb_serial = QIComboBox(self)
        self.usb_serial.addItem("No USB")
        self.usb_serial.addItem("FTDI & USB mini connector")
        self.usb_serial.addItem("FTDI & USB micro connector")
        self.registerField("usb_serial", self.usb_serial, "currentText")
        self.adc_label = QtWidgets.QLabel()
        self.adc_label.setText("ADC pin")
        self.adc_voltage_divider = QtWidgets.QComboBox()
        self.adc_voltage_divider.addItems(['1.0V','3.0V', '3V3', '4.5V', '5V', '6V', '9V', '12V', '24V'])
        self.onewire_label = QtWidgets.QLabel()
        self.onewire_label.setText("Onewire")
        self.peripherals["DS18B20"] = QtWidgets.QCheckBox("DS18B20")
        self.registerField("DS18B20", self.peripherals["DS18B20"])
        self.peripherals["DS18B20U"] = QtWidgets.QCheckBox("DS18B20U")
        self.registerField("DS18B20U", self.peripherals["DS18B20U"])
        self.spi_label = QtWidgets.QLabel()
        self.spi_label.setText("SPI")
        self.i2c_label = QtWidgets.QLabel()
        self.i2c_label.setText("I2C")
        self.peripherals["ina219"] = QtWidgets.QCheckBox("INA219")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.serial_label)
        layout.addWidget(self.usb_serial)
        layout.addWidget(self.adc_label)
        layout.addWidget(self.adc_voltage_divider)
        layout.addWidget(self.onewire_label)
        layout.addWidget(self.peripherals["DS18B20"])
        layout.addWidget(self.peripherals["DS18B20U"])
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
            'Wemos D1 Mini': 'RF_Module:WEMOS_D1_mini_light'
        }

        battery_footprints = {
            'No battery': '',
            '2x1.5V AA - Keystone 2462':'Battery:BatteryHolder_Keystone_2462_2xAA',
            '2x1.5V AAA - Keystone 2468': 'BatteryHolder_Keystone_2468_2xAAA',
            '3.7V Li-ion 18650 battery holder': 'BatteryHolder_Keystone_1042_1x18650'
        }

        resistor_footprints = {
            'SMD 0402': 'Resistor_SMD:R_0402_1005Metric',
            'SMD 0603': 'Resistor_SMD:R_0603_1608Metric',
            'SMD 0805': 'Resistor_SMD:R_0805_2012Metric',
            'SMD 1206': 'Resistor_SMD:R_1206_3216Metric',
            'SMD 1210': 'Resistor_SMD:R_1210_3225Metric'
        }

        usb_connector_footprints = {
            'USB B': 'USB_B_OST_USB-B1HSxx_Horizontal',
            'USB B Micro': 'USB_Micro-B_Amphenol_10103594-0001LF_Horizontal',
            'USB B Mini': 'USB_Mini-B_Lumberg_2486_01_Horizontal'
        }

        f = open(self.field('filename'), "w")
        variables = {
            'mcu': self.field("mcu"),
            'mcu_footprint': footprints[self.field("mcu")],
            'mcurail': self.field('mcurail'),
            'powersource': battery_footprints[self.field('powersource')],
            'resistor_footprint': resistor_footprints[self.field('resistor_footprint')]
            }

        code = generate(variables, self)

        f.write(code)
        f.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wizard = Skimibowi()
    wizard.show()
    sys.exit(app.exec_())
