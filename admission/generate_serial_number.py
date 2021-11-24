from string import ascii_letters, digits
from random import choices, shuffle


class SerialNumberGenerator:
    def __init__(self, prefix='', suffix='', units=4, quantity=1, pin_code_len=5):
        self.prefix = prefix
        self.suffix = suffix
        rem = (units - (len(prefix) + len(suffix))) + 1
        self.units = rem if rem else units
        self.quantity = quantity
        self.pin_code_len = pin_code_len

    def _generate_(self, unique=None):
        letters = ''.join(choices(ascii_letters, k=self.units))
        return self.prefix + letters + str(unique) + self.suffix

    def pin_code(self,):
        half_units = int(self.pin_code_len/2)
        nums = choices(list(digits), k=half_units)
        letters = choices(ascii_letters, k=half_units)+nums
        shuffle(letters)
        returns = ''.join(letters)
        return returns

    def __iter__(self):
        return (self._generate_(k) for k in range(self.quantity))
