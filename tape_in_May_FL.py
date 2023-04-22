"""
Class which acts as a functional Level
Model for the FFT System.
Generates SPI feedback at the message level, not the SPI Level
Made by Will Salcedo '23
"""

from pymtl3 import *
from math import log2
import math
import numpy as np

class TapeInMayFL:
    ADDRESS_MAPPING = {
        'Loopback':                  Bits4(0),
        'FFT_input_XBar':            Bits4(1),
        'FFT_output_XBar':           Bits4(2),
        'SPI_master_frequency_sel':  Bits4(3),
        'SPI_master_chip_sel':       Bits4(4),
        'SPI_packet_size_sel':       Bits4(5),
        'SPI_master_xbar_sel':       Bits4(6),
        'FFT_input_crossbar_inj':    Bits4(7), 
        'SPI_master_xbar_inj':       Bits4(8)
    }

    BIT_WIDTH    = 32
    DECIMAL_PT   = 16
    FFT_LRG_SIZE = 256
    FFT_SML_SIZE = 8
    MAXIMUM_ADDRESSIBLE_COMPONENTS = 16
    LOG2_MAXIMUM_ADDRESSIBLE_COMPONENTS = round(log2(MAXIMUM_ADDRESSIBLE_COMPONENTS))


    def __init__(self):
        self.FFT_input_XBar_in_state    = Bits32(0)
        self.FFT_input_XBar_out_state   = Bits32(0)
        self.FFT_output_XBar_in_state   = Bits32(0)
        self.FFT_output_XBar_out_state  = Bits32(0)
        self.SPI_master_frequency_state = Bits32(0)
        self.SPI_master_chip_select     = Bits32(0)
        self.SPI_master_pkt_size_select = Bits32(0)
        self.SPI_master_Xbar_state      = Bits32(0)
        self.source_state               = Bits32(0)

        self.deserializer_buffer        = []
        self.source_buffer              = []

        print("Tape-in May 2023 module initialized")
    
    #Takes a message you would send over SPI in the PyMTL bits Datatype
    #Returns an array of bits that designate the return type.
    def SPI_minion_input(self, input_bits):

        BIT_WIDTH = TapeInMayFL.BIT_WIDTH
        DECIMAL_PT = TapeInMayFL.DECIMAL_PT
        FFT_LRG_SIZE = TapeInMayFL.FFT_LRG_SIZE
        FFT_SML_SIZE = TapeInMayFL.FFT_SML_SIZE

        LOG2_MAXIMUM_ADDRESSIBLE_COMPONENTS = TapeInMayFL.LOG2_MAXIMUM_ADDRESSIBLE_COMPONENTS
        ADDRESS_MAPPING = TapeInMayFL.ADDRESS_MAPPING

        w_en    = input_bits[BIT_WIDTH:BIT_WIDTH + 1] # [32:33]
        address = input_bits[BIT_WIDTH + 1:BIT_WIDTH + 1 + LOG2_MAXIMUM_ADDRESSIBLE_COMPONENTS] # [34:37]
        msg     = input_bits[:BIT_WIDTH] # [0:31]

        if(address == ADDRESS_MAPPING['Loopback']):
            # loopback just returns what is given
            return input_bits
            
        elif(address == ADDRESS_MAPPING['FFT_input_XBar']):
            if (w_en):
                self.FFT_input_Xbar_in_state  = msg[BIT_WIDTH - 1:BIT_WIDTH]
                self.FFT_input_Xbar_out_state = msg[BIT_WIDTH - 2:BIT_WIDTH - 1]
            # set ack signal to 1 for return
            input_bits[BIT_WIDTH:BIT_WIDTH + 1] = 1
            return input_bits

        elif(address == ADDRESS_MAPPING['FFT_output_XBar']):
            if (w_en):
                self.FFT_output_Xbar_in_state  = msg[BIT_WIDTH - 1:BIT_WIDTH]
            # set ack signal to 1 for return
            input_bits[BIT_WIDTH:BIT_WIDTH + 1] = 1
            return input_bits

        elif(address == ADDRESS_MAPPING['SPI_master_frequency_sel']):
            # set ack signal to 1 for return
            input_bits[BIT_WIDTH:BIT_WIDTH + 1] = 1
            return input_bits

        elif(address == ADDRESS_MAPPING['SPI_master_chip_sel']):
            # set ack signal to 1 for return
            input_bits[BIT_WIDTH:BIT_WIDTH + 1] = 1
            return input_bits

        elif(address == ADDRESS_MAPPING['SPI_packet_size_sel']):
            # set ack signal to 1 for return
            input_bits[BIT_WIDTH:BIT_WIDTH + 1] = 1
            return input_bits

        elif(address == ADDRESS_MAPPING['SPI_master_xbar_sel']):
            if (w_en):
                self.FFT_input_Xbar_in_state  = msg[BIT_WIDTH - 1:BIT_WIDTH]
            # set ack signal to 1 for return
            input_bits[BIT_WIDTH:BIT_WIDTH + 1] = 1
            return input_bits      

        elif(address == ADDRESS_MAPPING['FFT_input_crossbar_inj']):
            if(w_en):
                self.source_buffer.append(msg)
                self.source_state  = self.source_state + 1

                #  if source received all message inputs, pass to the FFT
            if (self.source_state == FFT_SML_SIZE):
                self.source_state = 0
                if(self.FFT_input_Xbar_in_state == 0 and self.FFT_input_Xbar_out_state == 1 and self.FFT_output_Xbar_in_state == 1):
                    return msg
                elif(self.FFT_input_Xbar_in_state == 0 and self.FFT_input_Xbar_out_state == 0 and self.FFT_output_Xbar_in_state == 0):
                    return fixed_point_fft(BIT_WIDTH, DECIMAL_PT, FFT_SML_SIZE, self.source_buffer)

            # set ack signal to 1 for return
            input_bits[BIT_WIDTH:BIT_WIDTH + 1] = 1
            return input_bits

        elif(address == ADDRESS_MAPPING['SPI_master_xbar_inj']):
            # set ack signal to 1 for return
            input_bits[BIT_WIDTH:BIT_WIDTH + 1] = 1
            return input_bits


