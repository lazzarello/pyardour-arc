#! /usr/bin/env python3
# Interpret messages to/from a Monome Arc to Ardour's OSC control surface API
# message reference as documentation at 
# https://manual.ardour.org/using-control-surfaces/controlling-ardour-with-osc/osc-control/
# SSID is an integer starting at 1 from the order in the Strips list
import asyncio
import monome

ARDOUR_PORT = 3819
ARDOUR_HOST = 'localhost'
ARDOUR_FEEDBACK_PORT = 3820
ARDOUR_FADER_MIN_DB = -193
ARDOUR_FADER_MAX_DB = 6

class Ardour:
    def __init__(self, host: str, port: int, fb_port: int):
        self._host = host
        self._port = port
        self._conn = None
        self._fb_port = fb_port

    def on_db_delta(self, strip: int, db: float):
        # ardour strips are 1 indexed, arc is 0
        strip =+ 1
        # generate this message string
        osc_message = f'/strip/db_delta i {strip} f {db}'
        print(osc_message)

class ArdourArcApp(monome.ArcApp):
    def __init__(self):
        super().__init__()
        self.pos = [0, 0, 0, 0]
        self.ardour = Ardour(ARDOUR_HOST, ARDOUR_PORT, ARDOUR_FEEDBACK_PORT)

    def on_arc_ready(self):
        print('Ready, clearing all rings...')
        for n in range(0, 4):
            self.arc.ring_all(n, 0)

    def on_arc_disconnect(self):
        print('Arc disconnected.')

    def on_arc_delta(self, ring, delta):
        # print(f'Ring: {ring} Delta: {delta}')
        self.ardour.on_db_delta(ring, delta)

        old_pos = self.pos[ring]
        new_pos = old_pos + delta

        if new_pos > old_pos:
            self.arc.ring_range(ring, old_pos, new_pos, 15)
        else:
            self.arc.ring_range(ring, new_pos, old_pos, 0)

        self.pos[ring] = new_pos

async def main():
    loop = asyncio.get_running_loop()
    app = ArdourArcApp()

    def serialosc_device_added(id, type, port):
        if 'arc' not in type:
            print(f'ignoring {id} ({type}) as device does not appear to be an arc')
            return

        print(f'connecting to {id} ({type})')
        asyncio.ensure_future(app.arc.connect('127.0.0.1', port))

    serialosc = monome.SerialOsc()
    serialosc.device_added_event.add_handler(serialosc_device_added)

    await serialosc.connect()
    await loop.create_future()

if __name__ == '__main__':
    asyncio.run(main())
