import json
import os
import random
from datetime import datetime
from pathlib import Path


def cargar_tasas(ruta: str) -> dict:
    """Carga las tasas desde un archivo JSON."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def convertir(precio_usd: float, moneda_destino: str, tasas: dict) -> float:
    """Convierte un precio en USD a la moneda destino usando las tasas."""
    try:
        tasa = tasas["USD"][moneda_destino]
    except KeyError:
        raise ValueError(f"Moneda no soportada: {moneda_destino}")
    # 🔹 Redondear el resultado final a 2 decimales
    return round(precio_usd * float(tasa), 2)


def registrar_transaccion(producto: str, precio_convertido: float, moneda: str, ruta_log: str) -> None:
    """Registra la transacción en un archivo de log (crea la carpeta si no existe)."""
    Path(os.path.dirname(ruta_log) or ".").mkdir(parents=True, exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ruta_log, "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha} | {producto}: {precio_convertido:.2f} {moneda}\n")


def actualizar_tasas(ruta: str) -> None:
    """Simula una API: ajusta las tasas aleatoriamente ±2% y actualiza la fecha."""
    with open(ruta, "r+", encoding="utf-8") as archivo:
        tasas = json.load(archivo)

        for moneda, valor in list(tasas.get("USD", {}).items()):
            # Factor entre 0.98 y 1.02
            factor = 0.98 + (0.04 * random.random())
            # 🔹 Redondear las tasas a 2 decimales antes de guardarlas
            tasas["USD"][moneda] = round(float(valor) * factor, 2)

        tasas["actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        archivo.seek(0)
        json.dump(tasas, archivo, indent=2, ensure_ascii=False)
        archivo.truncate()


# Ejemplo de uso
if __name__ == "__main__":
    # Actualizar las tasas
    actualizar_tasas("data/tasas.json")
    tasas = cargar_tasas("data/tasas.json")
    precio_usd = 100.00

    precio_eur = convertir(precio_usd, "EUR", tasas)
    registrar_transaccion("Laptop", precio_eur, "EUR", "logs/historial.txt")

    print(f"Precio en EUR: {precio_eur:.2f}")
