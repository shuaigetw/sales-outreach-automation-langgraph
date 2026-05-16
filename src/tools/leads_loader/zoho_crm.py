import os
import requests
from .lead_loader_base import LeadLoaderBase

class ZohoLeadLoader(LeadLoaderBase):
    def __init__(self, access_token=None, api_domain=None):
        self.access_token = access_token or os.getenv("ZOHO_ACCESS_TOKEN")
        self.api_domain = api_domain or os.getenv("ZOHO_API_DOMAIN", "https://www.zohoapis.com")
        self.headers = {
            "Authorization": f"Zoho-oauthtoken {self.access_token}",
            "Content-Type": "application/json"
        }

    def fetch_records(self, lead_ids=None, status_filter="NEW"):
        """
        Fetches leads from Zoho CRM.
        """
        if lead_ids:
            leads = []
            for lead_id in lead_ids:
                url = f"{self.api_domain}/crm/v3/Leads/{lead_id}"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    data = response.json().get("data", [])
                    if data:
                        record = data[0]
                        leads.append({
                            "id": record.get("id"),
                            "First_Name": record.get("First_Name", ""),
                            "Last_Name": record.get("Last_Name", ""),
                            "Email": record.get("Email", ""),
                            "Phone": record.get("Phone", ""),
                            "Mailing_Street": record.get("Street", ""),
                            "Company": record.get("Company", "")
                        })
            return leads
        else:
            # 為了測試方便，我們暫時移除嚴格的 "NEW" 狀態過濾
            # 直接抓取系統中最新建立的 2 筆客戶 (Contacts)
            url = f"{self.api_domain}/crm/v3/Contacts"
            params = {
                "fields": "First_Name,Last_Name,Email,Phone,Mailing_Street,Account_Name",
                "per_page": 50,
                "sort_order": "desc",
                "sort_by": "Created_Time"
            }
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json().get("data", [])
                normalized_leads = []
                for record in data:
                    normalized_leads.append({
                        "id": record.get("id"),
                        "First_Name": record.get("First_Name", ""),
                        "Last_Name": record.get("Last_Name", ""),
                        "Email": record.get("Email", ""),
                        "Phone": record.get("Phone", ""),
                        "Mailing_Street": record.get("Mailing_Street", record.get("Street", "")),
                        "Company": record.get("Account_Name", {}).get("name", "") if isinstance(record.get("Account_Name"), dict) else record.get("Account_Name", "")
                    })
                return normalized_leads
            elif response.status_code == 204:
                # No Content
                return []
            else:
                print(f"Error fetching Zoho leads: {response.text}")
                return []

    def update_record(self, lead_id, updates: dict):
        """
        Updates a lead record in Zoho CRM.
        """
        url = f"{self.api_domain}/crm/v3/Leads/{lead_id}"
        
        zoho_updates = {}
        if "Status" in updates:
            zoho_updates["Lead_Status"] = updates["Status"]
        if "Outreach Report" in updates:
            # Storing the outreach report link in Description, 
            # or it could be mapped to a custom field in Zoho
            zoho_updates["Description"] = f"Outreach Report: {updates['Outreach Report']}"
            
        payload = {
            "data": [
                zoho_updates
            ]
        }
        
        response = requests.put(url, headers=self.headers, json=payload)
        if response.status_code in [200, 201, 202, 204]:
            return response.json()
        else:
            print(f"Error updating Zoho lead {lead_id}: {response.text}")
            return None
