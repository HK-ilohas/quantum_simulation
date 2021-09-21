def init_register(qc, qr, x: int):
    a = x
    for qr_i in qr:
        if a & 1 == 1:
            qc.x(qr_i)
        a >>= 1
