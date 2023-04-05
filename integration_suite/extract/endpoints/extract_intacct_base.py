import requests
from auth.endpoints.auth_sage_intacct import get_credentials
from datetime import datetime
import uuid

credentials = get_credentials('Sage Intacct', 'Intacct (DFP) - Sandbox')


def construct_payload(credentials, object_name, fields):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    guid = uuid.uuid4()

    payload = f"""<request>
                    <control>
                        <senderid>{credentials['sender_id']}</senderid>
                        <password>{credentials['sender_password']}</password>
                        <controlid>{timestamp}</controlid>
                        <uniqueid>false</uniqueid>
                        <dtdversion>3.0</dtdversion>
                        <includewhitespace>false</includewhitespace>
                    </control>
                    <operation>
                        <authentication>
                            <login>
                                <userid>{credentials['user_id']}</userid>
                                <companyid>{credentials['company_id']}</companyid>
                                <password>{credentials['user_password']}</password>
                            </login>
                        </authentication>
                        <content>
                            <function controlid="{guid}">
                                <readByQuery>
                                    <object>{object_name}</object>
                                    <fields>{fields}</fields>
                                    <query/>
                                    <pagesize>100</pagesize>
                                </readByQuery>
                            </function>
                        </content>
                    </operation>
                </request>"""
    return payload


def extract_data(object_name, fields):
    url = "https://api.intacct.com/ia/xml/xmlgw.phtml"
    payload = construct_payload(credentials, object_name, fields)
    headers = {
        'Content-Type': 'application/xml',
        'Cookie': 'DFT_LOCALE=en_AU.UTF-8'
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.text


def extract_departments():
    return extract_data('DEPARTMENT', 'DEPARTMENTID,RECORDNO,TITLE')

# def extract_locations():
#     return extract_data('locations', 'FIELDS')

# def extract_locationEntities():
#     return extract_data('locationEntities', 'FIELDS')

# def extract_glAccounts():
#     return extract_data('glAccounts', 'FIELDS')

# def extract_projects():
#     return extract_data('projects', 'FIELDS')
