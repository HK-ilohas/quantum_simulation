# Quantum Simulation

Qiskit を用いた，卒業研究用の量子シミュレーションコード．

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Quantum Simulation](#quantum-simulation)
  - [utils.py](#utilspy)
    - [`init_register` (`qc`, `qr`, `x`)](#init_register-qc-qr-x)
  - [arithmetic_circuit.py](#arithmetic_circuitpy)
    - [`phi_adder` (`num_qubits`)](#phi_adder-num_qubits)
    - [`phi_cc_adder_modulo` (`num_qubits`)](#phi_cc_adder_modulo-num_qubits)
    - [`cmult_mod` (`num_qubits`, `a`, `n`)](#cmult_mod-num_qubits-a-n)
    - [`cmult_mod_inv` (`num_qubits`, `a_inv`, `n`)](#cmult_mod_inv-num_qubits-a_inv-n)
    - [`c_Ua` (`num_qubits`, `a`, `n`)](#c_ua-num_qubits-a-n)
    - [参考文献](#参考文献)

<!-- /code_chunk_output -->

## utils.py

### `init_register` (`qc`, `qr`, `x`)

レジスタに値をセットする関数．

| 引数 | 説明 |
| ---- | ---- |
| `qc` | QuantumCircuit |
| `qr` | QuantumRegister |
| `x` | int |

## arithmetic_circuit.py

GitHub の README では数式が使用できないので，詳しくは [[2]](#参考文献) を参照．

### `phi_adder` (`num_qubits`)

| 引数 | 説明 |
| ---- | ---- |
| `num_qubits` | `a`, `b` のビット数 |

| レジスタ | ビット数 |
| ---- | ---- |
| `qr_a` | `num_qubits` |
| `qr_b` | `num_qubits` |
| `qr_z` | 1（桁上がり分）|

### `phi_cc_adder_modulo` (`num_qubits`)

| 引数 | 説明 |
| ---- | ---- |
| `num_qubits` | `a`, `N` のビット数 |

| レジスタ | ビット数 |
| ---- | ---- |
| `qr_c` | 2（コントロールビット）|
| `qr_a` | `num_qubits` |
| `qr_b` | `num_qubits` + 1（桁上がり分込み）|
| `qr_n` | `num_qubits` |
| `qr_z` | 1 |

### `cmult_mod` (`num_qubits`, `a`, `n`)

| 引数 | 説明 |
| ---- | ---- |
| `num_qubits` | `x`, `a`, `N` のビット数 |
| `a` | `a` の値 |
| `n` | `N` の値 |

| レジスタ | ビット数 |
| ---- | ---- |
| `qr_c` | 1（コントロールビット）|
| `qr_x` | `num_qubits` |
| `qr_a` | `num_qubits` （0 で初期化） |
| `qr_b` | `num_qubits` + 1（桁上がり分込み）|
| `qr_n` | `num_qubits` |
| `qr_z` | 1 |

### `cmult_mod_inv` (`num_qubits`, `a_inv`, `n`)

| 引数 | 説明 |
| ---- | ---- |
| `num_qubits` | `x`, `a`, `N` のビット数 |
| `a_inv` | `a` の inverse |
| `n` | `N` の値 |

| レジスタ | ビット数 |
| ---- | ---- |
| `qr_c` | 1（コントロールビット）|
| `qr_x` | `num_qubits` |
| `qr_a` | `num_qubits` （0 で初期化） |
| `qr_b` | `num_qubits` + 1（桁上がり分込み）|
| `qr_n` | `num_qubits` |
| `qr_z` | 1 |

### `c_Ua` (`num_qubits`, `a`, `n`)

| 引数 | 説明 |
| ---- | ---- |
| `num_qubits` | `x`, `a`, `b`, `N` のビット数 |
| `a` | `a` の値 |
| `n` | `N` の値 |

| レジスタ | ビット数 |
| ---- | ---- |
| `qr_c` | 1（コントロールビット）|
| `qr_x` | `num_qubits` |
| `qr_a` | `num_qubits` （0 で初期化）|
| `qr_b` | `num_qubits` （0 で初期化）|
| `qr_co`| 1 |
| `qr_n` | `num_qubits` |
| `qr_z` | 1 |

### 参考文献

[1] T. G. Draper, Addition on a Quantum Computer, 2000. [arXiv:quant-ph/0008033](https://arxiv.org/pdf/quant-ph/0008033.pdf)

[2] Stephane Beauregard, Circuit for Shor's algorithm using 2n+3 qubits, [arXiv:quant-ph/0205095](https://arxiv.org/abs/quant-ph/0205095)
