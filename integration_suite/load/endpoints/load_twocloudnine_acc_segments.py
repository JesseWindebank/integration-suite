from typing import List, Dict
from transform.endpoints.transform_intacct_base import transform_departments
from auth.endpoints.auth_twocloudnine_payroll import get_sf_connection


def get_record_type_id(sf, record_type_name) -> str:
    query = (
        "SELECT Id FROM RecordType WHERE SobjectType = 'tc9_bgl__Acc_Segments__c'"
        f" AND DeveloperName = '{record_type_name}'"
    )
    result = sf.query(query)['records'][0]['Id']
    return result


def get_accounting_system_id(sf) -> str:
    query = "SELECT Id FROM tc9_bgl__Acc_System_Setup__c WHERE Name = 'Default'"
    result = sf.query(query)['records'][0]['Id']
    return result


def prepare_department_data(department: Dict[str, str], record_type_id: str, accounting_system_id: str) -> Dict[str, str]:
    data = {
        "tc9_bgl__External_ID__c": f"{department['RECORDNO']}D",
        "Name": department['DEPARTMENTID'],
        "RecordTypeId": record_type_id,
        "tc9_bgl__Accounting_System_Reference__c": department['DEPARTMENTID'],
        "tc9_bgl__Accounting_System__c": accounting_system_id,
        "tc9_bgl__Active_Inactive__c": True,
        "tc9_bgl__Segment_Description__c": department['TITLE']
    }
    return data


def upsert_departments(sf, departments_data: List[Dict[str, str]]) -> None:
    record_type_id = get_record_type_id(sf, 'Assignment_Department')
    accounting_system_id = get_accounting_system_id(sf)

    upsert_data = [
        prepare_department_data(
            department, record_type_id, accounting_system_id)
        for department in departments_data
    ]
    print(f'load department - total count: {len(upsert_data)}')
    results = sf.bulk.__getattr__('tc9_bgl__Acc_Segments__c').upsert(
        upsert_data, 'tc9_bgl__External_ID__c'
    )

    success_count = 0
    failure_count = 0

    for result in results:
        if result['success']:
            success_count += 1
        else:
            failure_count += 1

    print(f'load department - success count: {success_count}')
    print(f'load department - failure count: {failure_count}')


def load_departments() -> None:
    departments_data = transform_departments()
    sf = get_sf_connection()
    upsert_departments(sf, departments_data)
