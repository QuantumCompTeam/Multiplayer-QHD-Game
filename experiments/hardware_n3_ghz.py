import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_aer import AerSimulator

# ── Build the N=3 GHZ EWL circuit ──
# Q_3 = U(0, pi/3, pi/3). This is the canonical structure — swap in your
# repo's validated J / J-dagger entangler before the real hardware run.
N = 3
qr = QuantumRegister(N, "q")
cr = ClassicalRegister(N, "meas")
qc = QuantumCircuit(qr, cr)

# J: GHZ-style entangler
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)

# Local quantum strategy Q_3 = U(theta=0, phi=pi/3, lam=pi/3) on each player
for q in range(N):
    qc.u(0, np.pi/3, np.pi/3, q)

# J-dagger: inverse entangler
qc.cx(0, 2)
qc.cx(0, 1)
qc.h(0)

qc.measure(qr, cr)

# ── Dry run on the noiseless simulator ──
backend = AerSimulator()
pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
isa = pm.run(qc)

result = Sampler(mode=backend).run([isa], shots=4096).result()
counts = result[0].data.meas.get_counts()

print("counts:", counts)
print("transpiled depth:", isa.depth(), "| 2q gates:", isa.num_nonlocal_gates())