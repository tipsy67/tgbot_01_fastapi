from pydantic import BaseModel


class RequiredChannelRequest(BaseModel):
    name: str = ""
    subscribe: bool = False


class RequiredChannelResponse(RequiredChannelRequest):
    pass