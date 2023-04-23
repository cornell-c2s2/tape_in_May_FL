# Test cases for tape_in_Mar_FL.py
from pymtl3 import *
import math
import numpy as np
from tape_in_May_FL import *
from command_generator import *

BIT_WIDTH    = 32

def sample_fft_input_generate(fft_size):
    input_array = []
    for i in range(fft_size):
        input_array.append(math.trunc(i* (2**16)))
    return input_array

def test_minion_pass_fft_control():
    May_FL = TapeInMayFL(8)

    # set two xbars
    fft_input_xbar_from_spi_minion_to_fft = FFT_Input_Crossbar_Control(0, 0)
    fft_output_xbar_from_fft              = FFT_Output_Crossbar_Control(0)

    inst_arr = [
        fft_input_xbar_from_spi_minion_to_fft,
        fft_output_xbar_from_fft
        ]

    for i in inst_arr:
        resp = May_FL.SPI_minion_input(i)
        i[BIT_WIDTH:BIT_WIDTH + 1] = 1
        assert(resp == i)
    
    assert(May_FL.FFT_input_Xbar_in_state == 0)
    assert(May_FL.FFT_input_Xbar_out_state == 0)
    assert(May_FL.FFT_output_Xbar_in_state == 0)

    print("minion-fft control test passed\n")

def test_minion_pass_fft_data():
    May_FL = TapeInMayFL(8)

    # set two xbars
    fft_input_xbar_from_spi_minion_to_fft = FFT_Input_Crossbar_Control(0, 0)
    fft_output_xbar_from_fft              = FFT_Output_Crossbar_Control(0)

    inst_arr = [
        fft_input_xbar_from_spi_minion_to_fft,
        fft_output_xbar_from_fft
        ]

    # create a list of 8 Bits32 fft numbers
    arr = sample_fft_input_generate(8)
    # create 8 instructions to inject the numbers
    for num in arr:
        inst_arr.append(FFT_Input_Crossbar_Injection(num))

    for i in inst_arr:
        resp = May_FL.SPI_minion_input(i)
        i[BIT_WIDTH:BIT_WIDTH + 1] = 1
    
    assert(May_FL.FFT_input_Xbar_in_state == 0)
    assert(May_FL.FFT_input_Xbar_out_state == 0)
    assert(May_FL.FFT_output_Xbar_in_state == 0)

    print("minion-fft data test passed\n")

def main():
    test_minion_pass_fft_control()
    test_minion_pass_fft_data()

        
if __name__ == "__main__":
    main()
