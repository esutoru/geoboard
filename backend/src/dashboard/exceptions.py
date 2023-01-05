from fastapi import HTTPException


class WeatherApiHttpException(HTTPException):
    status_code = 400
    detail = (
        "We are currently experiencing problems accessing another external service. "
        "Please, try again later."
    )

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)
