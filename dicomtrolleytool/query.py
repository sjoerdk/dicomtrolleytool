"""Classes and functions for working with and displaying queries, query results"""
from typing import Iterable, List, Tuple, Union

from dicomtrolley.core import Query, Study
from dicomtrolley.exceptions import DICOMTrolleyError
from dicomtrolley.trolley import Trolley


class QueryResult:
    def __init__(self, content: Union[Study, Exception], query: Query):
        """The result of running a query. Can be error or data coming back from
        server
        """

        self.content = content
        self.query = query

    def is_error(self):
        return isinstance(self, QueryErrorResult)

    def __str__(self):
        return f"QueryResult {self.content}"


class QueryErrorResult(QueryResult):
    def __init__(self, content: Exception, query: Query):
        super().__init__(content=content, query=query)


class QueryStudyResult(QueryResult):
    def __init__(self, content: Study, query: Query):
        # Typing needed to convince mypy content is not Union[Exception,Any]. Why?
        self.content: Study
        super().__init__(content=content, query=query)


def split_error_results(
    results: Iterable[QueryResult],
) -> Tuple[List[QueryStudyResult], List[QueryErrorResult]]:
    study_results = [x for x in results if isinstance(x, QueryStudyResult)]
    error_results = [x for x in results if isinstance(x, QueryErrorResult)]
    return study_results, error_results


def collect_query_results(
    trolley: Trolley, queries: Iterable[Query]
) -> List[QueryResult]:
    """Run all queries and collect results"""
    results: List[QueryResult] = []
    for query in queries:
        try:
            results.append(
                QueryStudyResult(content=trolley.find_study(query), query=query)
            )
        except DICOMTrolleyError as e:
            results.append(QueryErrorResult(content=e, query=query))

    return results
