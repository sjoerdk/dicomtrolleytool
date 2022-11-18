from dicomtrolley.core import Query, QueryLevels

from dicomtrolleytool.persistence import KeyRingStorage

storage = KeyRingStorage()
searcher = storage.load_channel(key="DICOMQRConnection").init_searcher()

print("Perform a search")

studies = searcher.find_studies(
    Query(
        PatientName="ABA*",
        query_level=QueryLevels.STUDY,
    )
)

print(f"Found {len(studies)} studies")
