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

"""Controller for Skimibowi. Acts between UI and code generator, maps component selections to footprints"""

from yaml import load, dump, Loader
from generator import generate

footprints = {
    'ESP-07': 'RF_Module:ESP-07',
    'ESP-12E': 'RF_Module:ESP-12E',
    'Wemos D1 Mini': 'RF_Module:WEMOS_D1_mini_light',
    'ATtiny85-20PU': 'Package_DIP:DIP-8_W7.62mm',
    'ATtiny85-20SU': 'Package_SO:SOIJ-8_5.3x5.3mm_P1.27mm',
    'ATtiny85-20MU': 'Package_DFN_QFN:QFN-20-1EP_4x4mm_P0.5mm_EP2.6x2.6mm',
    'ATmega328P-PU': 'Package_DIP:DIP-28_W7.62mm',
    'ATmega328P-AU': 'Package_QFP:TQFP-32_7x7mm_P0.8mm',
    'ATmega328P-MU': 'Package_DFN_QFN:QFN-32-1EP_5x5mm_P0.5mm_EP3.1x3.1mm',
    'No MCU': ''
}

battery_footprints = {
    'No battery': '',
    '2xAA - Keystone 2462':'Battery:BatteryHolder_Keystone_2462_2xAA',
    '3xAA - TruPower BH-331P':'BatteryHolder_TruPower_BH-331P_3xAA',
    '2xAAA - Keystone 2468': 'Battery:BatteryHolder_Keystone_2468_2xAAA',
    '3xAAA - Keystone 2479': 'Battery:BatteryHolder_Keystone_2479_3xAAA',
    '18650 - Keystone 1042': 'Battery:BatteryHolder_Keystone_1042_1x18650',
    'JST PH S2B': 'JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal',
    'Barrel Jack 2.0/5.5mm': 'Connector_BarrelJack:BarrelJack_CUI_PJ-063AH_Horizontal'
}

regulators = {
    'No regulator': None,
    'LD1117S33TR': {'module': 'Regulator_Linear', 'part': 'LD1117S33TR_SOT223', 'footprint': 'Package_TO_SOT_SMD:SOT-223-3_TabPin2', 'output': '+3V3'},
    'LD1117S50TR': {'module': 'Regulator_Linear', 'part': 'LD1117S50TR_SOT223', 'footprint': 'Package_TO_SOT_SMD:SOT-223-3_TabPin2', 'output': '+5V'},
    'LP2985-30': {'module': 'Regulator_Linear', 'part': 'LP2985-3.0', 'footprint': 'Package_TO_SOT_SMD:SOT-23-5', 'output': '+3V'},
    'LP2985-33': {'module': 'Regulator_Linear', 'part': 'LP2985-3.3', 'footprint': 'Package_TO_SOT_SMD:SOT-23-5', 'output': '+3V3'},
    'LP2985-50': {'module': 'Regulator_Linear', 'part': 'LP2985-5.0', 'footprint': 'Package_TO_SOT_SMD:SOT-23-5', 'output': '+5V'},
    'AP2112K-3.0': {'module': 'Regulator_Linear', 'part': 'AP2112K-3.0', 'footprint': 'Package_TO_SOT_SMD:SOT-23-5', 'output': '+3V', 'enable_pin': True},
    'AP2112K-3.3': {'module': 'Regulator_Linear', 'part': 'AP2112K-3.3', 'footprint': 'Package_TO_SOT_SMD:SOT-23-5', 'output': '+3V3', 'enable_pin': True},
    'AP2112K-5.0': {'module': 'Regulator_Linear', 'part': 'AP2112K-5.0', 'footprint': 'Package_TO_SOT_SMD:SOT-23-5', 'output': '+5V', 'enable_pin': True}
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
    'No USB connector': None,
    'USB B': {'part': 'USB_B', 'footprint': 'USB_B_OST_USB-B1HSxx_Horizontal'},
    'USB B Mini': {'part': 'USB_B_Mini', 'footprint': 'USB_Mini-B_Lumberg_2486_01_Horizontal'},
    'USB B Micro': {'part': 'USB_B_Micro', 'footprint': 'USB_Micro-B_Amphenol_10103594-0001LF_Horizontal'},
    'USB A PCB Trace': {'part': 'USB_A', 'footprint': 'skimibowi:usb'},
}

