import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.basis_change import QFT


def phi_adder(num_qubits: int):
    qr_a = QuantumRegister(num_qubits, name="a")
    qr_b = QuantumRegister(num_qubits, name="b")
    qr_z = QuantumRegister(1, name="cout")
    qr_list = [qr_a, qr_b, qr_z]

    qc = QuantumCircuit(*qr_list, name="phi_adder")

    for i in range(num_qubits):
        for j in range(num_qubits - i):
            lam = np.pi / (2 ** j)
            qc.cp(lam, qr_a[i], qr_b[i + j])

    for i in range(num_qubits):
        lam = np.pi / (2 ** (i + 1))
        qc.cp(lam, qr_a[num_qubits - i - 1], qr_z[0])

    return qc.to_gate()


def adder_modulo(num_qubits: int):
    # define qubits
    qr_a = QuantumRegister(num_qubits, "a")
    qr_b = QuantumRegister(num_qubits + 1, "b")  # avoid to overflow
    qr_n = QuantumRegister(num_qubits, "n")
    qr_z = QuantumRegister(1, "z")  # zero
    qr_list = [qr_a, qr_b, qr_n, qr_z]

    # define circuit
    qc = QuantumCircuit(*qr_list, name="adder_modulo")

    # a + b
    qc.append(QFT(num_qubits+1, do_swaps=False).to_gate(), qr_b[:])
    qc.append(phi_adder(num_qubits), qr_a[:] + qr_b[:])
    # a + b - n
    qc.append(phi_adder(num_qubits).inverse(), qr_n[:] + qr_b[:])
    # check for overflow
    qc.append(QFT(num_qubits+1, do_swaps=False).inverse().to_gate(), qr_b[:])
    qc.cx(qr_b[-1], qr_z[:])
    qc.append(QFT(num_qubits+1, do_swaps=False).to_gate(), qr_b[:])
    # add n if overflow
    qc.append(phi_adder(num_qubits).control(1), qr_z[:] + qr_n[:] + qr_b[:])
    # sub a
    qc.append(phi_adder(num_qubits).inverse(), qr_a[:] + qr_b[:])
    # restore zero
    qc.append(QFT(num_qubits+1, do_swaps=False).inverse().to_gate(), qr_b[:])
    qc.x(qr_b[-1])
    qc.cx(qr_b[-1], qr_z[:])
    qc.x(qr_b[-1])
    qc.append(QFT(num_qubits+1, do_swaps=False).to_gate(), qr_b[:])
    # add a
    qc.append(phi_adder(num_qubits), qr_a[:] + qr_b[:])
    qc.append(QFT(num_qubits+1, do_swaps=False).inverse().to_gate(), qr_b[:])

    return qc.to_gate()


def cc_adder_modulo(num_qubits: int):
    # define qubits
    qr_c = QuantumRegister(2, "c")  # control
    qr_a = QuantumRegister(num_qubits, "a")
    qr_b = QuantumRegister(num_qubits + 1, "b")  # avoid to overflow
    qr_n = QuantumRegister(num_qubits, "n")
    qr_z = QuantumRegister(1, "z")  # zero
    qr_list = [qr_c, qr_a, qr_b, qr_n, qr_z]

    # define circuit
    qc = QuantumCircuit(*qr_list, name="cc_adder_modulo")

    # a + b
    qc.append(QFT(num_qubits+1, do_swaps=False).to_gate(), qr_b[:])
    qc.append(phi_adder(num_qubits).control(2), qr_c[:] + qr_a[:] + qr_b[:])
    # a + b - n
    qc.append(phi_adder(num_qubits).inverse(), qr_n[:] + qr_b[:])
    # check for overflow
    qc.append(QFT(num_qubits+1, do_swaps=False).inverse().to_gate(), qr_b[:])
    qc.cx(qr_b[-1], qr_z[:])
    qc.append(QFT(num_qubits+1, do_swaps=False).to_gate(), qr_b[:])
    # add n if overflow
    qc.append(phi_adder(num_qubits).control(1), qr_z[:] + qr_n[:] + qr_b[:])
    # sub a
    qc.append(phi_adder(num_qubits).control(2).inverse(), qr_c[:] + qr_a[:] + qr_b[:])
    # restore zero
    qc.append(QFT(num_qubits+1, do_swaps=False).inverse().to_gate(), qr_b[:])
    qc.x(qr_b[-1])
    qc.cx(qr_b[-1], qr_z[:])
    qc.x(qr_b[-1])
    qc.append(QFT(num_qubits+1, do_swaps=False).to_gate(), qr_b[:])
    # add a
    qc.append(phi_adder(num_qubits).control(2), qr_c[:] + qr_a[:] + qr_b[:])
    qc.append(QFT(num_qubits+1, do_swaps=False).inverse().to_gate(), qr_b[:])

    return qc.to_gate()


def init_register(qc, qr, x: int):
    a = x
    for qr_i in qr:
        if a & 1 == 1:
            qc.x(qr_i)
        a >>= 1
