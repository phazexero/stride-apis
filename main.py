import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from routes.routes import router as main_router  


# print(ROOT_PATH)

app = FastAPI(title="APIs for Reports", description="Export Reports API", \
              openapi_url='/openapi.json', docs_url=None, redoc_url=None)


origins = [
    "*"
]

app.add_middleware(CORSMiddleware, allow_origins=origins,  
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Include the central router in the app
app.include_router(main_router)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(req: Request):
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title="APIs for Reports"
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload= True)