import machine
import time
from decode import decode_time, decode_date
from read import read_impulses

# Ustawienie pinu GPIO (np. pin 23) jako wejście
input_pin = machine.Pin(23, machine.Pin.IN)

# Główna pętla programu
bits = read_impulses(input_pin)

# Wyświetlanie wyników
if bits:
    hour, minutes = decode_time(bits)
    day, month, year = decode_date(bits)
    print(f"{hour:02}:{minutes:02}")
    print(f"{day:02}.{month:02}.{year}")
