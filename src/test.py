from core.auth import UserPassCredentials
from apps.collectors import CollectorManagementClient
import os

creds = UserPassCredentials(
    username=os.environ.get('USERNAME'),
    password=os.environ.get('PASSWORD')
)

collector_management_client = CollectorManagementClient(creds)
collector_management_client.list()[0].write({
    "message": "hello world"
})
