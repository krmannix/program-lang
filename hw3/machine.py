#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3 (skeleton code)
# machine.py
#

def simulate(s):
    instructions = s if type(s) == list else s.split("\n")
    instructions = [l.strip().split(" ") for l in instructions]
    mem = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: 0}
    control = 0
    outputs = []
    while control < len(instructions):
        # Update the memory address for control.
        mem[6] = control 
        
        # Retrieve the current instruction.
        inst = instructions[control]
        
        # Handle the instruction.
        if inst[0] == 'label':
            pass
        if inst[0] == 'goto':
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'branch' and mem[int(inst[2])]:
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'jump':
            control = mem[int(inst[1])]
            continue
        if inst[0] == 'set':
            mem[int(inst[1])] = int(inst[2])
        if inst[0] == 'copy':
            mem[mem[4]] = mem[mem[3]]
        if inst[0] == 'add':
            mem[0] = mem[1] + mem[2]

        # Push the output address's content to the output.
        if mem[5] > -1:
            outputs.append(mem[5])
            mem[5] = -1

        # Move control to the next instruction.
        control = control + 1

    print("memory: "+str(mem))
    return outputs

# Examples of useful helper functions from lecture.    
def copy(frm, to):
   return [\
      'set 3 ' + str(frm),\
      'set 4 ' + str(to),\
      'copy'\
   ]

def set(addr, val):
    return ['set ' + str(addr) + ' ' + str(val)]


# Go through the list of address and set to zero, then return those functions
def setZero(addrs):
    instrs = []
    for x in addrs:
        instrs += ['set ' + str(x) + ' 0']
    return instrs


def increment(addr):
    instrs = [] # Initialize instructions
    instrs += set('1', '1')
    instrs += copy(addr, 2)
    instrs += ['add']
    instrs += copy(0, addr)
    instrs += setZero([0, 1, 2, 3, 4])
    return instrs

# Same as increment, just uses negative 1 instead
def decrement(addr):
    instrs = [] # Initialize instructions
    instrs += set(1, -1)
    instrs += copy(addr, 2)
    instrs += ['add']
    instrs += copy(0, addr)
    instrs += setZero([0, 1, 2, 3, 4])
    return instrs

def call(name):
    instrs = []
    instrs += decrement(7) # Increase stack size
    instrs += copy(7, 4)
    instrs += ['set 3 6']
    instrs += increment(3) # Inside 3 should have the value that will be placed at the top of the call stack
    instrs += 'copy' # Copy this updated address to top of the call stack
    instrs += ['goto', name]
    instrs += increment(7)
    instrs += setZero([0, 1, 2, 3, 4])
    return instrs

def procedure(name, body):
    labelStart = name + '_start'
    labelEnd = name + '_end'
    instrs = []
    instrs += ['goto' + labelEnd]
    instrs += ['label' + labelStart]
    instrs += body
    # Get the address at the top of the stack currently
    instrs += copy(7, 4)
    instrs += ['jump' + 4]
    instrs += ['label' + labelEnd]
    return instrs

def printVal(val):
    instrs = ['set 5 ' + str(val)]
    return instrs

def printMem(val):
    #  Val is the mem location
    instrs = copy(str(val), 5)  # Move the value in mem[8] to the output buffer
    return instrs

def storeVal(val, addr):
    instrs = set(addr, val)
    return instrs, addr, addr + 1


def assignVal(addr, val):
    instrs = []
    instrs += set(str(addr), str(val))
    return addr, addr + 1, instrs

def addFromMem(addr1, addr2, heap):
    instrs = []
    instrs += copy(str(addr1), 1)
    instrs += copy(str(addr2), 2)
    instrs += ['add']
    instrs += copy(0, heap)
    return instrs, heap, heap + 1

# eof