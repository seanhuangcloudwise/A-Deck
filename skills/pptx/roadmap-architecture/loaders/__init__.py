"""Roadmap Architecture loader registry helpers."""

LOADER_REGISTRY = {}


def register_loader(name, load_fn):
    LOADER_REGISTRY[name] = load_fn


def get_loader(name):
    return LOADER_REGISTRY.get(name)


def list_all_loaders():
    return sorted(LOADER_REGISTRY.keys())
