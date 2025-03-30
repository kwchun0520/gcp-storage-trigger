import google.auth

def get_project() -> str:
    """Get the project ID

    Returns:
        str: The project ID
    """
    _, project = google.auth.default()
    return project
