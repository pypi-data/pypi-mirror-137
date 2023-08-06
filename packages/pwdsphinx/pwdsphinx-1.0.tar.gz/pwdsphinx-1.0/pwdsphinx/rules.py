#!/usr/bin/env python

import bin2pass
import pysodium

"""
|---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | e | f |
|---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---|
|       password size       | U | L | D |' '| ! | " | # | $ | % |
|---------------------------+---+---+---+---+-------------------|

|---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---|
|10 |11 |12 |13 |14 |15 |16 |17 |18 |19 |1a |1b |1c |1d |1e |1f |
|---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---|
| & | ' | ( | ) | * | + | , | - | . | / | : | ; | < | = | > | ? |
|---------------------------+---+---+---+---+-------------------|

|---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---|
|20 |21 |22 |23 |24 |25 |26 |27 |28 |29 |2a |2b |2c |2d |2e |2f |
|---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---|
| @ | [ | \ | ] | ^ | _ | ` | { | | | } | ~ |    check-digit    |
|---------------------------+---+---+---+---+-------------------|

and 32 bytes xor mask

"""

def unpack_rule(noncect):
  nonce, ct = nonce_ct[:24], nonce_ct[24:]
  packed = pysodium.crypto_stream_xchacha20_xor(ct, nonce, get_sealkey())
  xor_mask = packed[-32:]
  v = int.from_bytes(packed[:-32], "big")

  size = v & ((1<<7) - 1)
  rule = {c for i,c in enumerate(('u','l','d')) if (v >> 7) & (1 << i)}
  symbols = [c for i,c in enumerate(bin2pass.symbols) if (v>>(7+3) & (1<<i))]
  check_digit = (v>>(7+3+33))

  return rule, symbols, size, check_digit, xor_mask

def pack_rule(char_classes, syms, size, check_digit, xor_mask=None):
  # pack rules into 2 bytes, and encrypt them
  if set(char_classes) - {'u','l','d'}:
    raise ValueError("error: rules can only contain any of 'uld'.")
  if set(syms) - set(bin2pass.symbols) != set():
    raise ValueError("error: symbols can only contain any of '%s'." % bin2pass.symbols)
  if char_classes == '' and len(syms)<2:
    raise ValueError("error: no char classes and not enough symbols specified.")
  if xor_mask is None:
      xor_mask = b'\x00' * 32
  elif len(xor_mask)!=32:
    raise ValueError("error: xor_mask must be 32bytes, is instead: %d." % len(xor_mask))
  if size<0 or size>127:
    raise ValueError("error: invalid max password size: %d." % size)

  packed = size
  packed = packed + (sum(1<<i for i, c in enumerate(('u','l','d')) if c in char_classes) << 7)
  packed = packed + (sum(1<<i for i, c in enumerate(bin2pass.symbols) if c in syms) << (7 + 3))
  packed = packed + ((check_digit & (2**5 - 1)) << (7 + 3 + 33) )
  pt = packed.to_bytes(6,"big") + xor_mask
  nonce = pysodium.random_buf(pysodium.crypto_stream_xchacha20_NONCEBYTES)
  ct = pysodium.crypto_stream_xchacha20_xor(pt, nonce, get_sealkey())
  return nonce+ct

def tests():
    for cls in powerset('uld'):
        equ(''.join(cls), bin2pass.symbols, 64, 31, b'\x00'*32)
        if cls!=tuple():
            equ(''.join(cls), '', 64, 31, b'\x00'*32)

    equ('uld', bin2pass.symbols[:16], 64, 31, b'\x00'*32)
    equ('uld', bin2pass.symbols[16:], 64, 31, b'\x00'*32)

    equ('uld', bin2pass.symbols, 64, 31, b'\xff'*32)
    equ('uld', bin2pass.symbols, 64, 31, b'\xaa'*32)

    for i in range(128):
        equ('uld', bin2pass.symbols, i, 31, b'\xaa'*32)
    for i in range(32):
        equ('uld', bin2pass.symbols, 64, i, b'\xaa'*32)

def equ(classes, syms, size, check, xor):
    unpacked = unpack_rule(pack_rule(classes, syms, size, check, xor))
    assert set(classes) == unpacked[0]
    assert list(syms) == unpacked[1]
    assert size == unpacked[2]
    assert check == unpacked[3]
    assert xor == unpacked[4]

from itertools import chain, combinations
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

tests()
