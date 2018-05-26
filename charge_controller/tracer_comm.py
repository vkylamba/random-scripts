#!/usr/bin/env python
import minimalmodbus
import sys
import serial

ADDRESS_PV_VOLTAGE = 0x3100
ADDRESS_PV_CURRENT = 0x3101
ADDRESS_PV_POWER_L = 0x3102
ADDRESS_PV_POWER_H = 0x3103

ADDRESS_BATT_VOLTAGE = 0x3104
ADDRESS_BATT_CURRENT = 0x3105
ADDRESS_BATT_POWER_L = 0x3106
ADDRESS_BATT_POWER_H = 0x3107

ADDRESS_LOAD_VOLTAGE = 0x310c
ADDRESS_LOAD_CURRENT = 0x310d
ADDRESS_LOAD_POWER_L = 0x310e
ADDRESS_LOAD_POWER_H = 0x310f

ADDRESS_BATT_TEMP = 0x3110
ADDRESS_BATT_SOC = 0x311A

ADDRESS_BATT_STATUS = 0x3200

ADDRESS_ENERGY_GENERATED = 0x330C
ADDRESS_ENERGY_CONSUMED = 0x3304

ADDRESS_CALIBRATION_PV1 = 0x4000
ADDRESS_CALIBRATION_PV2 = 0x4001
ADDRESS_CALIBRATION_PV3 = 0x4002
ADDRESS_CALIBRATION_BV1 = 0x4003
ADDRESS_CALIBRATION_BV2 = 0x4004
ADDRESS_CALIBRATION_BV3 = 0x4005
ADDRESS_CALIBRATION_CC1 = 0x4006
ADDRESS_CALIBRATION_CC2 = 0x4007
ADDRESS_CALIBRATION_CC3 = 0x4008
ADDRESS_CALIBRATION_LC1 = 0x4009
ADDRESS_CALIBRATION_LC2 = 0x400a
ADDRESS_CALIBRATION_LC3 = 0x400b

DUSK_TIMER_ADDRESS = 0x903e
LENGTH_OF_NIGHT_ADDRESS = 0x9065
DAWN_TIMER_ADDRESS = 0x903f


def battery_type(set_it=0, new_val=0):
    address = 0x9000
    length = 1
    return handle_int(address, length, set_it, new_val)


def night_time_threshold_voltage(set_it=0, new_val=0):
    address = 0x901e
    length = 1
    return handle_int(address, length, set_it, new_val)


def load_control_mode(set_it=0, new_val=0):
    address = 0x903d
    length = 1
    return handle_int(address, length, set_it, new_val)


def handle_int(address, length=1, set_it=0, new_val=0):
    try:
        if set_it != 0:
            # Registernumber, value, number of decimals for storage
            value = instrument.write_register(address, new_val)
        else:

            value = instrument.read_register(address)  # Registernumber, number of decimals
        # print value
    except Exception as e:
        print str(e)
        value = None
        pass
    return value


def handle_time(address, length=1, set_it=0, new_val=0):
    # The 16 bit register has high 8 bits as houre and low 8 bits as minutes
    try:
        if set_it != 0:
            # Convert the new value in the 16 bit register value
            tmp_list = new_val.split(':')
            hours = int(tmp_list[0])
            minutes = int(tmp_list[1])
            # print "hours: " + str(hours);
            # print "minutes: " + str(minutes);
            new_val = ((hours << 8) | minutes)
            # print "Val: " + str(new_val);
            # Registernumber, value, number of decimals for storage
            value = instrument.write_register(address, new_val)
        else:
            value = int(instrument.read_register(address))  # Registernumber, number of decimals
            # print "Val: " + str(value);
            # Convert it into hours
            hours = value >> 8
            minutes = value & 0xff
            value = str(hours) + ':' + str(minutes)
        # print value
    except Exception as e:
        print str(e)
        value = None
        pass
    return value


def timer_1(set_it=0, new_val=0):
    return handle_time(DUSK_TIMER_ADDRESS, 1, set_it, new_val)


def timer_2(set_it=0, new_val=0):
    return handle_time(DAWN_TIMER_ADDRESS, 1, set_it, new_val)


def night_length(set_it=0, new_val=0):
    return handle_time(LENGTH_OF_NIGHT_ADDRESS, 1, set_it, new_val)


def load_control(set_it=0, new_val=0):
    return handle_int(0x9076, set_it, new_val)


def cal_pv1(set_it=0, new_val=0):
    return handle_int(ADDRESS_CALIBRATION_PV1, 1, set_it, new_val)


