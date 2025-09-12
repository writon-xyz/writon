"""
Writon API - FastAPI wrapper for AI-powered text processing.

This module provides a RESTful API for the Writon text processing engine,
allowing for integration with web front-ends and other applications.
It uses a "Bring Your Own Key" (BYOK) model via request headers.
"""

from fastapi import FastAPI, HTTPException, status, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from datetime import datetime
import logging
import traceback

# Security imports
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware

# Import core application modules
from core.writon import WritonCore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Security Setup ---

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response

# Request size limiting middleware
class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_size: int = 1024 * 1024):  # 1MB default
        super().__init__(app)
        self.max_size = max_size

    async def dispatch(self, request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > self.max_size:
                return JSONResponse(
                    status_code=413,
                    content={"detail": f"Request too large. Maximum size: {self.max_size} bytes"}
                )
        response = await call_next(request)
        return response

# --- Application Setup ---

# Configure logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# Initialize the FastAPI application
app = FastAPI(
    title="Writon API",
    description="AI-powered text processing API for grammar correction, translation, and summarization.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Instantiate the core logic
core = WritonCore()

# Configure security middleware (order matters!)
# 1. Security headers (first)
app.add_middleware(SecurityHeadersMiddleware)

# 2. Request size limiting
max_request_size = int(os.getenv("MAX_REQUEST_SIZE_MB", "1")) * 1024 * 1024
app.add_middleware(RequestSizeLimitMiddleware, max_size=max_request_size)

# 3. HTTPS redirect (production only)
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# 4. Trusted host (production only)
if os.getenv("ENVIRONMENT") == "production":
    allowed_hosts = os.getenv("ALLOWED_HOSTS", "writon.xyz,*.writon.xyz").split(",")
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# 5. CORS (last)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

# --- Pydantic Data Models ---
# Define the structure and validation for API requests and responses.


class ProcessRequest(BaseModel):
    text: str = Field(
        ..., min_length=1, max_length=10000, description="Text to process"
    )
    mode: str = Field(
        ..., pattern="^(grammar|translate|summarize)$", description="Processing mode"
    )
    case_style: str = Field(
        "sentence",
        pattern="^(lower|sentence|title|upper)$",
        description="Case formatting style",
    )
    target_language: Optional[str] = Field(
        None, description="Target language for translation"
    )


class SimpleProcessRequest(BaseModel):
    text: str = Field(
        ..., min_length=1, max_length=10000, description="Text to process"
    )
    case_style: str = Field(
        "sentence",
        pattern="^(lower|sentence|title|upper)$",
        description="Case formatting style",
    )


class TranslateRequest(BaseModel):
    text: str = Field(
        ..., min_length=1, max_length=10000, description="Text to translate"
    )
    target_language: str = Field(..., min_length=1, description="Target language")
    case_style: str = Field(
        "sentence",
        pattern="^(lower|sentence|title|upper)$",
        description="Case formatting style",
    )


class ProcessResponse(BaseModel):
    success: bool
    original_text: str
    processed_text: str
    mode: str
    case_style: str
    target_language: Optional[str] = None
    provider: Optional[str] = None
    timestamp: str


class ErrorResponse(BaseModel):
    success: bool = False
    error_type: str
    message: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    version: str
    provider: str
    timestamp: str


class ProvidersResponse(BaseModel):
    available_providers: List[str]
    current_provider: str
    supported_modes: List[str]
    supported_cases: List[str]


# --- Helper Functions ---


def get_current_provider() -> str:
    """Gets the default AI provider from environment variables."""
    return os.getenv("API_PROVIDER", "not_configured")


def extract_user_keys(request: Request) -> Optional[dict]:
    """
    Extracts user-provided AI credentials from request headers for BYOK mode.
    FastAPI automatically lowercases headers.
    """
    user_keys = {}
    provider_map = {
        "openai": "x-openai",
        "groq": "x-groq",
        "google": "x-google",
        "anthropic": "x-anthropic",
    }

    # Extract provider override first
    if "x-provider" in request.headers:
        user_keys["provider"] = request.headers["x-provider"]

    # Extract keys and models based on provider map
    for provider, prefix in provider_map.items():
        key_header = f"{prefix}-key"
        model_header = f"{prefix}-model"
        if key_header in request.headers:
            user_keys[f"{provider}_key"] = request.headers[key_header]
        if model_header in request.headers:
            user_keys[f"{provider}_model"] = request.headers[model_header]

    return user_keys if user_keys else None


def create_error_response(error_type: str, message: str) -> ErrorResponse:
    """Creates a standardized error response object."""
    return ErrorResponse(
        error_type=error_type, message=message, timestamp=datetime.now().isoformat()
    )


# --- API Routes ---


@app.get("/api", response_model=dict, summary="API Information")
async def api_info():
    """API information endpoint."""
    return {
        "message": "📝 Writon API - AI-powered text processing",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse, summary="Health Check")
async def health_check():
    """Health check endpoint to verify server status."""
    provider = get_current_provider()
    return HealthResponse(
        status="healthy" if provider != "not_configured" else "warning",
        version="0.1.0",
        provider=provider,
        timestamp=datetime.now().isoformat(),
    )


@app.get("/providers", response_model=ProvidersResponse, summary="Get Provider Info")
async def get_providers():
    """Returns a list of available providers and supported configurations."""
    return ProvidersResponse(
        available_providers=["openai", "google", "anthropic", "groq"],
        current_provider=get_current_provider(),
        supported_modes=["grammar", "translate", "summarize"],
        supported_cases=["lower", "sentence", "title", "upper"],
    )


@app.post("/upload", summary="Upload a text file")
@limiter.limit("10/minute")
async def upload_file(request: Request, file: UploadFile = File(...)):
    """
    Uploads a text file (.txt, .md, .rtf) and returns its content.
    """
    # Check file type
    if not file.filename.endswith(('.txt', '.md', '.rtf')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .txt, .md, or .rtf file.")
    
    # Check file size (5MB limit)
    max_file_size = int(os.getenv("MAX_FILE_SIZE_MB", "5")) * 1024 * 1024
    if file.size and file.size > max_file_size:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Maximum size: {max_file_size} bytes ({os.getenv('MAX_FILE_SIZE_MB', '5')}MB)"
        )
    
    try:
        contents = await file.read()
        
        # Double-check size after reading
        if len(contents) > max_file_size:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size: {max_file_size} bytes ({os.getenv('MAX_FILE_SIZE_MB', '5')}MB)"
            )
        
        decoded_contents = contents.decode('utf-8')
        return {"filename": file.filename, "content": decoded_contents}
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid file encoding. Please upload a UTF-8 encoded file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error uploading or reading the file: {e}")


async def _process_request(
    text: str,
    mode: str,
    case_style: str,
    http_request: Request,
    target_language: Optional[str] = None,
) -> ProcessResponse:
    """Helper function to process text requests."""
    try:
        logger.info(f"Processing text with mode: {mode}, case: {case_style}")
        user_keys = extract_user_keys(http_request)

        if mode == "translate" and not target_language:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="target_language is required when mode is 'translate'",
            )

        final_text = core.process_text(
            text=text,
            mode=mode,
            case_style=case_style,
            target_language=target_language,
            user_keys=user_keys,
        )

        used_provider = user_keys.get("provider") if user_keys else get_current_provider()

        return ProcessResponse(
            success=True,
            original_text=text,
            processed_text=final_text,
            mode=mode,
            case_style=case_style,
            target_language=target_language,
            provider=used_provider,
            timestamp=datetime.now().isoformat(),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Unexpected error in _process_request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected internal error occurred: {str(e)}",
        )


