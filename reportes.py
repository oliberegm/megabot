from datetime import datetime
import time
from prettytable import PrettyTable

from pocketoptionapi.global_value import result
from src.repository.operation_record import OperationRecorder

db = OperationRecorder()

init_time = datetime.now()

while True:
    results_by_asset = db.result_by_asset(init_time, datetime.now())
    # Crear una tabla usando PrettyTable
    table = PrettyTable()
    table.field_names = ["Asset Name", "Total Result"]

    # Llenar la tabla con los resultados por asset_name
    for asset_name, total_result in results_by_asset.items():
        table.add_row([asset_name, total_result])

    # Limpiar la consola y mostrar la tabla
    print("\033[H\033[J")  # Esto limpia la consola
    print(f"Reporte generado el: {datetime.now()}\n")
    print(table)

    # Esperar un minuto antes de volver a generar el reporte
    time.sleep(60)