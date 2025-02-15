import re
import time
import ipaddress
import pandas as pd
from typing import List,Tuple
from datetime import datetime
from collections import deque
from threading import Lock
from functools import wraps

styling = """
    <style>
    /* Card-like containers */
    .custom-markdown {
        background-color: #171717;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
        
    /* Link styling */
    a {
        color: #FED766 !important;
        text-decoration: none !important;
        transition: color 0.3s ease;
    }
    a:hover {
        color: #FC2505 !important;
        text-decoration: underline !important;
    }

    /* Footer styling */
    .footer {
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 0.5rem;
        margin-top: 1rem;
        text-align: center;
    }
    </style>
"""


class RateLimiter:
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
        self.lock = Lock()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.lock:
                now = time.time()
                # Remove old calls outside the time window
                while self.calls and now - self.calls[0] >= self.time_window:
                    self.calls.popleft()
                
                if len(self.calls) >= self.max_calls:
                    raise Exception("Rate limit exceeded. Please try again later.")
                
                self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper


class NetflowValidator:
    TIMESTAMP_FORMATS = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y/%m/%d %H:%M:%S"
    ]
    
    PORT_MIN = 0
    PORT_MAX = 65535
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_port(port: int) -> bool:
        return isinstance(port, (int, float)) and NetflowValidator.PORT_MIN <= port <= NetflowValidator.PORT_MAX
    
    @staticmethod
    def validate_timestamp(timestamp: str) -> bool:
        for fmt in NetflowValidator.TIMESTAMP_FORMATS:
            try:
                datetime.strptime(timestamp, fmt)
                return True
            except ValueError:
                continue
        return False
    
    @staticmethod
    def validate_numeric(value: float) -> bool:
        return isinstance(value, (int, float)) and value >= 0


def sanitize_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Sanitizes and validates the input dataframe.
    Returns: (sanitized_df, list_of_errors)
    """
    errors = []
    
    # Create a copy to avoid modifying the original
    clean_df = df.copy()
    
    # Basic sanitization
    for column in clean_df.columns:
        # Convert column names to lowercase
        clean_df.rename(columns={column: column.lower().strip()}, inplace=True)
    
    validator = NetflowValidator()
    
    # Validate each required field
    for idx, row in clean_df.iterrows():
        try:
            # IP validation
            if not validator.validate_ip(str(row['src_ip'])):
                errors.append(f"Invalid source IP at row {idx}: {row['src_ip']}")
            if not validator.validate_ip(str(row['dest_ip'])):
                errors.append(f"Invalid destination IP at row {idx}: {row['dest_ip']}")
            
            # Port validation
            if not validator.validate_port(row['src_port']):
                errors.append(f"Invalid source port at row {idx}: {row['src_port']}")
            if not validator.validate_port(row['dest_port']):
                errors.append(f"Invalid destination port at row {idx}: {row['dest_port']}")
            
            # Timestamp validation
            if not validator.validate_timestamp(str(row['timestamp'])):
                errors.append(f"Invalid timestamp at row {idx}: {row['timestamp']}")
            
            # Numeric field validation
            numeric_fields = ['flow_dur', 'fwd_bytes', 'bwd_bytes', 'total_bwd_pkts', 'total_fwd_pkts']
            for field in numeric_fields:
                if not validator.validate_numeric(row[field]):
                    errors.append(f"Invalid {field} at row {idx}: {row[field]}")
                    
        except KeyError as e:
            errors.append(f"Missing required column: {str(e)}")
    
    # Remove any HTML or script tags from string fields
    string_columns = clean_df.select_dtypes(include=['object']).columns
    for col in string_columns:
        clean_df[col] = clean_df[col].astype(str).apply(lambda x: re.sub(r'<[^>]*>', '', x))
    
    return clean_df, errors

api_rate_limiter = RateLimiter(max_calls=100, time_window=60)


schema_information = """
        <div class="custom-markdown">
        <table>
            <thead>
            <tr>
                <th>Network Fields</th>
                <th>Description</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>timestamp</td>
                <td>Time of the flow record</td>
            </tr>
            <tr>
                <td>flow_dur</td>
                <td>Duration of the flow</td>
            </tr>
            <tr>
                <td>src_ip</td>
                <td>Source IP address</td>
            </tr>
            <tr>
                <td>dest_ip</td>
                <td>Destination IP address</td>
            </tr>
            <tr>
                <td>dest_port</td>
                <td>Destination port number</td>
            </tr>
            <tr>
                <td>src_port</td>
                <td>Source port number</td>
            </tr>
            <tr>
                <td>fwd_bytes</td>
                <td>Forward bytes count</td>
            </tr>
            <tr>
                <td>bwd_bytes</td>
                <td>Backward bytes count</td>
            </tr>
            <tr>
                <td>total_bwd_pkts</td>
                <td>Total backward packets</td>
            </tr>
            <tr>
                <td>total_fwd_pkts</td>
                <td>Total forward packets</td>
            </tr>
            </tbody>
        </table>
        </div>
        """