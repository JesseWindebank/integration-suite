import xml.etree.ElementTree as ET
from extract.endpoints.extract_sage_intacct import extract_departments


def transform_departments():
    xml_response = extract_departments()

    # Parse the XML response
    root = ET.fromstring(xml_response)

    # Initialize a list to store extracted data
    departments_data = []

    # Iterate over 'department' elements and extract the required fields
    for department in root.findall(".//department"):
        department_id = department.find("DEPARTMENTID").text
        record_no = department.find("RECORDNO").text
        title = department.find("TITLE").text

        department_data = {
            "DEPARTMENTID": department_id,
            "RECORDNO": record_no,
            "TITLE": title
        }

        departments_data.append(department_data)

    # Print the extracted data
    print(departments_data)

    return departments_data
