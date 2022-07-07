from pydantic import BaseModel


class FreeSpotGetResponse(BaseModel):
    """
    Схема, описывающая ответ на запрос о получении ближайшего свободного интервала в календарях.
    """

    starts_at: str
    ends_at: str

    @staticmethod
    def make_serialized_item(data: dict) -> dict:
        result = {
            "starts_at": data.get('starts_at').strftime('%Y-%m-%d %H:%M'),
            "ends_at": data.get('starts_at').strftime('%Y-%m-%d %H:%M')
        }

        return result

    @staticmethod
    def serializer(data: dict) -> dict:
        return FreeSpotGetResponse.make_serialized_item(data)
