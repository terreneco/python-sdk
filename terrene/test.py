from .core.auth import UserPassCredentials
from .apps.collectors import CollectorManagementClient
from .apps.storage import StorageManagementClient
import os

creds = UserPassCredentials(
    username=os.environ.get('USERNAME'),
    password=os.environ.get('PASSWORD')
)
print(creds)


collector_management_client = CollectorManagementClient(creds)
collector = collector_management_client.list({
    "owners__email": os.environ.get('USERNAME')
})

storage_management_client = StorageManagementClient(creds)
print(storage_management_client)

# storage_management_client.create({
#     "name"    : "my stuff",
#     "contributors": [],
#     "owners": [os.environ.get('USERNAME')],
#     "region": "eastus"
# })

storage = storage_management_client.list({
    "name": "my stuff"
})[0]
print(storage)

storage.create_table("hello")
# storage.insert_record(
#     {
#         "name": "kash"
#     },
#     table_name="hello"
# )
query = storage.query(
    filter_str="",
    table_name="hello"
)
print(query)

obj = query[0]
# obj.partial_update({
#     "name": "khashayar"
# })
print(obj)
# storage.drop_table("hello")
