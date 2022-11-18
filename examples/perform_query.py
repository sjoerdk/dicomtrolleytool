from dicomtrolley.core import Query, QueryLevels

from dicomtrolleytool.persistence import KeyRingStorage


storage = KeyRingStorage()
searcher = storage.load_channel("VNA_MINT").init_searcher()

study = searcher.find_study(
    query=Query(
        StudyInstanceUID="12345678",
        include_fields=["AccessionNumber", "StudyDescription", "SeriesDescription"],
        query_level=QueryLevels.SERIES,
    )
)

print(study.data)
