from NGPIris import WD
from NGPIris.hcp import HCPManager
import pdb

#pdb.set_trace()
print(f"WD at {WD}")
hcpm = HCPManager(credentials_path="./credentials.json", autotest=False)
hcpm.set_bucket('ngs-test')
ls = hcpm.list_buckets()
print(f"Buckets: {ls}")
hcpm.test_connection()
print("Connection is working fine!")


