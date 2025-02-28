from fastapi import FastAPI
import validators
from pydantic import BaseModel
import json
from api_executor import ApiExecutor
from fastapi.responses import JSONResponse


app = FastAPI()
api_executor = ApiExecutor()

def cust_response(code, message, data=None):
    message = {
        "status": code,
        "message": message
    }
    if data:
        message.update(data)
    return JSONResponse(content=message)

class CreateShortUrl(BaseModel):
    url: str
@app.post("/v1/url")
def create_shorturl(payload:CreateShortUrl):
    if not validators.url(payload.url):
        return cust_response(500, "Input URL cannot be shorten")
    payload_dict = payload.dict()
    if payload.url:
        payload_short_url = api_executor.create_url_shortener(payload.url)
        payload_dict.update({"short_url": payload_short_url})
    return cust_response(200, "Successfully created short url", data= payload_dict)

