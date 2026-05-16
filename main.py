import os
from dotenv import load_dotenv
from src.graph import OutReachAutomation
from src.state import *
from src.tools.leads_loader.zoho_crm import ZohoLeadLoader

# Load environment variables from a .env file
load_dotenv()

if __name__ == "__main__":
    # Use Zoho CRM for accessing your leads list
    lead_loader = ZohoLeadLoader(
        access_token=os.getenv("ZOHO_ACCESS_TOKEN"),
        api_domain=os.getenv("ZOHO_API_DOMAIN")
    )
    
    # Use Airtable for accessing your leads list
    # from src.tools.leads_loader.airtable import AirtableLeadLoader
    # lead_loader = AirtableLeadLoader(
    #     access_token=os.getenv("AIRTABLE_ACCESS_TOKEN"),
    #     base_id=os.getenv("AIRTABLE_BASE_ID"),
    #     table_name=os.getenv("AIRTABLE_TABLE_NAME"),
    # )
    
    # Instantiate the OutReachAutomation class
    automation = OutReachAutomation(lead_loader)
    app = automation.app
    
    # initial graph inputs:
    # Lead ids to be processed, leave empty to fetch all news leads
    inputs = {"leads_ids": []}


    # Run the outreach automation with the provided lead name and email
    config = {'recursion_limit': 1000}
    output = app.invoke(inputs, config)
    print(output)