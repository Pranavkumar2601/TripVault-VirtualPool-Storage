from fastapi import FastAPI

app = FastAPI(title="TripVault API")

@app.get("/health")
def health():
    return {"status": "ok"}
