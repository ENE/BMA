from PyNeuro.PyNeuro import PyNeuro

pn = PyNeuro()

def blinkStrength_callback(value):
    print("blink:", value)

pn.set_blinkStrength_callback(blinkStrength_callback)

pn.connect()
pn.start()