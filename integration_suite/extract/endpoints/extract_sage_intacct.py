import requests
from auth.endpoints.auth_sage_intacct import get_credentials
from datetime import datetime
import uuid

# get credentials object
credentials = get_credentials('Sage Intacct', 'Intacct (DFP) - Sandbox')


def extract_departments():

    url = "https://api.intacct.com/ia/xml/xmlgw.phtml"

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
                                        <object>DEPARTMENT</object>
                                        <fields>DEPARTMENTID,RECORDNO,TITLE</fields>
                                        <query/>
                                        <pagesize>100</pagesize>
                                    </readByQuery>
                                </function>
                            </content>
                        </operation>
                    </request>"""

    headers = {
        'Content-Type': 'application/xml',
        'Cookie': 'DFT_LOCALE=en_AU.UTF-8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


print(extract_departments())

# def extract_locations():
#     """Extract locations from Sage Intacct"""
#     return extract_records('locations')


# def extract_locationEntities():
#     """Extract location entities from Sage Intacct"""
#     return extract_records('locationEntities')


# def extract_glAccounts():
#     """Extract GL accounts from Sage Intacct"""
#     return extract_records('glAccounts')


# def extract_projects():
#     """Extract projects from Sage Intacct"""
#     return extract_records('projects')
