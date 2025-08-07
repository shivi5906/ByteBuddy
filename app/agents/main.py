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
    time: str 
    space: str 
    language: Optional[str] = None
    generate_docs: Optional[bool] = True
    generate_viz: Optional[bool] = True
    generate_refactor: Optional[bool] = True

class CodeAnalysisResponse(BaseModel):
    status: str
    analysis_id: Optional[str] = None
    visualization_path: Optional[str] = None
    visualization_url: Optional[str] = None
    documentation: Optional[str] = None
    refactoring_suggestions: Optional[str] = None
    complexity_analysis: Optional[str] = None
    improvement_suggestions: Optional[str] = None
    message: Optional[str] = None
    results: dict

# Create directories
UPLOAD_DIR = "uploads"
RESULTS_DIR = "app/static/results"  # For storing visualizations
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

def extract_complexity_from_analysis(complexity_text: str) -> dict:
    """Extract time and space complexity from the analysis text"""
    if not complexity_text:
        return {"time": "O(n)", "space": "O(1)"}
    
    import re
    
    # Extract time complexity
    time_match = re.search(r'Time Complexity:\s*([O\(][^)]*\))', complexity_text, re.IGNORECASE)
    time_complexity = time_match.group(1) if time_match else "O(n)"
    
    # Extract space complexity  
    space_match = re.search(r'Space Complexity:\s*([O\(][^)]*\))', complexity_text, re.IGNORECASE)
    space_complexity = space_match.group(1) if space_match else "O(1)"
    
    return {
        "time": time_complexity,
        "space": space_complexity
    }

@app.post("/analyze/code")
async def analyze_code_form(
    request: Request,
    code: str = Form(...),
    language: str = Form(...),
    options: str = Form("complexity,documentation")
):
    """
    Analyze code from form data (for web interface) and give a perfect analysis for the complete code structure.
    """
    try:
        # Generate unique analysis ID
        analysis_id = str(uuid.uuid4())[:8]
        
        print(f"🚀 Starting analysis with ID: {analysis_id}")
        print(f"📝 Code length: {len(code)} characters")
        print(f"🔤 Language: {language}")
        print(f"⚙️ Options: {options}")
        
        # Call your analyzer
        results = analyzer.analyze_code_complete(
            code=code,
            display_docs=False,  # Don't display in terminal for web
            save_docs=False      # Don't save files, return content
        )
        
        print(f"✅ Agent analysis complete. Results keys: {list(results.keys())}")
        
        # Handle visualization file
        visualization_url = None
        if results.get('visualization') and os.path.exists(results['visualization']):
            # Move visualization to static directory with analysis_id
            viz_filename = f"viz_{analysis_id}.png"
            viz_destination = os.path.join(RESULTS_DIR, viz_filename)
            
            try:
                shutil.move(results['visualization'], viz_destination)
                visualization_url = f"/static/results/{viz_filename}"
                print(f"📊 Moved visualization to: {viz_destination}")
            except Exception as e:
                print(f"⚠️ Error moving visualization: {e}")
        
        # Extract complexity information
        complexity_data = extract_complexity_from_analysis(results.get('complexity', ''))
        print(f"🧮 Extracted complexity: {complexity_data}")
        
        # Build the response in the EXACT format your frontend expects
        response_data = {
            "results": {
                "success": True,
                "analysis_id": analysis_id,
                "complexity_analysis": results.get("complexity", "No complexity analysis available"),
                "documentation": results.get("documentation", "No documentation generated"),
                "refactoring_suggestions": results.get("refactoring", "No refactoring suggestions available"),
                "improvement_suggestions": results.get("improvements", "No improvement suggestions available"),
                "visualization_path": viz_destination if visualization_url else None,
                "structure_img": visualization_url,  # This is what your frontend looks for
                "visualization_url": visualization_url
            }
        }
        
        print(f"📤 Sending response with structure_img: {visualization_url}")
        return response_data
        
    except Exception as e:
        print(f"❌ Error in analyze_code_form: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return error in the expected format
        return {
            "results": {
                "success": False,
                "error": str(e),
                "analysis_id": None,
                "complexity_analysis": "Analysis failed",
                "documentation": "Documentation generation failed",
                "refactoring_suggestions": "Refactoring analysis failed", 
                "improvement_suggestions": "Improvement analysis failed",
                "structure_img": None
            }
        }

@app.get("/visualization/{analysis_id}")
async def get_visualization_by_id(analysis_id: str):
    """
    Retrieve visualization by analysis ID and display it in the section also 
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
   
# Setup static file serving
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/js", StaticFiles(directory=os.path.join("app", "static", "js")), name="js")
app.mount("/css", StaticFiles(directory=os.path.join("app", "static", "css")), name="css")
app.mount("/images", StaticFiles(directory=os.path.join("app", "static", "images")), name="images")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)