import serial

ser = serial.Serial('TODO', 9600)

def switch_led(on):
    cmd = "on" if on else "off"
    ser.write(cmd)
