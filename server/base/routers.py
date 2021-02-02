import importlib


def register_router(app, path):
    module_path, router = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return app.include_router(getattr(module, router))