def fixed_point_fft(BIT_WIDTH, DECIMAL_PT, SIZE_FFT, x):
    X_r = list(x)
    X_i = np.zeros(SIZE_FFT)
    
    j = round(SIZE_FFT // 2)


    for i in range(1, SIZE_FFT - 1):
        if i >= j:

            X_r[round(i)], X_r[round(j)] = X_r[round(j)], X_r[round(i)]
        
        k = SIZE_FFT/2

        while(1):
            if k > j:
                break
            j -= k
            k /= 2
        j += k

    sine_table = np.zeros(SIZE_FFT)

    for i in range(SIZE_FFT):
        X_i[i] = 0
        sine_table[i] = math.trunc(math.sin((2 * math.pi * i / SIZE_FFT)) * (2**DECIMAL_PT))

    for stage in range(round(math.log2(SIZE_FFT))):
        
        X_r, X_i = fixed_point_fft_stage(BIT_WIDTH, DECIMAL_PT, SIZE_FFT, stage, sine_table, X_r, X_i)

    return X_r

def fixed_point_fft_stage( BIT_WIDTH, DECIMAL_PT, SIZE_FFT, STAGE_FFT, sine_table, X_r, X_i):
    for m in range( 2 ** STAGE_FFT ):
        for i in range( m, SIZE_FFT, 2 ** (STAGE_FFT + 1)):
            #print("m: " + str(m))
            if( m != 0 ):    
                w_r = sine_table[round((m * SIZE_FFT / (2 * (2 ** STAGE_FFT))) % SIZE_FFT + SIZE_FFT/4)]
                w_im = -sine_table[round((m * SIZE_FFT / (2 * (2 ** STAGE_FFT))) % SIZE_FFT)]
            if( m == 0 ):
                w_r = 1 * (2**DECIMAL_PT)
                w_im = 0
            X_r[round(i)], X_r[round(i + 2 ** STAGE_FFT)], X_i[round(i)], X_i[round(i + 2 ** STAGE_FFT)] = bfu( X_r[round(i)], X_r[round(i + 2 ** STAGE_FFT)], X_i[round(i)], X_i[round(i + 2 ** STAGE_FFT)], w_r, w_im, BIT_WIDTH, DECIMAL_PT)
    return X_r, X_i

def bfu(a_r, b_r, a_i, b_i, w_r, w_im, BIT_WIDTH, DECIMAL_PT):

    """
    print("w_r: " + str(w_r))
    print("w_i: " + str(w_im))
    print("a_r: " + str(a_r))
    print("a_i: " + str(a_i))
    """

    t_r = ((w_r * b_r) // (2**DECIMAL_PT)) - ((w_im * b_i) // (2**DECIMAL_PT))
    t_i = ((w_r + w_im) * (b_r + b_i) // (2**DECIMAL_PT)) - (w_r * b_r) // (2**DECIMAL_PT) - (w_im * b_i) / (2**DECIMAL_PT)
    
    c_r = a_r + t_r
    c_i = a_i + t_i 

    d_r = a_r - t_r
    d_i = a_i - t_i


    return c_r, d_r, c_i, d_i