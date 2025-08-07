from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import tempfile
import os
from pathlib import Path
from pydantic import BaseModel
import shutil
import uuid

# Import your analyzer class
from app.agents.code_analysis import MultiLanguageCodeAnalyzer
from enum import Enum

class Language(Enum):
    CPP = "cpp"
    PYTHON = "python"
    JAVA = "java"
    C = "c"
    GO = "go"
    RUST = "rust"

app = FastAPI(
    title="Code Analyzer API",
    description="API for analyzing code structure and complexity",
    version="1.0.0"
)

# Setup CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer
analyzer = MultiLanguageCodeAnalyzer()

class CodeAnalysisRequest(BaseModel):
    code: str
    language: Optional[str] = None
    generate_docs: Optional[bool] = True
    generate_viz: Optional[bool] = True
    generate_refactor: Optional[bool] = True

class CodeAnalysisResponse(BaseModel):
    status: str
    analysis_id: Optional[str] = None
    visualization_path: Optional[str] = None
    visualization_url: Optional[str] = None  # Add this for web access
    documentation: Optional[str] = None
    refactoring_suggestions: Optional[str] = None
    complexity_analysis: Optional[str] = None
    improvement_suggestions: Optional[str] = None
    message: Optional[str] = None

# Create directories
UPLOAD_DIR = "uploads"
RESULTS_DIR = "app/static/results"  # For storing visualizations
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

@app.post("/analyze/code", response_model=CodeAnalysisResponse)
async def analyze_code_form(
    request: Request,
    code: str = Form(...),
    language: str = Form(...),
    options: str = Form("complexity,documentation")
):
    """
    Analyze code from form data (for web interface)
    """
    try:
        # Generate unique analysis ID
        analysis_id = str(uuid.uuid4())[:8]
        
        # Call analyzer
        results = analyzer.analyze_code_complete(
            code=code,
            display_docs=False,
            save_docs=False
        )
        
        response_data = {
            "status": "success",
            "analysis_id": analysis_id,
            "message": "Analysis completed successfully"
        }
        
        # Handle visualization
        if results.get('visualization') and os.path.exists(results['visualization']):
            # Move visualization to static directory
            viz_filename = f"viz_{analysis_id}.png"
            viz_destination = os.path.join(RESULTS_DIR, viz_filename)
            shutil.move(results['visualization'], viz_destination)
            
            response_data["visualization_path"] = viz_destination
            response_data["visualization_url"] = f"/static/results/{viz_filename}"
        
        # Add other results
        response_data.update({
            "complexity_analysis": results.get("complexity", ""),
            "documentation": results.get("documentation", ""),
            "refactoring_suggestions": results.get("refactoring", ""),
            "improvement_suggestions": results.get("improvements", "")
        })
        
        return response_data
        
    except Exception as e:
        print(f"Error in analyze_code_form: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code_json(request: CodeAnalysisRequest):
    """
    Analyze code with JSON payload (for API clients)
    """
    try:
        # Generate unique analysis ID
        analysis_id = str(uuid.uuid4())[:8]
        
        # Determine language
        language = None
        if request.language:
            try:
                language = Language(request.language.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")
        
        # Run analysis
        results = analyzer.analyze_code_complete(
            request.code,
            language=language,
            display_docs=False,
            save_docs=False
        )
        
        response_data = {
            "status": "success",
            "analysis_id": analysis_id,
            "message": "Code analysis completed successfully"
        }
        
        # Handle visualization if requested
        if request.generate_viz and results.get('visualization') and os.path.exists(results['visualization']):
            viz_filename = f"viz_{analysis_id}.png"
            viz_destination = os.path.join(RESULTS_DIR, viz_filename)
            shutil.move(results['visualization'], viz_destination)
            
            response_data["visualization_path"] = viz_destination
            response_data["visualization_url"] = f"/static/results/{viz_filename}"
        
        # Add other results based on request options
        if request.generate_docs:
            response_data["documentation"] = results.get('documentation', "")
        
        if request.generate_refactor:
            response_data["refactoring_suggestions"] = results.get('refactoring', "")
            response_data["improvement_suggestions"] = results.get('improvements', "")
        
        response_data["complexity_analysis"] = results.get('complexity', "")
        
        return response_data
        
    except Exception as e:
        print(f"Error in analyze_code_json: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/file")
async def analyze_file(
    file: UploadFile = File(...),
    generate_docs: bool = Form(True),
    save_docs: bool = Form(False)
):
    """
    Analyze code from a file upload
    """
    try:
        # Save uploaded file temporarily
        file_ext = Path(file.filename).suffix
        temp_file_path = Path(UPLOAD_DIR) / f"upload_{uuid.uuid4()}{file_ext}"
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Read file content
        with open(temp_file_path, "r", encoding='utf-8') as f:
            code = f.read()
        
        # Create request object and analyze
        request_obj = CodeAnalysisRequest(
            code=code,
            generate_docs=generate_docs,
            generate_viz=True,
            generate_refactor=True
        )
        
        return await analyze_code_json(request_obj)
    
    except Exception as e:
        print(f"Error in analyze_file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if hasattr(file, 'file') and file.file:
            file.file.close()
        if 'temp_file_path' in locals() and temp_file_path.exists():
            temp_file_path.unlink()

@app.get("/visualization/{analysis_id}")
async def get_visualization_by_id(analysis_id: str):
    """
    Retrieve visualization by analysis ID
    """
    viz_path = os.path.join(RESULTS_DIR, f"viz_{analysis_id}.png")
    if os.path.exists(viz_path):
        return FileResponse(viz_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Visualization not found")

@app.get("/results/visualization/{filename}")
async def get_visualization_file(filename: str):
    """
    Serve visualization files directly
    """
    file_path = os.path.join(RESULTS_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/download/{session_id}/{format}")
async def download_docs(session_id: str, format: str):
    """
    Download documentation in various formats
    """
    return {"status": "Download feature not implemented yet"}

@app.get("/results/documentation/{analysis_id}")
async def get_documentation(analysis_id: str):
    """
    Get documentation by analysis ID
    """
    return JSONResponse(content={"status": "Documentation retrieval not implemented"})

@app.get("/")
def read_root():
    """
    Serve main page
    """
    index_path = "app/static/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to Code Analyzer API", "docs": "/docs"}

# Setup static file serving
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/js", StaticFiles(directory=os.path.join("app", "static", "js")), name="js")
app.mount("/css", StaticFiles(directory=os.path.join("app", "static", "css")), name="css")
app.mount("/images", StaticFiles(directory=os.path.join("app", "static", "images")), name="images")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)