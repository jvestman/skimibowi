"""Tests for SKiDL generator functions"""
import sys
from io import StringIO
import unittest
from unittest.mock import Mock
from generator import generate
from generator import generate_battery_management
from generator import generate_ftdi_header
from generator import generate_ftdi230

class TestGenerator(unittest.TestCase):
    """Tests for SKiDL generator functions"""
    def test_esp12e_basic(self):
        """Test basic generation case with ESP-12E"""
        wizard = Mock()
        wizard.field.return_value = False
        self.maxDiff = 10000
        self.assertEqual(
            generate({'mcu':'ESP-12E',
                      'mcu_footprint':'RF_Module:ESP-12E',
                      'mcurail':'+VBatt',
                      'powersource':'No battery',
                      'resistor_footprint': 'Resistor_SMD:R_1206_3216Metric',
                      'led_footprint': 'LED_1206_3216Metric',
                      'usb_connector_footprint':'USB_Micro-B_Amphenol_10103594-0001LF_Horizontal'}, wizard),
            '''
#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Bus, Part, Net, generate_netlist

U1 = Part('RF_Module', 'ESP-12E', footprint='RF_Module:ESP-12E')

NETS = {}
NETS['+VLipo'] = Net('+VLipo')
NETS['+VBatt'] = Net('+VBatt')
NETS['+VBus'] = Net('+VBus')
NETS['+3V'] = Net('+3V')
NETS['+3V3'] = Net('+3V3')
NETS['+5V'] = Net('+5V')
NETS['GND'] = Net('GND')

U1['VCC'] += NETS['+VBatt']
U1['GND'] += NETS['GND']
U1R1 = Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_1206_3216Metric')
U1R2 = Part('Device', 'R', value='4k7', footprint='Resistor_SMD:R_1206_3216Metric')
NETS['+VBatt'] & U1R1 & U1['EN']
NETS['GND'] & U1R2 & U1['GPIO15']

USBMICRO = Part('Connector', 'USB_B_Micro', footprint='USB_Micro-B_Amphenol_10103594-0001LF_Horizontal')
USBMICRO['VBUS'] += NETS['+VBus']
USBMICRO['GND'] += NETS['GND']

generate_netlist()
'''
        )
    def test_esp12e_all_options(self):
        """Test ESP-12E with reset line, reset button and 18b20"""
        self.maxDiff = 10000
        wizard = Mock()
        wizard.field.return_value = True
        self.assertEqual(
            generate({'mcu':'ESP-12E',
                      'mcu_footprint':'RF_Module:ESP-12E',
                      'mcurail':'+VBatt',
                      'powersource':'No battery',
                      'resistor_footprint':'Resistor_SMD:R_1206_3216Metric',
                      'led_footprint': 'LED_1206_3216Metric',
                      'usb_connector_footprint':'USB_Micro-B_Amphenol_10103594-0001LF_Horizontal'}, wizard),
            '''
#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Bus, Part, Net, generate_netlist

U1 = Part('RF_Module', 'ESP-12E', footprint='RF_Module:ESP-12E')

NETS = {}
NETS['+VLipo'] = Net('+VLipo')
NETS['+VBatt'] = Net('+VBatt')
NETS['+VBus'] = Net('+VBus')
NETS['+3V'] = Net('+3V')
NETS['+3V3'] = Net('+3V3')
NETS['+5V'] = Net('+5V')
NETS['GND'] = Net('GND')

U1['VCC'] += NETS['+VBatt']
U1['GND'] += NETS['GND']
U1R1 = Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_1206_3216Metric')
U1R2 = Part('Device', 'R', value='4k7', footprint='Resistor_SMD:R_1206_3216Metric')
NETS['+VBatt'] & U1R1 & U1['EN']
NETS['GND'] & U1R2 & U1['GPIO15']

NETS['RST'] = Net('RST')
U1['RST'] += NETS['RST']
U1['GPIO16'] += NETS['RST']

SW1 = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
SW1[1] += NETS['RST']
SW1[2] += NETS['GND']

SW2 = Part('Switch', 'SW_Push', footprint="Button_Switch_SMD:SW_SPST_B3U-1000P")
SW2[1] += U1['GPIO0']
SW2[2] += NETS['GND']

LED = Part('Device', 'LED', footprint='LED_1206_3216Metric')
LED_R = Part('Device', 'R', value='1k', footprint='Resistor_SMD:R_1206_3216Metric')
U1['GPIO0'] & LED_R & LED & NETS['+VBatt']

NETS['DQ'] = Net('DQ')

U3R1 = Part('Device', 'R', value='4k7', footprint='Resistor_SMD:R_1206_3216Metric')
U3R1[1] += NETS['+VBatt']
U3R1[2] += NETS['DQ']

U2 = Part('Sensor_Temperature', 'DS18B20', footprint="Package_TO_SOT_THT:TO-92_Inline")
U2['VDD'] += NETS['+VBatt']
U2['GND'] += NETS['GND']
U2['DQ'] += NETS['DQ']
U1['GPIO2'] += NETS['DQ']

U3 = Part('Sensor_Temperature', 'DS18B20U', footprint="Package_SO:MSOP-8_3x3mm_P0.65mm")
U3['VDD'] += NETS['+VBatt']
U3['GND'] += NETS['GND']
U3['DQ'] += NETS['DQ']
U1['GPIO2'] += NETS['DQ']

FTDI_HEADER = Part('Connector', 'Conn_01x06_Female', footprint='Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical')
FTDI_HEADER[1] += NETS['GND']
FTDI_HEADER[2] += NC
FTDI_HEADER[3] += NETS['+VBatt']
FTDI_HEADER[4] += U1['TX']
FTDI_HEADER[5] += U1['RX']
FTDI_HEADER[6] += NC

USBMICRO = Part('Connector', 'USB_B_Micro', footprint='USB_Micro-B_Amphenol_10103594-0001LF_Horizontal')
USBMICRO['VBUS'] += NETS['+VBus']
USBMICRO['GND'] += NETS['GND']

generate_netlist()
'''
        )

    def test_ftdi_header(self):
        """Test FTDI header generation"""
        self.maxDiff = 10000
        self.assertEqual(
            generate_ftdi_header({'mcurail':'VDD'}),
            '''
FTDI_HEADER = Part('Connector', 'Conn_01x06_Female', footprint='Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical')
FTDI_HEADER[1] += NETS['GND']
FTDI_HEADER[2] += NC
FTDI_HEADER[3] += NETS['VDD']
FTDI_HEADER[4] += U1['TX']
FTDI_HEADER[5] += U1['RX']
FTDI_HEADER[6] += NC
'''
            )

    def test_battery_management(self):
        """Test FTDI header generation"""
        self.maxDiff = 10000
        self.assertEqual(
            generate_battery_management({'resistor_footprint':'Resistor_SMD:R_1206_3216Metric',
                                         'led_footprint':'LED_SMD:LED_1206_3216Metric',
                                         'capacitor_footprint':'Capacitor_SMD:C_1206_3216Metric'}),
            '''
BATTERYMANAGER = Part('Battery_Management', 'MCP73871-2AA', footprint='Package_DFN_QFN:QFN-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm')
BATTERYMANAGER['IN'] += NETS['+VBus']
BATTERYMANAGER['SEL'] += NETS['+VBus']
BATTERYMANAGER['PROG2'] += NETS['+VBus']
BATTERYMANAGER['TE'] += NETS['+VBus']
BATTERYMANAGER['CE'] += NETS['+VBus']

BATTERYMANAGER['VSS'] += NETS['GND']

BATTERYMANAGER['OUT'] += NETS['+VBatt']

BATTERYMANAGER['VBAT'] += NETS['+VLipo']
BATTERYMANAGER['Vbat_SENSE'] += NETS['+VLipo']

RPROG1 = Part('Device', 'R', value='2k', footprint='Resistor_SMD:R_1206_3216Metric')
NETS['GND'] & RPROG1 & BATTERYMANAGER['PROG1']
RPROG2 = Part('Device', 'R', value='100k', footprint='Resistor_SMD:R_1206_3216Metric')
NETS['GND'] & RPROG2 & BATTERYMANAGER['PROG3']

BM_LED = Part('Device', 'LED', footprint='LED_SMD:LED_1206_3216Metric')
BM_LED_R = Part('Device', 'R', value='1k', footprint='Resistor_SMD:R_1206_3216Metric')
BATTERYMANAGER['STAT1'] & BM_LED_R & BM_LED & NETS['+VBus']

BM_LED2 = Part('Device', 'LED', footprint='LED_SMD:LED_1206_3216Metric')
BM_LED_R2 = Part('Device', 'R', value='1k', footprint='Resistor_SMD:R_1206_3216Metric')
BATTERYMANAGER['STAT2'] & BM_LED_R2 & BM_LED2 & NETS['+VBus']

BM_C = Part('Device', 'C', value='10uF', footprint='Capacitor_SMD:C_1206_3216Metric')
NETS['+VLipo'] & BM_C & NETS['GND']

BM_VPCC_R1 = Part('Device', 'R', value='100k', footprint='Resistor_SMD:R_1206_3216Metric')
BM_VPCC_R2 = Part('Device', 'R', value='270k', footprint='Resistor_SMD:R_1206_3216Metric')
NETS['GND'] & BM_VPCC_R1 & BM_VPCC_R2 & NETS['+VBus']
BATTERYMANAGER['VPCC'] += BM_VPCC_R2[1]

BM_THERM_R = Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_1206_3216Metric')
BATTERYMANAGER['THERM'] & BM_THERM_R & NETS['GND']
'''
            )

    def test_ftdi230(self):
        """Test generation of FTDI230"""
        self.maxDiff = 10000
        self.assertEqual(
            generate_ftdi230({'resistor_footprint':'Resistor_SMD:R_1206_3216Metric',
                              'mcurail':'+VBus'}),
            '''
FTDI230 = Part('Interface_USB', 'FT231XS', footprint="Package_SO:SSOP-20_3.9x8.7mm_P0.635mm")
FTDI230['VCC'] += NETS['+VBus']
FTDI230['GND'] += NETS['GND']
FTDI230['TXD'] += U1['RX']
FTDI230['RXD'] += U1['TX']
FTDI230['USBDM'] += USBMICRO['D-']
FTDI230['USBDP'] += USBMICRO['D+']

Q1 = Part('Transistor_BJT', 'PZT2222A', footprint='Package_TO_SOT_SMD:SOT-223')
Q2 = Part('Transistor_BJT', 'PZT2222A', footprint='Package_TO_SOT_SMD:SOT-223')
QR1 = Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_1206_3216Metric')
QR2 = Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_1206_3216Metric')
Q1['B'] += QR1[1]
QR1[2] += FTDI230['DTR']
Q2['B'] += QR2[1]
QR2[2] += FTDI230['RTS']
Q1['E'] += U1['GPIO0']
Q2['E'] += U1['RST']
Q1['C'] += Q2['C']
Q2['C'] += FTDI230['DTR']
Q1['C'] += FTDI230['RTS']
'''
            )

    def test_esp12e_all_options_execution(self):
        """Test execution of generated skidl code with all options true"""

        codeOut = StringIO()
        codeErr = StringIO()
        sys.stdout = codeOut
        sys.stderr = codeErr

        wizard = Mock()
        wizard.field.return_value = True

        exec(generate({'mcu':'ESP-12E',
                       'mcu_footprint':'RF_Module:ESP-12E',
                       'mcurail':'+3V3',
                       'powersource': '2xAAA - Keystone 2468',
                       'powersource_footprint':'BatteryHolder_Keystone_2468_2xAAA',
                       'resistor_footprint':'Resistor_SMD:R_1206_3216Metric',
                       'led_footprint': 'LED_1206_3216Metric',
                       'usb_connector_footprint':'USB_Micro-B_Amphenol_10103594-0001LF_Horizontal'}, wizard))

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        self.assertTrue(codeErr.getvalue().endswith('No errors or warnings found during netlist generation.\n\n'))
        self.assertEqual('', codeOut.getvalue())

        codeOut.close()
        codeErr.close()

    def test_generate_battery(self):
        """Test ESP-12E with Battery"""
        self.maxDiff = 10000
        wizard = Mock()
        wizard.field.return_value = False
        self.assertEqual(
            generate({'mcu':'ESP-12E',
                      'mcu_footprint':'RF_Module:ESP-12E',
                      'mcurail':'+VBatt',
                      'powersource': '2xAAA - Keystone 2468',
                      'powersource_footprint':'BatteryHolder_Keystone_2468_2xAAA',
                      'resistor_footprint':'Resistor_SMD:R_1206_3216Metric',
                      'led_footprint': 'LED_1206_3216Metric',
                      'usb_connector_footprint':'USB_Micro-B_Amphenol_10103594-0001LF_Horizontal'}, wizard),
            '''
#Generated by Swimibowi - SKiDL Microcontroller Board Wizard
"""Creates Kicad netlist file for a microcontroller board"""
from skidl import Bus, Part, Net, generate_netlist

U1 = Part('RF_Module', 'ESP-12E', footprint='RF_Module:ESP-12E')

NETS = {}
NETS['+VLipo'] = Net('+VLipo')
NETS['+VBatt'] = Net('+VBatt')
NETS['+VBus'] = Net('+VBus')
NETS['+3V'] = Net('+3V')
NETS['+3V3'] = Net('+3V3')
NETS['+5V'] = Net('+5V')
NETS['GND'] = Net('GND')

U1['VCC'] += NETS['+VBatt']
U1['GND'] += NETS['GND']
U1R1 = Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_1206_3216Metric')
U1R2 = Part('Device', 'R', value='4k7', footprint='Resistor_SMD:R_1206_3216Metric')
NETS['+VBatt'] & U1R1 & U1['EN']
NETS['GND'] & U1R2 & U1['GPIO15']

BATTERY = Part('Device', 'Battery', footprint='BatteryHolder_Keystone_2468_2xAAA')
BATTERY['+'] += NETS['+VBatt']
BATTERY['-'] += NETS['GND']

USBMICRO = Part('Connector', 'USB_B_Micro', footprint='USB_Micro-B_Amphenol_10103594-0001LF_Horizontal')
USBMICRO['VBUS'] += NETS['+VBus']
USBMICRO['GND'] += NETS['GND']

generate_netlist()
''')



if __name__ == '__main__':
    unittest.main()
