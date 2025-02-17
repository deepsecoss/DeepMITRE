# DeepTempo NetFlow Analyzer
## User Guide

DeepTempo NetFlow Analyzer is a web-based tool that analyzes network flow logs and classifies them according to MITRE ATT&CK patterns. This guide will help you understand how to use the application effectively.

## Getting Started

### Accessing the Application
1. Navigate to the DeepTempo NetFlow Analyzer web interface
2. The interface will display a file upload area and instructions
3. No installation is required - the application runs in your web browser

### Data Requirements

Your input data must be in CSV format with the following specifications:

#### Required Columns
- `timestamp`: Time when the flow record was captured
- `flow_dur`: Duration of the network flow
- `src_ip`: Source IP address
- `dest_ip`: Destination IP address
- `dest_port`: Destination port number
- `src_port`: Source port number
- `fwd_bytes`: Number of bytes sent forward
- `bwd_bytes`: Number of bytes sent backward
- `total_bwd_pkts`: Total number of backward packets
- `total_fwd_pkts`: Total number of forward packets

#### File Limitations
- Maximum file size: 200MB
- Maximum rows per file: 100 rows
- File format: CSV only

## Using the Application

### Step 1: Preparing Your Data
Before uploading, ensure your CSV file:
- Contains all required columns (listed above)
- Has clean, properly formatted data
- Does not exceed 100 rows
- Is under 200MB in size

### Step 2: Uploading Data
1. Click the upload area or drag and drop your CSV file
2. The application will automatically validate your file
3. If any issues are found, error messages will guide you on what needs to be fixed

### Step 3: Processing and Results
Once your file is validated, the application will:
1. Process your NetFlow data
2. Apply MITRE ATT&CK classification
3. Generate results in two tabs:
   - Classification Results: Detailed analysis of each flow
   - Visualization: Visual representation of the analysis (coming soon)

### Step 4: Downloading Results
- Click the "📥 Download Classified Data" button
- Results will be saved as a CSV file named 'netflow_to_mitre.csv'
- The downloaded file will contain all original data plus classification results

## Error Handling

### Common Errors and Solutions

1. Missing Columns
   - Error: "Missing columns: [column names]"
   - Solution: Ensure your CSV contains all required columns

2. Row Limit Exceeded
   - Error: "File exceeds the row limit of 100"
   - Solution: Reduce the number of rows in your input file

3. Invalid Data Format
   - Error: "Invalid [field] at row [number]"
   - Solution: Check the specified row and ensure data meets format requirements

### Data Validation Rules

The application validates:
- IP addresses: Must be valid IPv4 or IPv6 addresses
- Ports: Must be between 0 and 65535
- Timestamps: Must follow standard date-time formats
- Numeric fields: Must be non-negative numbers

## Getting API Access

To use the service programmatically:
1. Visit the [Contact Us](https://www.deeptempo.ai/contact-us.html) page
2. Request an API key
3. Review the [Documentation](https://github.com/deepsecoss/DeepMITRE) for API usage

## Free Trial Information

A free trial is available through Snowflake:
1. Access unlimited row processing
2. Full access to Incident and MITRE models
3. Sign up at [Free Trial Signup](https://app.snowflake.com/marketplace/listing/GZTYZOYXHP3/deeptempo-cybersecurity-tempo)

## Support and Resources

- Documentation: [GitHub Repository](https://github.com/deepsecoss/DeepMITRE)
- Privacy Policy: [DeepTempo Privacy Policy](https://www.deeptempo.ai/docs/DeepTempo%20-%20Privacy%20Policy%20for%20Snowflake%20NativeApp.pdf)
- Contact: [DeepTempo Contact Page](https://www.deeptempo.ai/contact-us.html)
- Community: [GitHub Community](https://github.com/deepsecoss)
