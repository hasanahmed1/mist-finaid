import csv
import requests


# CONFIGURE THE BELOW CONSTANTS BEFORE RUNNING THE SCRIPT!

CSVFILEPATH = 'coupons.csv'     # Path to the csv file, ensure the file is in the same directory as this script
ENDPOINT = 'https://api2.getmistified.com/graphql'

TOKEN = 'INSERT_YOUR_TOKEN'
EXPIRATIONDATE = '2024-12-31'   # YYYY-MM-DD
MAXCODEUSAGE = 1
EVENTID = 109                   # myMIST event ID
ROLEID = 3                      # 3 is for student. 5 is for guest.




def create_coupons_from_csv(csv_file_path, graphql_endpoint, token):
    headers = {
        'Content-Type': 'application/json',
        'token': token
    }

    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            code_from_csv = row['code']
            value_from_csv = int(row['value'])
            role_from_csv = row['role']
            
            variables = {
                "code": code_from_csv,
                "value": value_from_csv,
                "role": role_from_csv
            }

            mutation = '''
                mutation createCoupon($code: String!, $value: Int!, $expirationDate: String!,
                                       $maxCodeUsage: Int!, $valuePercentage: Boolean!,
                                       $eventId: Int!, $roleId: Int!, $tenantId: Int!) {
                  createCoupon(input: {code: $code, maxCodeUsage: $maxCodeUsage,
                                        expirationDate: $expirationDate, value: $value,
                                        valuePercentage: $valuePercentage, roleId: $roleId,
                                        tenantId: $tenantId, eventId: $eventId}) {
                    coupon {
                      __typename
                      id
                      tenantId
                      eventId
                      roleId
                      status
                      code
                      maxCodeUsage
                      value
                      valuePercentage
                      expirationDate
                    }
                    __typename
                  }
                }
            '''
            
            
            variables.update({
                "maxCodeUsage": 1,
                "expirationDate": EXPIRATIONDATE,
                "valuePercentage": False,
                "eventId": EVENTID,
                "roleId": ROLEID, # 3 is for student. 5 is for guest.
                "tenantId": 1
            })

            payload = {
                "query": mutation,
                "variables": variables
            }

            response = requests.post(graphql_endpoint, json=payload, headers=headers)

            if response.status_code == 200:
                print(f"Coupon created successfully for code: {code_from_csv}")
            else:
                print(f"Failed to create coupon for code: {code_from_csv}, Status code: {response.status_code}")

create_coupons_from_csv(CSVFILEPATH, ENDPOINT, TOKEN)
