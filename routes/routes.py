from fastapi import APIRouter
from controllers import endpoints   
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Create a central router
router = APIRouter()

# Include the routers from controllers
router.include_router(endpoints.router, prefix="/endpoints")
# Add more include_router statements for other controllers
class NoDataError:
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

@app.exception_handler(NoDataError)
async def exception_handle(request: Request, exe: NoDataError):
    return JSONResponse(
        status_code=exe.error_code,
        content={"Error Message": exe.message}
        )

# Export the central router
__all__ = ["router"]