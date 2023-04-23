from pymtl3 import *

#-------------------------------------------------
#Command generator
#-------------------------------------------------
# input specifications:
# addr: address mapping recorded in https://confluence.cornell.edu/display/c2s2/Address+Mapping
# minion:      1 bit
#              0 - SPI minion, 1 - SPI master
# freq:        3 bits
#              when choosing SPI master, master frequency
# packet_size: 5 bits
#              when choosing SPI master, master packet size
# microphone:  1 bit
#              0 - microphone, 1 - undefined
# master_input:1 bit
#              0 - SPI minion, 1 - Constant/continuous mode
# fft:         1 bit
#              0 - fft, 1 - bypass fft
# fft_input:   32 bits
#              32 bit fixed point integer with decimal point at 16 bits
# master_inj:  32 bits
#              32 bit configuration value
def command_generator(addr, minion, freq, packet_size, microphone, master_input, fft, fft_input, master_inj):
    if (addr == 0):
        return Bits37(1) # what should loopback input output?
    elif (addr == 1):
        return FFT_Input_Crossbar_Control(minion, fft)
    elif (addr == 2):
        return FFT_Output_Crossbar_Control(fft)
    elif (addr == 3):
        return SPI_Master_Frequency_Select(freq)
    elif (addr == 4):
        return SPI_Master_Chip_Select(microphone)
    elif (addr == 5):
        return SPI_Packet_Size_Select(packet_size)
    elif (addr == 6):
        return SPI_Master_Crossbar_Select(master_input)
    elif (addr == 7):
        return FFT_Input_Crossbar_Injection(fft_input)
    elif (addr == 8):
        return SPI_Master_Crossbar_Injection(master_inj)

#--------------------------------------------------
# 0x1 FFT_Input_Crossbar_Control
#--------------------------------------------------
# [1         |1           |30 ]
#  input      output       DNC
# input = 0 → SPI minion
# input = 1 → SPI master
# output = 0 → FFT
# output = 1 → bypass FFT
def FFT_Input_Crossbar_Control(input, output):
    msg = concat(Bits4(1), Bits1(1), Bits1(input), Bits1(output), Bits30(0))
    return Bits37(msg)

#--------------------------------------------------
# 0x2 FFT_Output_Crossbar_Control
#--------------------------------------------------
# [1         |31]
#  input      DNC
# input = 0 → FFT
# input = 1 → Bypass FFT
def FFT_Output_Crossbar_Control(input):
    msg = concat(Bits4(2), Bits1(1), Bits1(input), Bits31(0))
    return Bits37(msg)

#--------------------------------------------------
# 0x3 SPI_Master_Frequency_Select
#--------------------------------------------------
# [3        | 29]
#  input    | DNC
# input = 000 → 1/2 clock speed
# input = 001 → 1/4 clock speed
# input = 010 → 1/8 clock speed
def SPI_Master_Frequency_Select(input):
    msg = concat(Bits4(3), Bits1(1), Bits3(input), Bits29(0))
    return Bits37(msg)

#--------------------------------------------------
# 0x4 SPI_Master_Chip_Select
#--------------------------------------------------
# [1         |31]
#  input     |DNC
# input = 0 → mic
# input = 1 → undefined
def SPI_Master_Chip_Select(input):
    msg = concat(Bits4(4), Bits1(1), Bits1(input), Bits31(0))
    return Bits37(msg)

#--------------------------------------------------
# 0x5 SPI_Packet_Size_Select
#--------------------------------------------------
# [5         |27]
#  input     |DNC
# input = 00000 → packet size = 1
# input = 00001 → packet size = 2
# input = 00010 → packet size = 3
# ......
# input = 11111 → packet size = 32
def SPI_Packet_Size_Select(input):
    msg = concat(Bits4(5), Bits1(1), Bits5(input), Bits27(0))
    return Bits37(msg)

#--------------------------------------------------
# 0x6 SPI_Master_Crossbar_Select
#--------------------------------------------------
# [1         |31]
#  input     |DNC
# input = 0 → SPI Minion
# input = 1 → Constant/continuous mode
def SPI_Master_Crossbar_Select(input):
    msg = concat(Bits4(6), Bits1(1), Bits1(input), Bits31(0))
    return Bits37(msg)

#--------------------------------------------------
# 0x7 FFT_Input_Crossbar_Injection
#--------------------------------------------------
# Input = 32 bit fixed point integer with decimal point at 16 bits
def FFT_Input_Crossbar_Injection(input):
    msg = concat(Bits4(7), Bits1(1), Bits32(input))
    return Bits37(msg)

#--------------------------------------------------
# 0x8 SPI-Master-Crossbar-Injection
#--------------------------------------------------
# Input = 32 bit configuration value
def SPI_Master_Crossbar_Injection(input):
    msg = concat(Bits4(8), Bits1(1), Bits32(input))
    return Bits37(msg)


