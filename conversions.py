
# -- Memory representation
#    Memory is a sequence of bytes. The address of a byte is its
#    index in that sequence. That's it!
Size = 32
Memory = [0 for _ in range(Size)]


# -- Clear memory
#    Set all the bits to 0
def clear_memory():
    for i in range(len(Memory)):
        Memory[i] = 0


# -- Convert a byte to a binary string
#    For use in printing the memory state as bits
def as_binary(byte):
    bin = ''
    for bit in range(8):
        if byte & 128 == 0:
            bin = bin + '0'
        else:
            bin = bin + '1'
        byte = byte << 1
    return bin


# -- Show contents of memory
#    Display all the bits in memory. This format prints the
#    bytes in order, with four bytes (32 bits) on each line
#    The column at the left side shows the address.
def show_memory():
    print("MEMORY:")
    for i in range(0, len(Memory), 4):
        line = ''
        for j in range(4):
            b = Memory[i + j]
            line = line + as_binary(b) + ' '
        print('{:3d}  {}'.format(i, line))


# === Memory access ================================================

# -- Load a byte from the given address
#    Raise a 'Segmentation fault' error if the address is outside
#    the legal range for the memory
def load_byte(address):
    if address >= Size or address < 0:
        print("Seg fault")
        return None
    else:
        return Memory[address]


# -- Store a byte value to the given address
#    Raise a 'Segmentation fault' error if the address is outside
#    the legal range for the memory
def store_byte(byte, address):
    if address >= Size or address < 0:
        print("Seg fault")
        return None
    else:
        Memory[address] = (byte % 256)


# -- Load an unsigned 8-bit int from the given address
def load_uint8(address):
    val = load_byte(address)
    return val


# -- Store an unsigned 8-bit int to the given address
def store_uint8(sint, address):
    val = sint % 256
    store_byte(val, address)


# -- Load a signed 8-bit int from the given address
#    Decode from two's-complement representation
def load_sint8(address):
    uint = load_uint8(address)
    if uint > 127:
        sint = uint - 256
    else:
        sint = uint
    return sint


# -- Store a signed 8-bit int to the given address
#    Convert to two's complement representation
def store_sint8(val, address):
    if val < 0:
        uint = val + 256
    else:
        uint = val
    store_uint8(uint, address)

# -- Load an unsigned 16-bit int from the given address
def load_uint16(address):
    high = load_byte(address)
    low = load_byte(address+1)
    val = high * 256 + low
    return val


