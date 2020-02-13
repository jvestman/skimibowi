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

"""Generates passive component footprints to SKiDL programs"""


def generate_r(args):
    """Generate default resistor footprint"""
    return f"""
def R(value):
    \"\"\"Creates default resistor footprint\"\"\"
    return Part('Device', 'R', value=value, footprint='{args['resistor_footprint']}')
"""


def generate_c(args):
    """Generate default capacitor footprint"""
    return f"""
def C(value):
    \"\"\"Creates default capacitor footprint\"\"\"
    return Part('Device', 'C', value=value, footprint='{args['capacitor_footprint']}')
"""


def generate_l(args):
    """Generate default inductor footprint"""
    return f"""
def L(value):
    \"\"\"Creates default resistor footprint\"\"\"
    return Part('Device', 'L', value=value, footprint='{args['resistor_footprint']}')
"""

def generate_device(args):
    """Generate part lookup function"""
    return f"""
def Device(library, name):
    \"\"\"Make part lookup and return the part with footprint set\"\"\"
    footprint = show(library, name).F2
    return Part(library, name, value=name, footprint=footprint)
"""

def generate_d(args):
    """Generate part lookup function"""
    return f"""
def D(name):
    \"\"\"Creates diode\"\"\"
    footprint = show('diode', name).F2
    return Device('Diode', name)
"""