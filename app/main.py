from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import pandas as pd

from app.ingest import detect_provider, normalize_azure, normalize_aws, normalize_gcp
from app.database import SessionLocal
from app.models import CloudCost
from app.savings import calculate_annual_savings

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/upload")
async def upload(file: UploadFile = File(...), account: str = ""):
    df = pd.read_csv(file.file)
    provider = detect_provider(df.columns)

    if provider == "AZURE":
        clean = normalize_azure(df, account)
    elif provider == "AWS":
        clean = normalize_aws(df, account)
    elif provider == "GCP":
        clean = normalize_gcp(df, account, 2025, 1)
    else:
        return {"error": "Unsupported provider"}

    db = SessionLocal()

    for _, row in clean.iterrows():
        record = CloudCost(**row.to_dict())
        db.merge(record)

    db.commit()

    calculate_annual_savings(db, account, provider)

    return {"rows_ingested": len(clean)}


app.mount(
    "/",
    StaticFiles(directory="frontend/build", html=True),
    name="frontend"
)
