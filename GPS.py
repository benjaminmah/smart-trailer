import time
import board
import busio

import adafruit_gps


# connect GP0, GP1, 3.3V and GND:
# https://www.waveshare.com/wiki/Pico-GPS-L76B

RX = board.GP1
TX = board.GP0

uart = busio.UART(TX, RX, baudrate=9600, timeout=30)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()
while True:

    gps.update()

    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print('Waiting for fix...')
            continue
        print('=' * 40)  # Print a separator line.
        print('Latitude: {0:.6f} degrees'.format(gps.latitude))
        print('Longitude: {0:.6f} degrees'.format(gps.longitude))
        print('Altitude: {} meters'.format(gps.altitude_m))
        print('Speed: {} knots'.format(gps.speed_knots))
        print('Heading: {} degrees'.format(gps.track_angle_deg))
        print('Timestamp: {}'.format(gps.timestamp_utc))

