# DeepMITRE

# DeepTempo NetFlow Front-End

## Overview
The NetFlow Analyzer is a Streamlit-based web application that processes and classifies network flow logs using MITRE ATT&CK patterns through DeepTempo's Model.

## Features
- CSV file upload and validation
- NetFlow log classification
- Interactive visualizations
- Downloadable classification results
- Responsive UI with custom styling

## Prerequisites for local replication
Check out the python dependencies [requirement.txt](./src/requirements.txt)

## Front End Usage
## Required Data Schema
The CSV input must contain the following columns:
- timestamp: Time of the flow record
- flow_dur: Duration of the flow
- src_ip: Source IP address
- dest_ip: Destination IP address
- dest_port: Destination port number
- src_port: Source port number
- fwd_bytes: Forward bytes count
- bwd_bytes: Backward bytes count
- total_bwd_pkts: Total backward packets
- total_fwd_pkts: Total forward packets

## Limitations
- Maximum file size: 200MB
- Maximum rows per file: 100

## Usage
1. Launch the Streamlit application from this endpoint
2. Upload a CSV file containing NetFlow logs
3. Wait for the classification process to complete
4. View results in the Classification Results tab
5. Explore visualizations in the Visualization tab
6. Download the classified data as CSV


---
# DeepTempo NetFlow Classification API

## Overview
The DeepTempo API provides NetFlow log classification using MITRE ATT&CK patterns and Sigma rules. This guide shows how to integrate the API using Python.

## Quick Start
```python
import requests
import pandas as pd

# API configuration
SERVING_API = "http://DeepMitre/endpoint"
headers = {
    "Authorization": f"Bearer {myapikey}",
    "Content-Type": "application/json"
}

# Load and prepare data
df = pd.read_csv('your_netflow.csv')
payload = [row for row in df.to_dict(orient='records')]

# Make API call
response = requests.post(SERVING_API, headers=headers, json=[payload, "streamlit"])
response.raise_for_status()

# Process results
results = response.json()
```

## Authentication
The API uses a simple Bearer token authentication:
- Token: `myapitoken`
- Header format: `Authorization: Bearer myapitoken`

## API Endpoint
```
POST DeepMitre://Endpoint
```

## Request Format

### Headers
```python
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
```

### Request Body
The request body should be structured as a JSON array with two elements:
1. Array of NetFlow records (converted from DataFrame)
2. The string "streamlit"

Example:
```python
# Convert DataFrame to required format
df = pd.read_csv('your_data.csv')
payload = [row for row in df.to_dict(orient='records')]

# Structure the request body
request_body = [payload]
```

### Required CSV Columns
Your input CSV file must contain:
- timestamp
- flow_dur
- src_ip
- dest_ip
- dest_port
- src_port
- fwd_bytes
- bwd_bytes
- total_bwd_pkts
- total_fwd_pkts

## Complete Example

```python
import requests
import pandas as pd
from typing import Dict, List, Union

def classify_netflow(csv_path: str) -> Union[List[Dict], None]:
    """
    Classify NetFlow data from a CSV file using DeepTempo API.
    
    Args:
        csv_path (str): Path to CSV file containing NetFlow data
    
    Returns:
        List[Dict]: Classification results or None if error occurs
    """
    SERVING_API = "http://DeepMitre/endpoint"
    headers = {
        "Authorization": "Bearer myapikey",
        "Content-Type": "application/json"
    }
    
    try:
        # Load and prepare data
        df = pd.read_csv(csv_path)
        payload = [row for row in df.to_dict(orient='records')]
        
        # Make API call
        response = requests.post(
            SERVING_API,
            headers=headers,
            json=[payload]
        )
        response.raise_for_status()
        return response.json()
        
    except pd.errors.EmptyDataError:
        print("The CSV file is empty")
        return None
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"API error: {str(e)}")
        return None

# Usage
results = classify_netflow('netflow_logs.csv')
if results:
    # Convert results to DataFrame for easier handling
    results_df = pd.DataFrame(results)
    print(results_df)
```

## Error Handling

```python
try:
    response = requests.post(SERVING_API, headers=headers, json=[payload, "streamlit"])
    response.raise_for_status()
    results = response.json()
    
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Invalid API token")
    elif e.response.status_code == 400:
        print("Invalid data format")
    else:
        print(f"HTTP error: {str(e)}")
        
except requests.exceptions.ConnectionError:
    print(f"Failed to connect to {SERVING_API}")
    
except Exception as e:
    print(f"Error: {str(e)}")
```

## Best Practices
1. Always validate your CSV data before sending
2. Implement error handling
3. Use pandas for efficient data handling
4. Check response status codes
5. Consider implementing retries for failed requests

## Response Processing

Convert API response to DataFrame for easier analysis:
```python
response = requests.post(SERVING_API, headers=headers, json=[payload, "streamlit"])
results = response.json()
results_df = pd.DataFrame(results)

# Save results to CSV
results_df.to_csv('classified_netflow.csv', index=False)
```


## Rate Limiting
- Maximum of 100 NetFlow entries per request

## Best Practices
1. Always validate NetFlow data before sending to the API
2. Implement exponential backoff for retries
3. Store API keys securely
4. Handle API responses asynchronously for large datasets
5. Monitor API response times and errors

## Support
For additional support or questions:
- To get access to a *FREE* api key, reach out to the [DeepTempo Team](deeptempo.ai/contact-us.html)
- Documentation: deeptempo.ai/docs
- Support: deeptempo.ai/contact-us.html
- Community: github.com/deepsecoss
