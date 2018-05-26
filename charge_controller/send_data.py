import tracer_comm as TC
import requests
import datetime

ACCESS_TOKEN = "673b27eed5e1ccc598265d25f4e525e5dce1d837"
API_URL = "http://okosengineering.com/device/datain?data={time},{numeric_ip},{energy},{runtime},{voltage},{current},{state}"
CHARGER_IP = 10
LOAD_IP = 9


def send_data(ip_address, energy, runtime, voltage, current, state):

    api = requests.get(API_URL.format(
        time=1,
        numeric_ip=ip_address,
        energy=energy,
        runtime=runtime,
        voltage=voltage,
        current=current,
        state=state
    ))

    if api.status_code == 200:
        print("Sent", api.text)
    else:
        print("Failed", api.text)


if __name__ == '__main__':
    # [159, 221, 30940, 0, 140, 221, 30940, 0]
    data = TC.get_data('/dev/ttyUSB0', 1)
    pv_voltage = data[0]
    charging_current = data[1]

    bat_voltage = data[4]
    discharging_current = data[5]

    send_data(CHARGER_IP, 0, 0, pv_voltage, charging_current, 0)
    send_data(LOAD_IP, 0, 0, bat_voltage, discharging_current, 0)
