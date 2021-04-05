from Valve import Valve
from time import sleep

hot = Valve(5)
cold = Valve(6)

hot.open()
sleep(1)
hot.close()
sleep(1)
cold.open()
sleep(1)
cold.close()