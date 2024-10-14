import logging
from datetime import datetime

from tinydb import TinyDB, Query

logger = logging.getLogger(__name__)


class OperationRecorder:
    def __init__(self):
        # Se inicializa la base de datos TinyDB
        self.db = TinyDB('db_operations.json')
        self.operations_table = self.db.table('operations')

    def record_operation(self, asset_name: str, id_operation: str, direction: str, amount: float, result: float, timestamp: int):
        """
        Registra una operación en la base de datos.

        :param asset_name: Nombre del activo en la operación.
        :param id_operation: Id de la operacion en iqOption
        :param direction: Dirección de la operación ('buy' o 'sell').
        :param amount: Monto de la operación.
        :param result: Resultado de la operación ('win' o 'lose').
        :param timestamp: Tiempo (epoch) de la operación.
        """
        operation = {
            'asset_name': asset_name,
            'id_operation': id_operation,
            'direction': direction,
            'amount': amount,
            'result': result,
            'timestamp': timestamp
        }
        self.operations_table.insert(operation)

    def get_operations(self):
        """
        Obtiene todas las operaciones registradas.

        :return: Lista de todas las operaciones.
        """
        return self.operations_table.all()

    def get_operations_by_asset(self, asset_name: str):
        """
        Obtiene todas las operaciones relacionadas con un activo específico.

        :param asset_name: Nombre del activo.
        :return: Lista de operaciones para el activo especificado.
        """
        query = Query()
        return self.operations_table.search(query.asset_name == asset_name)

    def get_win_rate(self):
        """
        Calcula la tasa de éxito (win rate) basada en las operaciones registradas.

        :return: Tasa de éxito como porcentaje.
        """
        wins = self.operations_table.count(Query().result == 'win')
        total = self.operations_table.count(Query().result.exists())

        if total == 0:
            return 0.0
        return (wins / total) * 100

    def delete_all_operations(self):
        """
        Elimina todas las operaciones registradas.
        """
        self.operations_table.truncate()
        logger.info("All operations have been deleted.")

    def get_operation_by_id_operation(self, id_operation):
        """
        Obtiene la operación de un activo por el id de la operación.

        :param id_operation: ID de la operación.
        :return: Registro de la operación.
        """
        query = Query()
        return self.operations_table.search(query['id_operation'] == id_operation)

    def get_operations_by_asset_with_no_result(self, asset_name: str):
        """
        Obtiene todas las operaciones para un activo específico donde el resultado ('result') es None.

        :param asset_name: Nombre del activo.
        :return: Lista de operaciones con result=None para el activo especificado.
        """
        query = Query()
        return self.operations_table.search((query.asset_name == asset_name) & (query.result is None))

    def get_total_results_in_range(self, start_date: datetime, end_date: datetime):
        """
        Obtiene la suma total de los resultados en un rango de fechas.

        :param start_date: Fecha de inicio del rango.
        :param end_date: Fecha de fin del rango.
        :return: Suma total de los resultados en el rango de fechas.
        """
        # Convertir las fechas a timestamps (segundos desde el epoch)
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())

        # Consultar la base de datos para obtener las operaciones en ese rango
        query = Query()
        operations_in_range = self.operations_table.search(
            (query.timestamp >= start_timestamp) & (query.timestamp <= end_timestamp)
        )

        # Sumar todos los resultados
        total_results = sum(operation['result'] - operation['amount'] for operation in operations_in_range)

        return total_results

    def get_total_results(self):
        """
        Obtiene la suma total de los resultados de todas las operaciones almacenadas.

        :return: Suma total de los resultados.
        """
        # Obtener todas las operaciones de la base de datos
        all_operations = self.db.all()

        # Sumar todos los resultados
        total_results = sum(operation['result'] for operation in all_operations)

        return total_results

    def update_result_by_id_operation(self, id_operation, result):
        """
        Actualiza el campo 'result' de una operación basada en su id_operation.

        :param id_operation: ID de la operación a actualizar.
        :param result: Nuevo valor para el campo 'result'.
        :return: True si la operación fue exitosa, False si no se encontró la operación.
        """
        query = Query()
        updated = self.operations_table.update({'result': result}, query['id_operation'] == id_operation)

        return bool(updated)  # Retorna True si se actualizó algún registro, False si no

    def result_by_asset(self, start_date: datetime, end_date: datetime) -> dict:
        # Convertir las fechas a timestamps (segundos desde el epoch)
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        query = Query()
        all_operations = self.operations_table.search(
            (query.timestamp >= start_timestamp) & (query.timestamp <= end_timestamp)
        )

        # Crear un diccionario para almacenar los resultados por asset_name
        results_by_asset = {}

        # Recorrer todas las operaciones y sumar resultados por asset_name
        for operation in all_operations:
            asset_name = operation['asset_name']
            result = operation['result'] - operation['amount']

            if asset_name not in results_by_asset:
                results_by_asset[asset_name] = 0
            results_by_asset[asset_name] += result

        return results_by_asset
