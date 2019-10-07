try:
    from periphery import GPIO
except ImportError:
    raise ImportError("Failed to inport python-periphery")

# Pins dont exist in CPython so...lets make our own!
class Pin:
    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2
    _CONSUMER = 'adafruit_blinka'

    id = None
    _value = LOW
    _mode = IN

    def __init__(self, pin_id):
        self.id = pin_id
        if type(pin_id) is tuple:
            raise NotImplementedError("Tuple as pin id is not supported")
        else:
            self._num = int(pin_id)
        self._line = None

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        if mode != None:
            if self._line:
                self._line.close()
                self._line = None
            if mode == self.IN:
                flags = 0
                if pull != None:
                    if pull == self.PULL_UP:
                        raise NotImplementedError("Internal pullups not supported in libgpiod, use physical resistor instead!")
                    elif pull == self.PULL_DOWN:
                        raise NotImplementedError("Internal pulldowns not supported in libgpiod, use physical resistor instead!")                    
                    else:
                        raise RuntimeError("Invalid pull for pin: %s" % self.id)

                self._mode = self.IN
                self._line = GPIO(self._num, "in")

            elif mode == self.OUT:
                if pull != None:
                    raise RuntimeError("Cannot set pull resistor on output")
                self._mode = self.OUT
                self._line = GPIO(self._num, "out")

            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)

    def value(self, val=None):
        if val != None:
            if val in (self.LOW, self.HIGH):
                self._value = val
                self._line.write(val == self.HIGH)
            else:
                raise RuntimeError("Invalid value for pin")
        else:
            return self.HIGH if self._line.read() else self.LOW
