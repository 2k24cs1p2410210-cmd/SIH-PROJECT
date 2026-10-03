from fastapi import HTTPException, status


class TransitPulseException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class ResourceNotFoundException(TransitPulseException):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            detail=f"{resource} with ID '{resource_id}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )


class InvalidGpsCoordinateException(TransitPulseException):
    def __init__(self, message: str = "Invalid GPS latitude/longitude values."):
        super().__init__(detail=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