onewire_connector_footprints = {
    'No Onewire connector': '',
    '1x3 Pin Header': 'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical',
    'Screw terminal': 'TerminalBlock_TE-Connectivity:TerminalBlock_TE_282834-3_1x03_P2.54mm_Horizontal'
}

fuse_footprints = {
    'No fuse': None,
    'Schurter 0031.8201 5x20mm holder': 'Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open',
    'SMD 1812':'Fuse_1812_4532Metric'
}

def fill_variables(wizard):
    """Fill circuit configuration based on selections made in wizard UI"""
    return {
        'mcu': wizard.field("mcu"),
        'mcu_footprint': footprints[wizard.field("mcu")],
        'icsp': wizard.field('icsp'),
        'mcurail': wizard.field('mcurail'),
        'powersource': wizard.field('powersource'),
        'powersource_footprint': battery_footprints[wizard.field('powersource')],
        'battery_management': wizard.field('battery_management'),
        'fuse': wizard.field('fuse'),
        'fuse_footprint': fuse_footprints[wizard.field('fuse')],
        'switch': wizard.field('switch'),
        'reset': wizard.field('reset'),
        'Reset button': wizard.field('Reset button'),
        'Flash button': wizard.field('Flash button'),
        'led': wizard.field('led'),
        'FTDI header': wizard.field('FTDI header'),
        'usb_connector': wizard.field('usb_connector'),
        'ina219': wizard.field('ina219'),
        'DS18B20': wizard.field('DS18B20'),
        'DS18B20U': wizard.field('DS18B20U'),
        'usb_uart': wizard.field('usb_uart'),
        'board_footprint': wizard.field('board_footprint'),
        'onewire_connector': wizard.field('onewire_connector'),
        'common_footprint': wizard.field('common_footprint'),
        'transistor_footprint': wizard.field('transistor_footprint'),
        'resistor_footprint': resistor_footprints[wizard.field('common_footprint')],
        'capacitor_footprint': capacitor_footprints[wizard.field('common_footprint')],
        'led_footprint': led_footprints[wizard.field('common_footprint')],
        'regulator': wizard.field('regulator'),
        'regulator_data': regulators[wizard.field('regulator')],
        'usb_connector_footprint': usb_connector_footprints[wizard.field('usb_connector')],
        'onewire_connector_footprint': onewire_connector_footprints[wizard.field('onewire_connector')],
        'autoselect': wizard.field('autoselect')
        }

def generate_skidl(wizard):
    """Generate SKiDL code based on chosen wizard options and save those settings to settings.yml
    where they are read when the wizard started next time"""
    with open("settings.yml", 'w') as settings:
        settings.write(dump(fill_variables(wizard)))

    code = generate(fill_variables(wizard))

    with open(wizard.field('filename'), 'w') as file:
        file.write(code)

def load_settings(wizard, settings_filename="settings.yml"):
    """Load chosen wizard settings from the previous time SKiDL code was generated with wizard"""
    try:
        with open(settings_filename, 'r') as settings_file:
            settings = load(settings_file, Loader=Loader)

            if settings:
                for field in ['mcu', 'mcurail', 'icsp', 'powersource', 'battery_management', 'fuse',
                            'switch', 'reset', 'Flash button', 'Reset button', 'led', 'FTDI header', 'usb_connector', 'ina219',
                            'DS18B20', 'DS18B20U', 'usb_uart', 'common_footprint', 'transistor_footprint', 'board_footprint',
                            'regulator', 'onewire_connector', 'autoselect']:
                    if field in settings:
                        wizard.setField(field, settings[field])
    except:
        None

def generate_from_settings(filename, settings_filename="settings.yml"):
    with open(settings_filename, 'r') as settings_file:
        settings = load(settings_file, Loader=Loader)
        code = generate(settings)
        with open(filename, 'w') as file:
            file.write(code)
