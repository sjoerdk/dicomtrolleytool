"""Classes and functions for working with and displaying queries, query results"""
from enum import Enum
from typing import Iterable, List, Optional, Union

from dicomtrolley.core import Query, Study
from dicomtrolley.exceptions import DICOMTrolleyError
from dicomtrolley.trolley import Trolley


class QueryResult:
    def __init__(self, content: Union[Study, Exception], query: Optional[Query] = None):
        self.content = content
        self.query = query

    def is_error(self):
        return isinstance(self.content, Exception)

    def __str__(self):
        return f"QueryResult {self.content}"


def collect_query_results(
    trolley: Trolley, queries: Iterable[Query]
) -> (List)[QueryResult]:
    """Run all queries and collect results"""
    results = []
    for query in queries:
        try:
            results.append(QueryResult(content=trolley.find_study(query), query=query))
        except DICOMTrolleyError as e:
            results.append(QueryResult(content=e, query=query))

    return results


class ResultFormat(Enum):
    """How to display query results"""

    RAW = "RAW"
    TABLE = "TABLE"
    CSV = "CSV"


class FormatLevel(str, Enum):
    """Display only study-level info, or deeper into study and instance?"""

    STUDY = "STUDY"
    SERIES = "SERIES"
    INSTANCE = "INSTANCE"
