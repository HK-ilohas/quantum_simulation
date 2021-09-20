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


def phi_cc_adder_modulo(num_qubits: int):
    # define qubits
    qr_c = QuantumRegister(2, "c")  # control
    qr_a = QuantumRegister(num_qubits, "a")
    qr_b = QuantumRegister(num_qubits + 1, "b")  # avoid to overflow
    qr_n = QuantumRegister(num_qubits, "n")
    qr_z = QuantumRegister(1, "z")  # zero
    qr_list = [qr_c, qr_a, qr_b, qr_n, qr_z]

    # define circuit
    qc = QuantumCircuit(*qr_list, name="phi_cc_adder_modulo")

    # a + b
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

    return qc.to_gate()


def cmult_mod(num_qubits: int, a: int):
    # define qubits
    qr_c = QuantumRegister(1, "c")  # control
    qr_x = QuantumRegister(num_qubits, "x")
    qr_a = QuantumRegister(num_qubits, "a")
    qr_z1 = QuantumRegister(num_qubits - 1, "z1")  # for bit shift
    qr_b = QuantumRegister(2 * num_qubits, "b")  # for overflow
    qr_n = QuantumRegister(2 * num_qubits - 1, "n")  # modulo
    qr_z2 = QuantumRegister(1, "z2")  # for adder modulo
    qr_list = [qr_c, qr_x, qr_a, qr_z1, qr_b, qr_n, qr_z2]
    # define circuit
    qc = QuantumCircuit(*qr_list, name="cmult_mod")

    qc.append(QFT(2 * num_qubits, do_swaps=False).to_gate(), qr_b[:])

    for i in range(num_qubits):
        qr_cc_adder_modulo = qr_c[:] + qr_x[i:i+1] + qr_z1[:i] + qr_a[:] + qr_z1[i:] + qr_b[:] + qr_n[:] + qr_z2[:]
        qc.append(phi_cc_adder_modulo(2 * num_qubits - 1), qr_cc_adder_modulo)

    qc.append(QFT(2 * num_qubits, do_swaps=False).inverse().to_gate(), qr_b[:])

    return qc.to_gate()


def cmult_mod_inv(num_qubits: int):
    # define qubits
    qr_c = QuantumRegister(1, "c")  # control
    qr_x = QuantumRegister(num_qubits, "x")  # can't use higher bits than 2^num_qubits
    qr_a = QuantumRegister(num_qubits, "a")
    qr_z1 = QuantumRegister(num_qubits - 1, "z1")  # for bit shift
    qr_b = QuantumRegister(2 * num_qubits, "b")  # for overflow
    qr_n = QuantumRegister(2 * num_qubits - 1, "n")  # modulo
    qr_z2 = QuantumRegister(1, "z2")  # for adder modulo
    qr_list = [qr_c, qr_x, qr_a, qr_z1, qr_b, qr_n, qr_z2]
    # define circuit
    qc = QuantumCircuit(*qr_list, name="cmult_mod")

    qc.append(QFT(2 * num_qubits, do_swaps=False).to_gate(), qr_b[:])

    for i in range(num_qubits - 1, -1, -1):
        qr_cc_adder_modulo = qr_c[:] + qr_x[i:i+1] + qr_z1[:i] + qr_a[:] + qr_z1[i:] + qr_b[:] + qr_n[:] + qr_z2[:]
        qc.append(phi_cc_adder_modulo(2 * num_qubits - 1).inverse(), qr_cc_adder_modulo)

    qc.append(QFT(2 * num_qubits, do_swaps=False).inverse().to_gate(), qr_b[:])

    return qc.to_gate()


def init_register(qc, qr, x: int):
    a = x
    for qr_i in qr:
        if a & 1 == 1:
            qc.x(qr_i)
        a >>= 1
