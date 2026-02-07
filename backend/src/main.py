"""
Flight Track Analyzer Backend
FastAPI server for processing flight trajectory data
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .data_processor import FlightDataProcessor

app = FastAPI(
    title="Flight Track Analyzer API",
    description="Backend API for processing and analyzing flight trajectory data",
    version="1.0.1"
)

# Enable CORS for Electron app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processor
processor = FlightDataProcessor()


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Flight Track Analyzer API",
        "status": "running",
        "version": "1.0.1",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/analyze-flight"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/analyze-flight")
async def analyze_flight(file: UploadFile = File(...)):
    """
    Analyze flight trajectory from CSV file
    
    Args:
        file: CSV file upload (FlightRadar24 format)
    
    Returns:
        JSON with processed flight data, statistics, and plot data
    
    Raises:
        HTTPException: If CSV is invalid or processing fails
    """
    try:
        # Read CSV file
        contents = await file.read()
        
        # Process flight data
        data = processor.process_flight_data(contents)
        
        return JSONResponse({
            'success': True,
            'data': data
        })
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)