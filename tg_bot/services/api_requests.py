from functools import wraps
from typing import Callable

import aiohttp


class APIPath:
    BASE_URL = "http://localhost:8000/api/v1"
    set_user = f"{BASE_URL}/users"


def aiohttp_request(method: str = "POST", url: str = None, status_code: int = 200):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                request_data = await func(*args, **kwargs)

                async with aiohttp.ClientSession() as session:
                    request_kwargs = {"url": url}

                    if request_data:
                        for key in ["params", "headers", "json", "data"]:
                            if key in request_data:
                                request_kwargs[key] = request_data[key]

                    async with session.request(method, **request_kwargs) as response:
                        if response.status != status_code:
                            error_text = await response.text()
                            return {
                                "error": f"HTTP Error {response.status}",
                                "details": error_text,
                            }

                        try:
                            return await response.json()
                        except:
                            return await response.text()

            except aiohttp.ClientError as e:
                return {"error": f"Client error: {str(e)}"}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}

        return wrapper

    return decorator


@aiohttp_request(method="POST", url=APIPath.set_user)
async def set_user(user, payload=None):
    json = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": user.language_code,
    }
    if payload is not None:
        json["payload"] = payload

    return {"json": json}


