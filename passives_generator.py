# MIT license
#
# Skimibowi - SKiDL Microcontroller Board Wizard
# Copyright (C) 2019  Jussi Vestman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
    return Device('Diode', name)
"""
