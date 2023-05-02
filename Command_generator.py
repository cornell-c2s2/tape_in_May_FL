from pymtl3 import *
from math import log2

#-------------------------------------------------
# Command generator
#-------------------------------------------------
# input specifications:
# addr: address mapping recorded in https://confluence.cornell.edu/display/c2s2/Address+Mapping


class CommandGenerator:
    
    def __init__(self, fft_size):
        self.fft_size = fft_size
        self.BitsAddr = mk_bits(round(log2(9 + fft_size)) + 1)
        self.address_bitwidth = round(log2(9 + fft_size) + 1)

    #--------------------------------------------------
    # 0x1 FFT_Input_Crossbar_Control
    #--------------------------------------------------
    # [1         |1           |30 ]
    #  input      output       DNC
    # input = 0 → SPI minion
    # input = 1 → SPI master
    # output = 0 → FFT
    # output = 1 → bypass FFT
    def FFT_Input_Crossbar_Control(self, w_en, input, output):
        msg = concat(self.BitsAddr(1), Bits1(w_en), Bits1(input), Bits1(output), Bits30(0))
        return msg

    #--------------------------------------------------
    # 0x2 FFT_Output_Crossbar_Control
    #--------------------------------------------------
    # [1         |31]
    #  input      DNC
    # input = 0 → FFT
    # input = 1 → Bypass FFT
    def FFT_Output_Crossbar_Control(self, w_en, input):
        msg = concat(self.BitsAddr(2), Bits1(w_en), Bits1(input), Bits31(0))
        return msg

    #--------------------------------------------------
    # 0x3 SPI_Master_Frequency_Select
    #--------------------------------------------------
    # [3        | 29]
    #  input    | DNC
    # input = 000 → 1/2 clock speed
    # input = 001 → 1/4 clock speed
    # input = 010 → 1/8 clock speed
    def SPI_Master_Frequency_Select(self, w_en, input):
        msg = concat(self.BitsAddr(3), Bits1(w_en), Bits3(input), Bits29(0))
        return msg

    #--------------------------------------------------
    # 0x4 SPI_Master_Chip_Select
    #--------------------------------------------------
    # [1         |31]
    #  input     |DNC
    # input = 0 → mic
    # input = 1 → undefined
    def SPI_Master_Chip_Select(self, w_en, input):
        msg = concat(self.BitsAddr(4), Bits1(w_en), Bits1(input), Bits31(0))
        return msg

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
    def SPI_Packet_Size_Select(self, w_en, input):
        msg = concat(self.BitsAddr(5), Bits1(w_en), Bits5(input), Bits27(0))
        return msg

    #--------------------------------------------------
    # 0x6 SPI_Master_Crossbar_Select
    #--------------------------------------------------
    # [1         |31]
    #  input     |DNC
    # input = 0 → SPI Minion
    # input = 1 → Constant/continuous mode
    def SPI_Master_Crossbar_Select(self, w_en, input):
        msg = concat(self.BitsAddr(6), Bits1(w_en), Bits1(input), Bits31(0))
        return msg

    #--------------------------------------------------
    # 0x7 FFT_Input_Crossbar_Injection
    #--------------------------------------------------
    # Input = 32 bit fixed point integer with decimal point at 16 bits
    def FFT_Input_Crossbar_Injection(self, w_en):
        msg = concat(self.BitsAddr(7), Bits1(w_en), Bits32(0))
        return msg

    #--------------------------------------------------
    # 0x8 SPI-Master-Crossbar-Injection
    #--------------------------------------------------
    # Input = 32 bit configuration value
    def SPI_Master_Crossbar_Injection(self, w_en, input):
        msg = concat(self.BitsAddr(8), Bits1(w_en), Bits32(input))
        return msg


    #--------------------------------------------------
    # from 9 to 9+fft_size-1: Source-Injection
    #--------------------------------------------------
    # source num = 0 to fft_size - 1
    def Source_Injection(self, w_en, source_num, input):
        msg = concat(self.BitsAddr(source_num+9), Bits1(w_en), Bits32(input))
        return msg