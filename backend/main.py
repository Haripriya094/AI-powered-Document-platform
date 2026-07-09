import uvicorn
from fastapi import FastAPI
from backend.core import router
from starlette.middleware.cors import CORSMiddleware
from backend.constants.app_configurations import service_host,port

class fastAPIservice:
    @staticmethod
    def fastapi():
        app=FastAPI(title="AI-powered resume Analyzer",
                version="0.1.0",
                description="AI powered resume Analyzer")
        app.include_router(router)

        app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )
        try:
            uvicorn.run(app, host=service_host, port=int(port))
        except Exception as es:
            print(es)

if __name__ == "__main__":
    fastAPIservice.fastapi()

