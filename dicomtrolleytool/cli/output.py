"""Functions and classes for formatting output to console"""
from collections import defaultdict
from enum import Enum
from typing import Dict, Iterable, List, Optional

from dicomtrolley.core import Study
from dicomtrolley.exceptions import DICOMTrolleyError

from pydicom import Dataset
from tabulate import tabulate

from dicomtrolleytool.exceptions import TrolleyToolError
from dicomtrolleytool.logs import get_module_logger
from dicomtrolleytool.query import QueryResult, QueryStudyResult, split_error_results

logger = get_module_logger("cli_output")


class ResultFormat(str, Enum):
    """How to display query results"""

    RAW = "RAW"
    TABLE = "TABLE"
    GITHUB = "GITHUB"  # github markup table
    CSV = "CSV"


class FormatLevel(str, Enum):
    """Which types of DICOM object results do you want to show in output?

    Typically, this should always match QueryLevel. You just display information
    on the deepest level you can find. It feels better to have a separate enum
    though.
    """

    STUDY = "STUDY"
    SERIES = "SERIES"
    INSTANCE = "INSTANCE"


def format_query_results(
    results=Iterable[QueryResult],
    output_format: ResultFormat = ResultFormat.RAW,
    output_field_filter: Optional[List[str]] = None,
) -> str:
    """Turn query results into something you can print to console

    Parameters
    ----------
    results:
        For each query either the data sent by the server or the error that occurred
    output_format:
        One of ResultFormat. How to display the results
    output_field_filter:
        Optionally only show these DICOM tag names in results. Defaults to None
        which show all fields without filter

    Returns
    -------
    A string, potentially containing newlines and tabs

    """

    logger.debug(f"Formatting query results as {output_format}")
    if output_format == ResultFormat.RAW:
        return format_query_results_raw(results, output_field_filter)
    elif output_format == ResultFormat.TABLE:
        return format_query_results_table(results, output_field_filter)
    elif output_format == ResultFormat.GITHUB:
        return format_query_results_table(
            results, output_field_filter, table_format="github"
        )
    elif output_format == ResultFormat.CSV:
        return format_query_results_csv(results, output_field_filter)
    else:
        raise TrolleyToolError(f"Unknown result format {output_format}")


def format_query_results_raw(
    results: Iterable[QueryResult], output_field_filter: Optional[List[str]] = None
) -> str:
    """Print each result as plainly as possible. Still use indentation for
    series and images to keep things remotely readable
    """
    if output_field_filter:
        raise NotImplementedError(
            "Raw output filtering not implemented."
            "Just use grep. Or implement it yourself if "
            "you are annoyed by this"
        )
    output = []
    tab = "  "
    for idx, result in enumerate(results, start=1):
        output.append(f"= Query {idx} =")
        output.append(result.query.to_short_string())
        if result.is_error():
            output.append(f"Error. No Results found. Error: {str(result.content)}")
        else:
            output.append(f"= Result for query {idx} =")
            study: Study = result.content
            output.append(f"Study: {study.uid}")
            output = output + (format_dataset(study.data, prefix=tab))

            for series in study.series:
                output.append(f"{tab}Series: {series.uid}")
                output = output + (format_dataset(series.data, prefix=tab + tab))
                for instance in series.instances:
                    output.append(f"{tab + tab} Instance: {instance.uid}")
                    output = output + (
                        format_dataset(instance.data, prefix=tab + tab + tab)
                    )

    return "\n".join(output)


def format_dataset(ds: Dataset, prefix="") -> List[str]:
    """Extract all elements in dataset as separate lines, optionally prefixed"""
    return [f"{prefix}{line}" for line in str(ds).split("\n")]


