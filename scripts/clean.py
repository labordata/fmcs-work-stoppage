#['Employer', 'Union', 'Union Local', 'Case Number', 'BU', 'NAICS', 'Industry', 'City, State', '# Idled', 'Start Date', 'End Date', 'Duration', 'Parties', '', 'Affected City', 'Affected State', 'Ending Fiscal Year', 'State"', 'WS Begin\nDate', 'WS End\nDate', 'Ending\nFiscal Year']

import csv
import sys
import dateutil.parser

reader = csv.DictReader(sys.stdin)

writer = csv.DictWriter(sys.stdout,
                        fieldnames=reader.fieldnames[:12],
                        extrasaction='ignore')
writer.writeheader()

for row in reader:
    if not row['City, State']:
        city_state = row['Affected City'] + ', ' + row['Affected State']
        if city_state.strip(', '):
            row['City, State'] = city_state
    parties = row['Parties'].split('/', 1)
    if not row['Employer'] and len(parties) == 2:
        row['Employer'], row['Union'] = parties
    start_date = row['Start Date']
    if start_date:
        row['Start Date'] = dateutil.parser.parse(start_date).date()
    end_date = row['End Date']
    if end_date:
        row['End Date'] = dateutil.parser.parse(end_date).date()
        
    writer.writerow(row)
