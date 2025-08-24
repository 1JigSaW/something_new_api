from app.main import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    from app.core.settings import get_settings

    settings = get_settings()
    uvicorn.run(app=app, host=settings.host, port=settings.port, reload=True)
