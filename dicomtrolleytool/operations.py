"""For working with ListComb lib"""
from lico.lico import Operation


class StudyInstanceUIDQuery(Operation):
    """Query a DICOM server and extract"""

    def __init__(self, id_column: str, server_func):
        self.id_column = id_column
        self.server_func = server_func

    def apply(self, row):
        id_value = row[self.id_column]
        return {"server_result": self.server_func(id_value)}
