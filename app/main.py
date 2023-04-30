from fastapi import FastAPI, HTTPException

from app.companies.errors import *
from app.companies.fetch_data import FetchData

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/v1/company/{jurisdiction_code}/{company_number}")
def fetch_company(jurisdiction_code: str, company_number: str):
    try:
        return FetchData(
            jurisdiction_code.lower(),
            company_number
        ).call()

    except NotFoundException:
        raise HTTPException(status_code=404)
    except UnsupportedJurisdictionException:
        raise HTTPException(status_code=400, detail=f"Unsupported Jurisdiction: {jurisdiction_code}")
    except CompanyException:
        # Idea: Report error to Rollbar/Similar
        raise HTTPException(status_code=500)


