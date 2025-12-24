# Run the uvicorn server with autoreload
poetry run uvicorn console_controller.main:app --app-dir src --host 0.0.0.0 --port 3000 --reload
