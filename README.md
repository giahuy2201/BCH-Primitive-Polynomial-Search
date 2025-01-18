# BCH Primitive Polynomial Search for Flash Dump

[BCH algorithm](https://en.wikipedia.org/wiki/BCH_code) is widely used for ECC calculation and bitflip protection in NAND flash memory. By storing a small amount parity data along with the main data to be protected, the algorithm could detect and correct bitflips up to a certain extend. However, this also makes the process of reading and writing data onto the flash chip a bit less transparent especially when vendors decide to 'tweak' the algorithm by using different paramters. 

Given a sample of real data and its parity data, the program derives ECC step size (the amount of data to protect) `m` and ECC strength (number of bitflips to protect against) `t` from the number of bytes in those files. It then generates a list of possible primitive polynomials of degree `m` over `GF(2)` and search for one that correctly encode main data into parity data

## Demo

## Usage

Install dependencies

```bash
pip install -r requirements.txt
```

Run `search.py` with binary data files

```bash
python search.py data.bin ecc.bin
```