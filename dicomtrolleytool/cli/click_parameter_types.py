"""Custom click parameter types"""
from click import ParamType
from pydicom.datadict import tag_for_keyword


class DICOMTagNameListParamType(ParamType):
    """One or more comma-seperated DICOM keywords in CamelCase"""

    name = "dicom_tag_name_list"

    def convert(self, value, param, ctx):
        """Check whether each keyword passed is a valid DICOM tag names
        like PatientID, AccessionNumber, etc.

        Returns
        -------
        List[str]
            A list of valid DICOM tag names

        """
        if not value:
            return []  # [] is default value if parameter not given

        if type(value) is not str:
            self.fail(
                f"Expected string input but found {type(value)} " f"value:'{value}'"
            )

        keywords = value.split(",")
        for keyword in keywords:
            if keyword == "":
                raise ValueError(
                    "Empty DICOM keyword in list. Do you have a " "trailing comma?"
                )
            if not tag_for_keyword(keyword):
                raise ValueError(
                    f"{keyword} is not a valid DICOM tag name. " f"Format: CamelCase"
                )

        return keywords

    def __repr__(self):
        return "DICOM_TAG_NAME_LIST"
