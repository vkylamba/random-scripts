import random
import datetime
import requests
import time

import pickle


class Device(object):
    """
            Class representing a physycal device.
            To mimic physical device and send data.
    """

    device_type = "E-Meter"
    server_url = "https://demo.thingsboard.io/"
    data_path = "api/v1/{}/telemetry"
    time_delta = datetime.timedelta(minutes=10)

    def __init__(self, device_type=None, token=None):

        if device_type:
            self.device_type = device_type
        if token:
            self.token = token

    def generate_data_point(self):
        """
            Method to generate a fake dat point.
        """

        data = getattr(self, 'data', {})
        energy = data.get('energy', 0)
        pv_energy = data.get('pv_energy', 0)
        runtime = data.get('runtime', 0)

        time_now = datetime.datetime.now()

        if self.device_type == "E-Meter":
            voltage = random.randrange(2200, 2400)
            current = random.randrange(0, 1000)
            power = voltage * current
            energy += (power * self.time_delta.total_seconds()) / 3600000
            runtime += self.time_delta.total_seconds()
            state = random.randrange(0, 4)

        elif self.device_type == "Solar":
            voltage = random.randrange(90, 140)
            current = random.randrange(0, 500)
            power = voltage * current
            energy += (power * self.time_delta.total_seconds()) / 3600000
            runtime += self.time_delta.total_seconds()
            state = random.randrange(0, 4)

            if time_now.hour > 6 and time_now.hour < 19:
                pv_voltage = random.randrange(90, 200) - 0.5 * abs(time_now.hour - 12)
                pv_current = pv_voltage * 3
            else:
                pv_voltage = random.randrange(0, 5)
                pv_current = 0
            pv_power = pv_voltage * pv_current
            pv_energy += (pv_power * self.time_delta.total_seconds()) / 3600000
            temperature = random.randrange(10, 45)

        self.data = {
            'voltage': int(voltage),
            'current': int(current),
            'power': int(power),
            'energy': int(energy),
            'runtime': int(runtime),
            'state': int(state)
        }
        if self.device_type == 'Solar':
            self.data['pv_voltage'] = int(pv_voltage)
            self.data['pv_current'] = int(pv_current)
            self.data['pv_power'] = int(pv_power)
            self.data['pv_energy'] = int(pv_energy)
            self.data['temperature'] = int(temperature)

        return self.data

    def send_data(self):
        data = getattr(self, 'data', None)
        if not data:
            data = str(self.generate_data_point()).replace("'", '"')

        print("Posting data {} to url {}".format(self.server_url + self.data_path.format(self.token), data))
        resp = requests.request("POST", "https://demo.thingsboard.io/api/v1/sRrJc8OnMiCAXSF01Fjo/telemetry", data=data, headers={
            "content-type": "application/json"
        })
        self.data = {}

        print(resp.status_code)
        if resp.status_code in [200, 201]:
            return True
        else:
            return resp.text


if __name__ == '__main__':

    try:
        dev = pickle.load( open( "dev_thingsboard.p", "rb" ) )

    except Exception as e:
        print(e)
        dev = Device(device_type="Solar", token='sRrJc8OnMiCAXSF01Fjo')

    dev.send_data()
    
    pickle.dump(dev, open( "dev_thingsboard.p", "wb" ) )
    # dev1 = Device(token='add4d09c752af1ccdfd02091baf66e70318ce9c3')
    
    # dev.send()
    # dev1.send()
    # for i in range(0, 100):
    #    dev.send_data()
    #    # dev1.send_data()
    #    time.sleep(595)
