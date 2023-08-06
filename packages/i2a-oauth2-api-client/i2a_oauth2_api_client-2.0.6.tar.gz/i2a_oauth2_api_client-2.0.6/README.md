#Installation
```python
pip install i2a-oauth2-api-client
```

#Usage
```python
from i2a_oauth2_api_client.client import I2AOauth2Client
from i2a_oauth2_api_client.enums import Environment


client = I2AOauth2Client(
    client_id='your client id',
    client_secret='your client secret',
    environment=Environment.QA  # default
)
```

#Enums
```python
from enum import Enum


class Environment(Enum):
    QA = 1
    PROD = 2
```