# -- Store an unsigned 16-bit int to the given address
def store_uint16(val, address):
    high = (val // 256) % 256
    low = val % 256
    store_byte(high, address)
    store_byte(low, address+1)


# -- Load a signed 16-bit int from the given address
def load_sint16(address):
    uint = load_uint16(address)
    if uint > 32767:
        sint = uint - 65536
    else:
        sint = uint
    return sint


# -- Store a signed 16-bit int to the given address
def store_sint16(val, address):
    if val < 0:
        uint = val + 65536
    else:
        uint = val
    store_uint16(uint, address)


# === Variable access functions =====================================

# -- Make a new variable
#    record the address and the type, which must be a string
#    that is one of 'uint8', 'sint8', 'uint16', 'sint16'
#    Return the new variable
def var(address, type):
    return (address, type)


# -- Get the value of a var
#    Load the value from the variable's address according to its type
def get_var(v):
    if type(v) is int:
        return v
    else:
        (address, typ) = v
        if typ == 'uint16':
            return load_uint16(address)
        if typ == 'sint16':
            return load_sint16(address)
        if typ == 'uint8':
            return load_uint8(address)
        if typ == 'sint8':
            return load_sint8(address)
        return None


# --- Set the value of a var
#     Store the value into the address according to its type
def set_var(v, val):
    (address, typ) = v
    if typ == 'uint16':
        store_uint16(val, address)
    if typ == 'sint16':
        store_sint16(val, address)
    if typ == 'uint8':
        store_uint8(val, address)
    if typ == 'sint8':
        store_sint8(val, address)


# === Assembly-like functions =======================================

# -- Move (copy) the value from the src variable to the dest
#    variable, converting the representation if necessary.
#    The src can also be a literal number.
def mov(src, dest):
    if type(src) is int:
        val = src
    else:
        val = get_var(src)
    set_var(dest, val)

# -- Add the value of op1 to op2 and store the result in op2
#    Equivalent to op2 = op1 + op2
#    op1 can be a literal
def add(op1, op2):
    v1 = get_var(op1)
    v2 = get_var(op2)
    v = v1 + v2
    set_var(op2, v)


# -- Subtract op2 from op1, store the result in op1
#    Equivalent to op1 = op1 - op2
#    op2 can be a literal
def sub(op1, op2):
    v1 = get_var(op1)
    v2 = get_var(op2)
    v = v1 - v2
    set_var(op1, v)


# -- Multiply op1 and op2 and store in op3
#    Equivalent to op3 = op1 * op2
#    op1 or op2 can be literals
def mul(op1, op2, op3):
    v1 = get_var(op1)
    v2 = get_var(op2)
    v = v1 * v2
    set_var(op3, v)

# -- Compare two variables, return True if op1 == op2
#    Either op can be a literal
def equal(op1, op2):
    v1 = get_var(op1)
    v2 = get_var(op2)
    return v1 == v2


# -- Compare two variables, return True if op1 < op2
#    Either op can be a literal
def less_than(op1, op2):
    v1 = get_var(op1)
    v2 = get_var(op2)
    return v1 < v2


# -- Compare two variables, return True if op1 <= op2
#    Either op can be a literal
def less_than_or_equal(op1, op2):
    v1 = get_var(op1)
    v2 = get_var(op2)
    return v1 <= v2


# -- Ask the user to enter a value, store the result in op
def read(msg, op):
    v = int(input(msg))
    set_var(op, v)


# -- Print the value of op with a message (a string)
def show(msg, op):
    v = get_var(op)
    fmt = msg + "{}"
    print(fmt.format(v))


# === Finally, the program ==========================================

# Exercise 1:
# Use a larger int (more bits) to discover the limitations of a smaller one
small_int = var(4, 'sint8')
big_int = var(8, 'uint16')

mov(1, small_int)
mov(1, big_int)
while equal(small_int, big_int):
    add(1, small_int)
    add(1, big_int)

show('Small int is ', small_int)
show('Big int is ', big_int)


# Exercise 2:
# Compute a student's age based on the number of years in college
# Overflow the number of years to get a smaller age. Try entering
# an age close to the 8-bit limit -- something like 254. Notice that
# it is the same bit pattern as signed int -2.

years = var(2, 'uint8')
age = var(4, 'uint8')
mov(17, age)
read('Enter number of years in college: ', years)
add(years, age)
show('Your age is ', age)


# Exercise 3:
# Compute the cost for some number of widgets and some number of gadgets.
# A widget costs $12, a gadget costs $7. It is possible by choosing the
# right number of widgets and gadgets to overflow the cost and end up
# paying $0
# Try entering 19 widgets and 4 gadgets (there are other solutions)

num_widgets = var(10, 'uint8')
num_gadgets = var(12, 'uint8')
read('Enter number of widgets:', num_widgets)
read('Enter number of gadgets:', num_gadgets)
widget_cost = var(14, 'uint8')
gadget_cost = var(16, 'uint8')
total_cost = var(18, 'uint8')
mul(num_widgets, 12, widget_cost)
mul(num_gadgets, 7, gadget_cost)
mov(widget_cost, total_cost)
add(gadget_cost, total_cost)
show('Total cost is ', total_cost)


# Exercise 4:
# Compute the award for a credit card points system. Each point is worth $4.
# The max amount of the award is $500, no matter how many points the
# customer has. You can get much more by entering the right number of points.
# Try entering a small negative number, which still satisfies the less-than
# check, but when converted to an unsigned int, becomes a huge number. This
# is the same strategy used against SSH in a real attack.

max_award = var(10, 'uint16')
mov(500, max_award)
final_award = var(16, 'uint16')
points = var(12, 'sint16')
award = var(14, 'sint16')
read('How many points? ', points)
mul(points, 4, award)
if less_than(award, max_award):
    mov(award, final_award)
else:
    mov(max_award, final_award)
show('Awarded: $', final_award)
