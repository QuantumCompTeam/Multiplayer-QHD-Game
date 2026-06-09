"""Single source of truth for game parameters and the bit-ordering convention.

BIT ORDERING CONVENTION
=======================
All probability arrays in this project follow Qiskit's statevector
little-endian ordering. Qubit j occupies bit position j (value 2**j)
of the integer index.

For an N-qubit system, integer index i encodes:
  player j plays Hawk  <=>  (i >> j) & 1 == 1
  player j plays Dove  <=>  (i >> j) & 1 == 0

Worked example (N=2):
  i=0 (0b00) -> player 0 Dove, player 1 Dove
  i=1 (0b01) -> player 0 HAWK, player 1 Dove   (bit 0 = player 0)
  i=2 (0b10) -> player 0 Dove, player 1 HAWK   (bit 1 = player 1)
  i=3 (0b11) -> player 0 HAWK, player 1 HAWK

This matches Statevector.probabilities() output directly — no reordering needed.
Use index_to_bitstring(i, N) in game/payoffs.py for human-readable labels.
"""

import math

V: float = 4.0  # resource value
C: float = 3.0  # conflict cost (C > V/2 ensures Hawk-Dove dynamics are non-trivial)

GAMMA: float = math.pi / 2
# CRITICAL: maximum entanglement requires gamma = pi/2.
# Symptom of wrong gamma: (Q,Q) payoff falls below (2,2) and Nash property fails.
# Do not change without re-running test_two_player.py.
