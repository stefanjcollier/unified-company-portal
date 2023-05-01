# Unified Data Portal
A microservice to provide consolidated company's house data from multiple sources

## Features
- simplifies name
- dedupes people and companies from multiple sources
- derives
   - active status
   - company types
- shows all nationalities in jurisdiction codes

## Endpoints
Host: http://127.0.0.1:8000
- / 
  - Health Check 
- /v1/company
  - Fetch company data
- /docs
  - A swagger endpoint


## Requirements
- Python 3.11
- pipenv

## Installation
```bash
pipenv install
```

## Run
```bash
pipenv run uvicorn app.main:app --reload
```

