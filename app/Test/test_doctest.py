import doctest

def calcular_cuota_prestamo(monto, meses):
    """
    Calcula la cuota mensual simple.
    >>> calcular_cuota_prestamo(1000, 10)
    100.0
    """
    return float(monto / meses)

if __name__ == "__main__":
    doctest.testmod(verbose=True)
