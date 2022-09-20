from dicomtrolleytool.connections import MintConnection
from dicomtrolleytool.persistence import KeyRingStorage

from dicomtrolley.core import Query, QueryLevels

storage = KeyRingStorage()
searcher = MintConnection.init_from_storage(storage, "Connection1").init_searcher()


study = searcher.find_study(
    query=Query(
        StudyInstanceUID="12345678",
        include_fields=["AccessionNumber", "StudyDescription", "SeriesDescription"],
        query_level=QueryLevels.SERIES,
    )
)


print(study.data)
