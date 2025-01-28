#!/usr/bin/env python
import os,sys,math
import bchlib
import galois
import numpy

def convert_polynomial(poly):
    # Transform polynomial object into its decimal representation required for bchlib
    # e.g x^13 + x^5 + x^2 + x + 1 is represented as 10000000100111 in binary or 8231 in decimal
    binary_representation = "".join(str(c) for c in poly.coeffs.astype(numpy.uint32))
    return int(binary_representation,2)


def calculate_parity(data,ecc_strength,poly_decimal,swap_bits):
    bch = bchlib.BCH(ecc_strength, prim_poly=poly_decimal, swap_bits=swap_bits)
    return bch.encode(data)

def find_m(data_size_in_bits):
    # find Galois field order m: 2^m > amount of data to protect in bits
    data_size_in_bits_log2 = math.log2(data_size_in_bits)
    m = math.ceil(data_size_in_bits_log2)
    if m == data_size_in_bits_log2:
        m += 1
    return m

# Get argv
if len(sys.argv) != 3:
    print('Usage:')
    print(f'python search.py <main_data_file> <parity_data_file>')
    sys.exit(1)
eccfname = sys.argv[2]
datafname = sys.argv[1]

# open binary files
eccf = open(eccfname, "rb")
dataf = open(datafname, "rb")
ecc = eccf.read()
data = dataf.read()
eccf.close()
dataf.close()

# find bch parameters
data_size_bits = len(data) * 8
ecc_size_bits = len(ecc) * 8

if data_size_bits < ecc_size_bits:
    print('Data should be larger than ECC')
    sys.exit(1)

m = find_m(data_size_bits)
# find ECC strength t: m * t <= parity data size in bits
t = math.floor(ecc_size_bits / m)

# generate all primitive polynomials of degree m over GF(2)
prim_polys = galois.primitive_polys(2, m)

# search
found_poly = 0
count = 0
for poly in prim_polys:
    poly_decimal = convert_polynomial(poly)
    # calculate ecc for main data for both cases
    swap_bits = False
    data_ecc = calculate_parity(data,t,poly_decimal,swap_bits)
    if data_ecc == ecc:
        found_poly = poly_decimal
        break
    swap_bits = True
    data_ecc = calculate_parity(data,t,poly_decimal,swap_bits)
    if data_ecc == ecc:
        found_poly = poly_decimal
        break
    count += 1

print(f'Searched {count} primitive polynomials')

if found_poly != 0:
    print(f'Found BCH({t}, prim_poly={poly_decimal}, swap_bits={swap_bits})')
else:
    print(f'No match found')