@app.post("/process", response_model=ProcessResponse, summary="Universal Processing")
@limiter.limit("30/minute")
async def process_text(request: Request, process_request: ProcessRequest):
    """Main endpoint to process text in any supported mode."""
    return await _process_request(
        text=process_request.text,
        mode=process_request.mode,
        case_style=process_request.case_style,
        http_request=request,
        target_language=process_request.target_language,
    )


@app.post("/grammar", response_model=ProcessResponse, summary="Fix Grammar")
@limiter.limit("30/minute")
async def fix_grammar(request: Request, grammar_request: SimpleProcessRequest):
    """Dedicated endpoint for grammar correction."""
    return await _process_request(
        text=grammar_request.text,
        mode="grammar",
        case_style=grammar_request.case_style,
        http_request=request,
    )


@app.post("/translate", response_model=ProcessResponse, summary="Translate Text")
@limiter.limit("30/minute")
async def translate_text(request: Request, translate_request: TranslateRequest):
    """Dedicated endpoint for translation."""
    return await _process_request(
        text=translate_request.text,
        mode="translate",
        case_style=translate_request.case_style,
        http_request=request,
        target_language=translate_request.target_language,
    )


@app.post("/summarize", response_model=ProcessResponse, summary="Summarize Text")
@limiter.limit("30/minute")
async def summarize_text(request: Request, summarize_request: SimpleProcessRequest):
    """Dedicated endpoint for text summarization."""
    return await _process_request(
        text=summarize_request.text,
        mode="summarize",
        case_style=summarize_request.case_style,
        http_request=request,
    )


# --- Custom Exception Handlers ---


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handles HTTPExceptions gracefully, returning a structured JSON error."""
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response("http_error", exc.detail).dict(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catches any unhandled exceptions and returns a generic 500 error."""
    logger.error(f"Unhandled exception for request {request.url.path}: {str(exc)}")
    traceback.print_exc()  # Log the full traceback for debugging
    return JSONResponse(
        status_code=500,
        content=create_error_response(
            "internal_server_error", "An unexpected error occurred on the server."
        ).dict(),
    )


# --- Static Files Mount ---
# Mount static files for frontend, but exclude API routes
app.mount("/static", StaticFiles(directory="frontend/assets"), name="assets")

# Serve the main frontend HTML file for root path
@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Serve the main frontend HTML file."""
    from fastapi.responses import HTMLResponse
    import os
    
    # Read the HTML file content
    html_file_path = os.path.join("frontend", "index.html")
    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        # Fallback to API info if frontend file not found
        return {
            "message": "📝 Writon API - AI-powered text processing",
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/health",
            "note": "Frontend file not found, serving API info instead"
        }


# --- Server Execution ---

if __name__ == "__main__":
    import uvicorn

    # Check for default provider configuration before starting the server
    provider = get_current_provider()
    if provider == "not_configured":
        logger.warning(
            "API_PROVIDER not set in .env. Server-side processing will fail without BYOK headers."
        )
    else:
        logger.info(f"🚀 Starting API with default provider: {provider}")

    # Run the Uvicorn server
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
