# Test cases for tape_in_Mar_FL.py
from pymtl3 import *
import math
import numpy as np
from tape_in_May_FL import *

BIT_WIDTH    = 32

def random_fft_input_generate(fft_size):
    input_array = []
    for i in range(fft_size):
        input_array.append(math.trunc(i* (2**16)))
    return input_array

def main():
    May_FL = TapeInMayFL()
    fft_input_xbar_from_spi_minion_to_fft = Bits37(0x0340000000) # 0001 | 1    | 0 | 1 | 30b'0
                                                                 # addr | w_en | in|out|
    fft_output_xbar_from_fft              = Bits37(0x0500000000) # 0010 | 1    | 0 | 31b'0
                                                                 # addr | w_en | in|
    # set two xbars
    inst_arr_1 = [
        fft_input_xbar_from_spi_minion_to_fft,
        fft_output_xbar_from_fft
        ]

    for i in inst_arr_1:
        resp = May_FL.SPI_minion_input(i)
        print(resp)
        i[BIT_WIDTH:BIT_WIDTH + 1] = 1
        print(resp) # resp shouldn't change with i

        

if __name__ == "__main__":
    main()
