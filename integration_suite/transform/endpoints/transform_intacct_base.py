import xml.etree.ElementTree as ET
from extract.endpoints.extract_intacct_base import extract_departments


def parse_department_element(department):
    department_id = department.find("DEPARTMENTID").text
    record_no = department.find("RECORDNO").text
    title = department.find("TITLE").text

    return {
        "DEPARTMENTID": department_id,
        "RECORDNO": record_no,
        "TITLE": title
    }


def transform_departments():
    xml_response = extract_departments()
    root = ET.fromstring(xml_response)

    departments = root.findall(".//department")
    departments_data = [parse_department_element(
        department) for department in departments]

    return departments_data