def cal_pv2(set_it=0, new_val=0):
    return handle_int(ADDRESS_CALIBRATION_PV2, 1, set_it, new_val)


def cal_pv3(set_it=0, new_val=0):
    return handle_int(ADDRESS_CALIBRATION_PV3, 1, set_it, new_val)


def cal_bv1(set_it=0, new_val=0):
    return handle_int(ADDRESS_CALIBRATION_BV1, 1, set_it, new_val)


def cal_bv2(set_it=0, new_val=0):
    return handle_int(ADDRESS_CALIBRATION_BV2, 1, set_it, new_val)


def cal_bv3(set_it=0, new_val=0):
    return handle_int(ADDRESS_CALIBRATION_BV3, 1, set_it, new_val)


def cal_cc1(set_it=0, new_val=0):
    return handle_int(ADDRESS_CALIBRATION_CC1, 1, set_it, new_val)


def cal_cc2(set_it=0, new_val=0):
    return handle_int(ADDRESS_CALIBRATION_CC2, 1, set_it, new_val)


def cal_cc3(set_it=0, new_val=0):
    return handle_int(0x4008, 1, set_it, new_val)


def get_data(device_name, dev_id):
    instrument = minimalmodbus.Instrument(device_name, int(
        dev_id))  # port name, slave address (in decimal)
    instrument.serial.baudrate = 115200
    instrument.serial.databits = 8
    instrument.serial.parity = 'N'
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 1
    return instrument.read_registers(ADDRESS_PV_VOLTAGE, 8, functioncode=4)


if __name__ == '__main__':

    if(len(sys.argv) > 2):
        instrument = minimalmodbus.Instrument(sys.argv[1], int(
            sys.argv[2]))  # port name, slave address (in decimal)
        instrument.serial.baudrate = 115200
        instrument.serial.databits = 8
        instrument.serial.parity = 'N'
        instrument.serial.stopbits = 1
        instrument.serial.timeout = 1
        # instrument.debug = True;
        # instrument.mode = minimalmodbus.MODE_RTU  # rtu or ascii mode

        # ser = serial.Serial(sys.argv[1]);
    else:
        sys.exit('use: ' + sys.argv[0] + ' device_name dev_id')

    # print "Night time threshold voltage is: " + str(night_time_threshold_voltage());
    # print "Load control mode: " + str(load_control_mode());
    # print "Load control mode: " + str(load_control_mode(2,0));
    # print "Timer1: " + str(timer_1());
    # print "Timer2: " + str(timer_2());
    # print "Timer1: " + str(timer_1(1, '4:00'));
    # print "Timer2: " + str(timer_2(1, '1:10'));
    # print "Night length: " + str(night_length());
    # print "Night length: " + str(night_length(1, '12:00'));
    # print "Load status: " + str(load_control());
    # print "Load status: " + str(load_control(1,1));
    # print "Battery type: " + str(battery_type());
    # print "Battery type: " + str(battery_type(1,2));

    # print "CAL PV-1: " + str(cal_pv1(1, 0));
    # print "CAL PV-2: " + str(cal_pv2(1, 167));
    # print "CAL PV-3: " + str(cal_pv3(1, 229));

    # print "CAL BV-1: " + str(cal_bv1(1, 0));
    # print "CAL BV-2: " + str(cal_bv2(1, 105));
    # print "CAL BV-3: " + str(cal_bv3(1, 150));

    # print "CAL CC-3: " + str(cal_cc3(1, 2240));

    print "PV voltage: " + str(handle_int(ADDRESS_PV_VOLTAGE))
    print "Battery voltage: " + str(handle_int(ADDRESS_BATT_VOLTAGE))
    print "Charging current: " + str(handle_int(ADDRESS_PV_CURRENT))
    print "Discharging current: " + str(handle_int(ADDRESS_BATT_CURRENT))
    # print "Batery temperature: " + str(handle_int(ADDRESS_BATT_TEMP))

    # print "PV data: " + str(instrument.read_registers(ADDRESS_PV_VOLTAGE, 8, functioncode=4))
    # print "Load data: " + str(instrument.read_registers(ADDRESS_LOAD_VOLTAGE, 5))
    # print "Batt SOC: " + str(instrument.read_registers(ADDRESS_BATT_SOC, 1))
    # print "Energy Consumed: " + str(instrument.read_registers(ADDRESS_ENERGY_CONSUMED, 2))
    # print "Energy Generated: " + str(instrument.read_registers(ADDRESS_ENERGY_GENERATED, 2))
