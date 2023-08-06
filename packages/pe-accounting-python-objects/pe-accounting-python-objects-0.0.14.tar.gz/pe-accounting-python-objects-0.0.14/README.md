# pe-accounting-python-objects

Python package to use the PE Accounting API with Python.

Definitions for business level objects. Currently only User, which models the users found in PE accounting.

PE Accounting is the Swedish bookkeeping system found at <https://www.accounting.pe/sv/var-tjanst>.  

PE's API docs are here: <https://api-doc.accounting.pe>.

This projects builds on the low level API project: <https://pypi.org/project/pe-accounting-python-api/> which will be installed as a requirement.

```sh
pip install pe-accounting-python-objects
```

```python
#!/usr/bin/env python3
eUser.pe_credentials = PeCredentials(company_id="1212", api_access_token="123asdfwer")
print(PeUser.all_users())
```
