from transform.endpoints.transform_sage_intacct import transform_departments
from auth.endpoints.auth_twocloudnine_payroll import CloudNinePayrollSalesforceConnection


def load_departments():
    departments_data = transform_departments()

    # Define the external ID field name
    external_id_field = 'Your_External_Id_Field__c'

    # Get a Salesforce connection object
    sf = CloudNinePayrollSalesforceConnection().get_connection()

    # Iterate through the departments_data list and upsert each record
    for department in departments_data:
        try:
            result = sf.YourCustomObjectName__c.upsert(
                external_id_field + '/' + department['DEPARTMENTID'], department)
            print(f"Upsert result: {result}")
        except Exception as e:
            print(
                f"An error occurred while upserting record {department['DEPARTMENTID']}: {e}")
