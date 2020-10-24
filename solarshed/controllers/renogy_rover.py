"""
Driver for the Renogy Rover Solar Controller using the Modbus RTU protocol
"""

import minimalmodbus

BATTERY_TYPE = {
    1: 'open',
    2: 'sealed',
    3: 'gel',
    4: 'lithium',
    5: 'self-customized'
}

CHARGING_STATE = {
    0: 'deactivated',
    1: 'activated',
    2: 'mppt',
    3: 'equalizing',
    4: 'boost',
    5: 'floating',
    6: 'current limiting'
}

class RenogyRover(minimalmodbus.Instrument):
    """
    Communicates using the Modbus RTU protocol (via provided USB<->RS232 cable)
    """

    def __init__(self, portname, slaveaddress, baudrate=9600, timeout=0.5):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.serial.baudrate = baudrate
        self.serial.timeout = timeout

    def model(self):
        """
        Read the controller's model information
        """
        return self.read_string(12, numberOfRegisters=8)

    def system_voltage_current(self):
        """
        Read the controler's system voltage and current
        Returns a tuple of (voltage, current)
        """
        register = self.read_register(10)
        amps = register & 0x00ff
        voltage = register >> 8
        return (voltage, amps)

    def version(self):
        """
        Read the controler's software and hardware version information
        Returns a tuple of (software version, hardware version)
        """
        registers = self.read_registers(20, 4)
        soft_major = registers[0] & 0x00ff
        soft_minor = registers[1] >> 8
        soft_patch = registers[1] & 0x00ff
        hard_major = registers[2] & 0x00ff
        hard_minor = registers[3] >> 8
        hard_patch = registers[3] & 0x00ff
        software_version = 'V{}.{}.{}'.format(soft_major, soft_minor, soft_patch)
        hardware_version = 'V{}.{}.{}'.format(hard_major, hard_minor, hard_patch)
        return (software_version, hardware_version)

    def serial_number(self):
        """
        Read the controller's serial number
        """
        registers = self.read_registers(24, 2)
        return '{}{}'.format(registers[0], registers[1])

    def battery_percentage(self):
        """
        Read the battery percentage
        """
        return self.read_register(256) & 0x00ff

    def battery_voltage(self):
        """
        Read the battery voltage
        """
        return self.read_register(257, numberOfDecimals=1)

    def battery_temperature(self):
        """
        Read the battery surface temperature
        """
        register = self.read_register(259)
        battery_temp_bits = register & 0x00ff
        temp_value = battery_temp_bits & 0x0ff
        sign = battery_temp_bits >> 7
        battery_temp = -(temp_value - 128) if sign == 1 else temp_value
        return battery_temp


    def controller_temperature(self):
        """
        Read the controller temperature
        """
        register = self.read_register(259)
        controller_temp_bits = register >> 8
        temp_value = controller_temp_bits & 0x0ff
        sign = controller_temp_bits >> 7
        controller_temp = -(temp_value - 128) if sign == 1 else temp_value
        return controller_temp

    def load_voltage(self):
        """
        Read load (raspberrypi) voltage
        """
        return self.read_register(260, numberOfDecimals=1)

    def load_current(self):
        """
        Read load (raspberrypi) current
        """
        return self.read_register(261, numberOfDecimals=2)

    def load_power(self):
        """
        Read load (raspberrypi) power
        """
        return self.read_register(262)

    def solar_voltage(self):
        """
        Read solar voltage
        """
        return self.read_register(263, numberOfDecimals=1)

    def solar_current(self):
        """
        Read solar current
        """
        return self.read_register(264, numberOfDecimals=2)

    def solar_power(self):
        """
        Read solar power
        """
        return self.read_register(265)

    def charging_amp_hours_today(self):
        """
        Read charging amp hours for the current day
        """
        return self.read_register(273)

    def discharging_amp_hours_today(self):
        """
        Read discharging amp hours for the current day
        """
        return self.read_register(274)

    def power_generation_today(self):
        return self.read_register(275)

    def charging_status(self):
        return self.read_register(288) & 0x00ff

    def charging_status_label(self):
        return CHARGING_STATE.get(self.charging_status())

    def battery_capacity(self):
        return self.read_register(57346)

    def voltage_setting(self):
        register = self.read_register(57347)
        setting = register >> 8
        recognized_voltage = register & 0x00ff
        return (setting, recognized_voltage)

    def battery_type(self):
        register = self.read_register(57348)
        return BATTERY_TYPE.get(register)

    #TODO: resume at 3.10 of spec

if __name__ == "__main__":
    rover = RenogyRover('/dev/ttyUSB0', 1)
    print('Model: ', rover.model())
    print('Battery %: ', rover.battery_percentage())
    print('Battery Type: ', rover.battery_type())
    print('Battery Capacity: ', rover.battery_capacity())
    print('Battery Voltage: ', rover.battery_voltage())
    battery_temp = rover.battery_temperature()
    print('Battery Temperature: ', battery_temp, battery_temp * 1.8 + 32)
    controller_temp = rover.controller_temperature()
    print('Controller Temperature: ', controller_temp, controller_temp * 1.8 + 32)
    print('Load Voltage: ', rover.load_voltage())
    print('Load Current: ', rover.load_current())
    print('Load Power: ', rover.load_power())
    print('Charging Status: ', rover.charging_status_label())
    print('Solar Voltage: ', rover.solar_voltage())
    print('Solar Current: ', rover.solar_current())
    print('Solar Power: ', rover.solar_power())
    print('Power Generated Today (kilowatt hours): ', rover.power_generation_today())
    print('Charging Amp/Hours Today: ', rover.charging_amp_hours_today())
    print('Discharging Amp/Hours Today: ', rover.discharging_amp_hours_today())
