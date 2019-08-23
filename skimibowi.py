#!/usr/bin/env python

# <one line to give the program's name and a brief idea of what it does.>
#    Copyright (C) <year>  <name of author>
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
from PyQt5 import QtCore, QtWidgets

class QIComboBox(QtWidgets.QComboBox):
    def __init__(self,parent=None):
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
        self.currentIdChanged.connect(self.idchanged)
        self.resize(640,480)

    def idchanged(self,i):
        titles = ""
        for i in self.pageIds():
            pagename = self.page(i).title()
            if i == self.currentId():
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
        self.powersource.addItem("2xAA - Keystone 2462")
        self.powersource.addItem("2x1.5V AAA battery holder")
        self.powersource.addItem("2x1.5V AAAA battery holder")
        self.powersource.addItem("3.7V Li-ion 18650 battery holder")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.powersource)
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
        self.label2 = QtWidgets.QLabel()
        self.bus3v3 = QtWidgets.QCheckBox("+3.3V")
        self.bus5v = QtWidgets.QCheckBox("+5V") 
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.componentType)
        layout.addWidget(self.label2)
        layout.addWidget(self.bus3v3)
        layout.addWidget(self.bus5v)
        self.setLayout(layout)

    def initializePage(self):
        self.label1.setText("Capasitor, resistor and diode form factor")
        self.label2.setText("Bus voltage")

class PeripheralsPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(PeripheralsPage, self).__init__(parent)
        self.setTitle("Peripherals")
        self.peripherals = {}
        self.onewire_label = QtWidgets.QLabel()
        self.onewire_label.setText("Onewire")
        self.peripherals["18b20"] = QtWidgets.QCheckBox("18b20")
        self.registerField("18b20", self.peripherals["18b20"])
        self.spi_label = QtWidgets.QLabel()
        self.spi_label.setText("SPI")
        self.i2c_label = QtWidgets.QLabel()
        self.i2c_label.setText("I2C")
        self.peripherals["ina219"] = QtWidgets.QCheckBox("INA219")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.onewire_label)
        layout.addWidget(self.peripherals["18b20"])
        layout.addWidget(self.spi_label)
        layout.addWidget(self.i2c_label)
        layout.addWidget(self.peripherals["ina219"])
        self.setLayout(layout)

class FinalPage(QtWidgets.QWizardPage): 
    def __init__(self, parent=None):
        super(FinalPage, self).__init__(parent)
        self.setTitle("Generate netlist")
        self.filename = QtWidgets.QLineEdit();
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
            '2xAA - Keystone 2462':'Battery:BatteryHolder_Keystone_2462_2xAA'
        }

        f = open(self.field('filename'), "w")
        variables = {
            'mcu': self.field("mcu"),
            'mcu_footprint': footprints[self.field("mcu")],
            'mcurail': self.field('mcurail'),
            'powersource': battery_footprints[self.field('powersource')]
            }
        
        code = '''
#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Bus, Part, Net, generate_netlist

U1 = Part('RF_Module', '{mcu}', footprint='{mcu_footprint}')

NETS = {{}}
NETS['+VBatt'] = Net('+VBatt')
NETS['+VBus'] = Net('+VBus')
NETS['+3V'] = Net('+3V')
NETS['+3V3'] = Net('+3V3')
NETS['+5V'] = Net('+5V')
NETS['GND'] = Net('GND')

U1['VCC'] += NETS['{mcurail}']
U1['GND'] += NETS['GND']
U1['EN'] += NETS['{mcurail}']
U1['GPIO15'] += NETS['GND']

BATTERY = Part('Device', 'Battery', footprint='{powersource}')
BATTERY['+'] += NETS['+VBatt']
BATTERY['-'] += NETS['GND']

'''.format(**variables)

        if self.field('reset') == True:
            code += '''
NETS['RST'] = Net('RST')
U1['RST'] += NETS['RST']
U1['GPIO16'] += NETS['RST']
'''

        if self.field('Reset button') == True:
            code += '''
SW1 = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
SW1[1] += NETS['RST']
SW1[2] += NETS['GND']
'''

        if self.field('Flash button') == True:
            code += '''
SW2 = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
SW2[1] += NETS['GPIO15']
SW2[2] += NETS['GND']
'''

        if self.field('18b20') == True:
            code += '''
NETS['VDD'] = Net('VDD')
NETS['VDD'] += NETS['+VBatt']
ONEWIRE = Bus('onewire', NETS['VDD'], NETS['GND'], Net('DQ'))
U1['GPIO2'] += ONEWIRE['DQ']

U2 = Part('Sensor_Temperature', 'DS18B20', footprint="Package_TO_SOT_THT:TO-92_Inline")
U2['VDD'] += ONEWIRE['VDD']
U2['GND'] += ONEWIRE['GND']
U2['DQ'] += ONEWIRE['DQ']
'''.format(**variables)

        code += '''
generate_netlist()

'''

        f.write(code)
        f.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wizard = Skimibowi()
    wizard.show()
    sys.exit(app.exec_())