def guess_format_level(results: List[QueryStudyResult]) -> str:
    """Determine the appropriate DICOM object level to display these results at
    by seeing whether there is Series and Instance information in these results

    Returns
    -------
    str
        One of the values of enum FormatLevel

    Raises
    ------
    ValueError
        If studies is empty. This function makes no sense for empty input

    DICOMTrolleyError
        If studies have inconsistent object depth. For example one study
        with only study-level info and another with instance-level info.
        It is not clear how to display such disparate series in a table
        so an error is raised.

    """
    level_per_result = set()
    if not results:
        raise ValueError("Studies was empty. Cannot guess format level")

    for study in [x.content for x in results]:
        if study.series:
            if study.series[0].instances:
                level_per_result.add(FormatLevel.INSTANCE)
            else:
                level_per_result.add(FormatLevel.SERIES)
        else:
            level_per_result.add(FormatLevel.STUDY)

    if len(level_per_result) > 1:
        raise DICOMTrolleyError(
            f"To display properly, studies should have consistent object levels "
            f"(whether they contain series and/or image information). "
            f"Found {level_per_result}"
        )

    else:
        result = level_per_result.pop()
        logger.debug(
            f"Guessing format_level of {result} based on content "
            f"of {len(results)} results"
        )
        return result


def query_results_to_table(  # noqa: C901  - I feel its acceptably complex for now
    results=Iterable[QueryStudyResult],
    output_field_filter: Optional[List[str]] = None,
    format_level: Optional[str] = None,
) -> Dict[str, List[str]]:
    """Take all format level information from results and put it in a
    {header1: [val1,val2,val3,...], header2: etc. } dictionary.
    Pre-processing step for printing as table or csv

    Notes
    -----
    Results contain DICOM objects (study->series->instances) which are in a
    tree datastructure. In order to shoehorn a tree into a 2D table for output
    the most detailed object level is taken to comprise the rows. Higher level
    information is then duplicated on every row.
    For example, for a series-level display, information for each series is
    put on a separate row, and patient-level information such as 'SeriesDescription'
    is repeated on each row.

    The leading consideration is to make the output easy to grep so that a single
    line contains all information you need.
    """
    if not format_level:
        format_level = guess_format_level(results)

    # first extract all data elements at the right level
    elements: List[Dict[str, str]] = []  # one dict per result
    studies = [x.content for x in results]
    if format_level == FormatLevel.STUDY:
        for study in studies:
            result_values = {"StudyInstanceUID": study.uid}
            result_values.update(dataset_to_dict(study.data))
            elements.append(result_values)

    if format_level == FormatLevel.SERIES:
        for study in studies:
            study_level_values = dataset_to_dict(study.data)
            for series in study.series:
                result_values = study_level_values.copy()
                result_values.update(dataset_to_dict(series.data))
                elements.append(result_values)

    if format_level == FormatLevel.INSTANCE:
        for study in studies:
            study_level_values = dataset_to_dict(study.data)
            for series in study.series:
                series_level_values = dataset_to_dict(series.data)
                for instance in series.instances:
                    result_values = study_level_values.copy()
                    result_values.update(series_level_values)
                    result_values.update(dataset_to_dict(instance.data))
                    elements.append(result_values)

    # then make sure that any missing data elements are filled in as empty
    all_headers = set()
    for x in elements:
        all_headers.update(list(x.keys()))
    table = defaultdict(list)
    for result_values in elements:
        all_items = {x: "" for x in all_headers}
        all_items.update(result_values)
        for key, value in all_items.items():
            table[key].append(value)

    if output_field_filter:
        logger.debug(
            f"Output field filter was given, filtering by " f"{output_field_filter}"
        )
        filtered = {x: y for x, y in table.items() if x in output_field_filter}
        return filtered
    else:
        return table


def dataset_to_dict(ds: Dataset) -> Dict[str, str]:
    """All elements of dataset as {Keyword: Value}"""
    return {x.keyword: x.value for x in ds}


def format_query_results_table(
    results: Iterable[QueryResult],
    output_field_filter: Optional[List[str]] = None,
    format_level: Optional[FormatLevel] = None,
    table_format: str = "simple",
) -> str:
    """Create"""
    study_results, error_results = split_error_results(results)
    table = query_results_to_table(
        study_results,
        output_field_filter=output_field_filter,
        format_level=format_level,
    )
    if error_results:
        logger.warning(
            f"{len(error_results)} queries resulted in error. Excluding those "
            f"from table"
        )
    # disable_numparse to prevent messing up accession numbers
    return tabulate(table, headers="keys", tablefmt=table_format, disable_numparse=True)


def format_query_results_csv(
    results: Iterable[QueryResult], output_field_filter
) -> str:
    raise NotImplementedError()
