from celery import shared_task
from home.models import Integration, Integration_Account
import requests
import json
import os

@shared_task
def pull_data_from_active_resources_scheduled():
    all_integrations = Integration.objects.all()
    seen_sources = []
    all_data = []

    for integration in all_integrations:
        if integration.source.link not in seen_sources:
            url = integration.source.link
            headers = {
                'X-Metabase-Session': '7ff69bc5-0d55-4216-b643-6cb992a249d0',
                'Content-Type': 'application/json'
            }
            try:
                response = requests.post(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                #adding login, password, script, and .apk file:
                for record in data:
                    customer = record['customer_customer - customer_id → name']
                    driver_id = record['asset_assignment - assignment_id → driver1_id']
                    del record['customer_customer - customer_id → name']
                    del record['asset_assignment - assignment_id → driver1_id']
                    try:
                        customer_integration = Integration.objects.filter(customer=customer).first()
                        record['script'] = customer_integration.sh_script
                        record['apk_file'] = customer_integration.apk_file
                        customer_driver_account = Integration_Account.objects.filter(integration__pk=customer_integration.pk, pk=driver_id).first()
                        if customer_driver_account:
                            record['login'] = customer_driver_account.login
                            record['password'] = customer_driver_account.password
                    except:
                        pass
                seen_sources.append(integration.source.link)
                all_data.append(data)
            except requests.RequestException as e:
                print(f"An error occurred: {e}")

    with open('../Executoner/data/new_data.json', 'w') as file:
        json.dump(all_data, file, indent=4)

    print("Data has been successfully saved to new_data.json.")

