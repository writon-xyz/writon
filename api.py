"""
Writon API - FastAPI wrapper for AI-powered text processing.

This module provides a RESTful API for the Writon text processing engine,
allowing for integration with web front-ends and other applications.
It uses a "Bring Your Own Key" (BYOK) model via request headers.
"""

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from datetime import datetime
import logging
import traceback

# Import core application modules
from formatter.text_formatter import format_text, format_text_with_params
from formatter.case_converter import convert_case
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Application Setup ---

# Configure logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# Initialize the FastAPI application
app = FastAPI(
    title="Writon API",
    description="AI-powered text processing API for grammar correction, translation, and summarization.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the front-end (on a different origin) to communicate with this API.
# WARNING: allow_origins=["*"] is insecure for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


def is_error_response(response: str) -> bool:
    """Checks if a string response from a core module indicates an error."""
    return response.startswith("[") and "error" in response.lower()


def clean_error_message(response: str) -> str:
    """Cleans up raw error messages for user-friendly display."""
    if "HTTPSConnectionPool" in response:
        return "Could not connect to the AI provider. Please check your network."
    if "API key" in response.lower() or "unauthorized" in response.lower():
        return "The provided API key is invalid or has insufficient permissions."
    if "Rate limit" in response or "429" in response:
        return "API rate limit exceeded. Please wait and try again."
    if response.startswith("[") and response.endswith("]"):
        return response[1:-1]  # Remove brackets for cleaner display
    return response


# --- API Routes ---


@app.get("/", response_model=dict, summary="API Information")
async def root():
    """Root endpoint providing basic API information."""
    return {
        "message": "📝 Writon API - AI-powered text processing",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse, summary="Health Check")
async def health_check():
    """Health check endpoint to verify server status."""
    provider = get_current_provider()
    return HealthResponse(
        status="healthy" if provider != "not_configured" else "warning",
        version="1.0.0",
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


@app.post("/process", response_model=ProcessResponse, summary="Universal Processing")
async def process_text(request: ProcessRequest, http_request: Request):
    """Main endpoint to process text in any supported mode."""
    try:
        logger.info(
            f"Processing text with mode: {request.mode}, case: {request.case_style}"
        )

        # Extract user-provided keys from headers for BYOK mode
        user_keys = extract_user_keys(http_request)

        # Validate that translation requests include the target language
        if request.mode == "translate" and not request.target_language:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="target_language is required when mode is 'translate'",
            )

        # Call the core text formatting logic
        if request.mode == "translate":
            ai_response = format_text_with_params(
                request.text,
                "translate",
                {"target_language": request.target_language},
                user_keys,
            )
        else:
            ai_response = format_text(request.text, request.mode, user_keys)

        # Handle any errors returned from the AI processing module
        if is_error_response(ai_response):
            error_message = clean_error_message(ai_response)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=error_message
            )

        # Apply the final case formatting
        final_text = convert_case(ai_response, request.case_style)
        used_provider = (
            user_keys.get("provider") if user_keys else get_current_provider()
        )

        return ProcessResponse(
            success=True,
            original_text=request.text,
            processed_text=final_text,
            mode=request.mode,
            case_style=request.case_style,
            target_language=request.target_language,
            provider=used_provider,
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Unexpected error in /process: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected internal error occurred: {str(e)}",
        )


@app.post("/grammar", response_model=ProcessResponse, summary="Fix Grammar")
async def fix_grammar(request: SimpleProcessRequest, http_request: Request):
    """Dedicated endpoint for grammar correction."""
    logger.info("Processing grammar correction")
    user_keys = extract_user_keys(http_request)
    try:
        # Call the core text formatting logic for grammar
        ai_response = format_text(request.text, "grammar", user_keys)

        # Handle potential errors from the AI module
        if is_error_response(ai_response):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=clean_error_message(ai_response),
            )

        final_text = convert_case(ai_response, request.case_style)
        used_provider = (
            user_keys.get("provider") if user_keys else get_current_provider()
        )

        return ProcessResponse(
            success=True,
            original_text=request.text,
            processed_text=final_text,
            mode="grammar",
            case_style=request.case_style,
            provider=used_provider,
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error in /grammar: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/translate", response_model=ProcessResponse, summary="Translate Text")
async def translate_text(request: TranslateRequest, http_request: Request):
    """Dedicated endpoint for translation."""
    logger.info(f"Translating text to {request.target_language}")
    user_keys = extract_user_keys(http_request)
    try:
        # Call the core text formatting logic for translation
        ai_response = format_text_with_params(
            request.text,
            "translate",
            {"target_language": request.target_language},
            user_keys,
        )

        # Handle potential errors from the AI module
        if is_error_response(ai_response):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=clean_error_message(ai_response),
            )

        final_text = convert_case(ai_response, request.case_style)
        used_provider = (
            user_keys.get("provider") if user_keys else get_current_provider()
        )

        return ProcessResponse(
            success=True,
            original_text=request.text,
            processed_text=final_text,
            mode="translate",
            case_style=request.case_style,
            target_language=request.target_language,
            provider=used_provider,
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error in /translate: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/summarize", response_model=ProcessResponse, summary="Summarize Text")
async def summarize_text(request: SimpleProcessRequest, http_request: Request):
    """Dedicated endpoint for text summarization."""
    logger.info("Processing text summarization")
    user_keys = extract_user_keys(http_request)
    try:
        # Call the core text formatting logic for summarization
        ai_response = format_text(request.text, "summarize", user_keys)

        # Handle potential errors from the AI module
        if is_error_response(ai_response):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=clean_error_message(ai_response),
            )

        final_text = convert_case(ai_response, request.case_style)
        used_provider = (
            user_keys.get("provider") if user_keys else get_current_provider()
        )

        return ProcessResponse(
            success=True,
            original_text=request.text,
            processed_text=final_text,
            mode="summarize",
            case_style=request.case_style,
            provider=used_provider,
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error in /summarize: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
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
