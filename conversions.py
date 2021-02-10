
# -- Memory is a big array of bytes
Size = 32
Memory = [0 for _ in range(Size)]


def clear_memory():
    for i in range(len(Memory)):
        Memory[i] = 0


def as_binary(byte):
    bin = ''
    for bit in range(8):
        if byte & 128 == 0:
            bin = bin + '0'
        else:
            bin = bin + '1'
    return bin


def show_memory():
    for i in range(0, len(Memory), 4):
        line = ''
        for j in range(4):
            b = Memory[i + j]
            line = line + as_binary(b) + ' '
        print('{:3d}  {}'.format(i, line))


def load_byte(address):
    if address >= Size or address < 0:
        print("Seg fault")
        return None
    else:
        return Memory[address]


def store_byte(byte, address):
    if address >= Size or address < 0:
        print("Seg fault")
        return None
    else:
        Memory[address] = byte


def load_uint8(address):
    val = load_byte(address)
    return val


def store_uint8(sint, address):
    val = sint % 256
    store_byte(val, address)


def load_sint8(address):
    uint = load_uint8(address)
    if uint > 127:
        sint = uint - 256
    else:
        sint = uint
    return sint


def store_sint8(val, address):
    if val < 0:
        uint = val + 256
    else:
        uint = val
    store_uint8(uint, address)


def load_uint16(address):
    high = load_byte(address)
    low = load_byte(address+1)
    val = high * 256 + low
    return val


def store_uint16(val, address):
    high = (val // 256) % 256
    low = val % 256
    store_byte(high, address)
    store_byte(low, address+1)


def load_sint16(address):
    uint = load_uint16(address)
    if uint > 32767:
        sint = uint - 65536
    else:
        sint = uint
    return sint


def store_sint16(val, address):
    if val < 0:
        uint = val + 65536
    else:
        uint = val
    store_uint16(uint, address)


all_variables = {}

def var(name, address, type):
    all_variables[name] = (address, type)


def get_var(name):
    if name in all_variables:
        (address, type) = all_variables[name]
        if type == 'uint16':
            return load_uint16(address)
        if type == 'sint16':
            return load_sint16(address)
        if type == 'uint8':
            return load_uint8(address)
        if type == 'sint8':
            return load_sint8(address)
    return None

def set_var(name, val):
    if name in all_variables:
        (address, type) = all_variables[name]
        if type == 'uint16':
            store_uint16(val, address)
        if type == 'sint16':
            store_sint16(val, address)
        if type == 'uint8':
            store_uint8(val, address)
        if type == 'sint8':
            store_sint8(val, address)
    return None


def copy_var(src, dest):
    val = get_var(src)
    set_var(dest, val)


def add(src1, src2, dest):
    v1 = get_var(src1)
    if type(src2) is int:
        v2 = src2
    else:
        v2 = get_var(src2)
    v = v1 + v2
    set_var(dest, v)


def less_than(src1, src2):
    v1 = get_var(src1)
    v2 = get_var(src2)
    return v1 < v2


def less_than_or_equal(src1, src2):
    v1 = get_var(src1)
    v2 = get_var(src2)
    return v1 <= v2


var('value', 8, 'sint16')
var('prev',  10, 'sint8')
set_var('value', 0)
set_var('prev', 0)
while less_than_or_equal('prev', 'value'):
    copy_var('value', 'prev')
    add('value', 5, 'value')
    print('prev = {}  val = {}'.format(get_var('prev'), get_var('value')))
