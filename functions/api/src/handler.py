from src.common.error.http import HTTPError
from src.controllers.health_controller import HealthController
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.exception import (
    default_exception_handler,
    exception_handler,
    python_exception_handler,
    request_validation_error_handler,
)
from src.middleware.request_extractor import RequestExtractorMiddleware
from src.middleware.request_logger import RequestLogger
from src.repositories.environment_repository import EnvironmentRepository

environment_repository = EnvironmentRepository()

service_name = "home-infrastructure"
app = FastAPI(title=service_name)

logger = RequestLogger(service_name=service_name)

# Add middleware first
app.middleware("http")(logger.log_request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    RequestExtractorMiddleware, api_host=environment_repository.get_api_host()
)

# Add handlers
app.add_exception_handler(HTTPError, exception_handler)
app.add_exception_handler(HTTPException, default_exception_handler)
app.add_exception_handler(Exception, python_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)

# Add routers or include other routers
app.include_router(HealthController().router, prefix="/health")

handler = FastAPI(app=app)