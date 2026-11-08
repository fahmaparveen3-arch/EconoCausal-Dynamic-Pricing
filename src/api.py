from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from fastapi import FastAPI, HTTPException

from src.validate_data import validate_dataset
from src.validate_pricing_calculations import validate_pricing_calculations


DATA_DIR = Path(__file__).resolve().parent.parent / "data"

app = FastAPI(
    title="EconoCausal Validation API",
    description="API for dataset quality and pricing calculation validation.",
    version="1.0.0",
)


def get_dataset_path(filename: str) -> Path:
    if Path(filename).name != filename or Path(filename).suffix.lower() != ".csv":
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid CSV filename.",
        )

    dataset_path = (DATA_DIR / filename).resolve()

    if dataset_path.parent != DATA_DIR.resolve():
        raise HTTPException(status_code=400, detail="Invalid dataset path.")

    if not dataset_path.is_file():
        raise HTTPException(status_code=404, detail="Dataset not found.")

    return dataset_path


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EconoCausal Validation API",
    }


@app.get("/api/validation/dataset/{filename}")
def dataset_validation(filename: str):
    dataset_path = get_dataset_path(filename)

    output = StringIO()

    with redirect_stdout(output):
        completed = validate_dataset(dataset_path)

    return {
        "filename": filename,
        "completed": bool(completed),
        "report": output.getvalue(),
    }


@app.get("/api/validation/pricing/{filename}")
def pricing_validation(filename: str):
    dataset_path = get_dataset_path(filename)

    output = StringIO()

    with redirect_stdout(output):
        passed = validate_pricing_calculations(dataset_path)

    return {
        "filename": filename,
        "passed": bool(passed),
        "report": output.getvalue(),
    }
