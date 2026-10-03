import uuid


def generate_uuid() -> str:
    """Generates standard string representation of UUID v4."""
    return str(uuid.uuid4())
