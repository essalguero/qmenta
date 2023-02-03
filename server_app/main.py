import os
from time import sleep

import numpy
import uvicorn

from db.database import Database
from session_verifier import SessionData
from pydantic import BaseModel

from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, Response, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.backends.implementations import InMemoryBackend

from fastapi.responses import FileResponse


import pydicom
from PIL import Image


app = FastAPI(title='Server',
              description='Server',
              version='0.0.0')

app.add_middleware(
    CORSMiddleware,
    #allow_origins=["localhost:80", "localhost:8080", "127.0.0.1:*"]
    allow_origins=["*"]
)


class SessionData(BaseModel):
    username: str


cookie_params = CookieParameters()
# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)
backend = InMemoryBackend[UUID, SessionData]()

def _initial_message():
    return {"message": "Fast API running"}


@app.get("/")
async def root():
    return _initial_message()


@app.get("/main")
async def main():
    return _initial_message()


@app.post("/logging")
async def logging(response: Response, username: str = Form(), password: str = Form()):
    """Validate user credentials and allow access if data is correct"""
    db_conn = None
    retries = 10
    while not db_conn:
        try:
            db_conn = db_pool.pop()
        except KeyError as e_exc:
            retries -= 1
            if not retries:
                return {"response": 400,
                        "message": "Could not connect, please try again later.\n{0}".format(e_exc)}
            sleep(0.05)

    user_loging = db_conn.logging(username, password)

    db_pool.add(db_conn)

    if user_loging['result']:
        data = SessionData(username=username)
        session = uuid4()

        session_data = {'session': session, 'data': data}

        await backend.create(session, data)

        response.set_cookie(key='session_data', value=session_data, httponly=False, samesite='none')

        return data

    else:
        raise HTTPException(status_code=404, detail="Could not loging")


@app.post("/close_session")
async def close_session(response: Response, request: Request):
    """Close connection deleting the cookie"""

    if len(request.cookies) == 0 or not request.cookies['session_data'] or len(backend.data) == 0:
        raise HTTPException(status_code=404, detail="Session Not Started")
    await backend.delete(eval(request.cookies['session_data'])['session'])
    cookie.delete_from_response(response)
    return "session closed"


@app.get("/patient_data")
def patient_data(response: Response, request: Request, username: str):
    """
    Returns data of the user from the files
    :return:
    """

    if len(request.cookies) == 0 or not request.cookies['session_data'] or len(backend.data) == 0:
        raise HTTPException(status_code=404, detail="Session Not Found")

    session_data = eval(request.cookies['session_data'])

    if not backend.data[session_data['session']] == session_data['data']:
        raise HTTPException(status_code=404, detail="No session for current user")

    # Get first file in directory
    filename_to_read = sorted(os.listdir("./resources"))[0]
    data = pydicom.read_file("./resources/" + filename_to_read)['PatientName']
    return {"data": data.to_json()}

@app.get("/patient_image")
def patient_image(response: Response, request: Request, username: str):
    """
    Returns an image (middle slice) from the files of the user
    """

    if len(request.cookies) == 0 or not request.cookies['session_data'] or len(backend.data) == 0:
        raise HTTPException(status_code=404, detail="Session Not Found")

    session_data = eval(request.cookies['session_data'])

    if not backend.data[session_data['session']] == session_data['data']:
        raise HTTPException(status_code=404, detail="No session for current user")

    datasets = []

    for filename in os.listdir("./resources"):
        file_to_read = "./resources/" + filename
        if os.path.isfile(file_to_read):
            dataset = pydicom.dcmread(file_to_read)
            datasets.append(dataset)

    datasets = sorted(datasets, key=lambda s: s.SliceLocation)

    # Get middle slice
    list_size = len(datasets)
    position = (list_size // 2) - 1 if list_size % 2 == 0 else list_size // 2

    file_to_process = datasets[position]

    # Name for the file to be created
    filename = "./resources/images/middle_slice.png"

    # Convert data to png format
    pixel_array_data = file_to_process.pixel_array
    image = pixel_array_data.astype(float)
    rescaled_image = (numpy.maximum(image, 0) / image.max()) * 255.0
    rescaled_image = numpy.uint8(rescaled_image)

    # write image file
    final_image = Image.fromarray(rescaled_image)
    final_image.save(filename)
    return FileResponse(filename)


@app.on_event('startup')
def startup():
    """Initialize Connections pool"""
    for i in range(50):
        # TODO: Get database connection info from config file
        db_pool.add(Database('localhost', 'database', 'username', 'secret', 5432))


@app.on_event('shutdown')
def shutdown():
    """Close all connections in Connections pool"""
    for conn in db_pool:
        conn.close_connection()


# To run locally
if __name__ == '__main__':
    # Use a pool of connections to avoid waiting when a query is needed
    db_pool = set()

    try:
        uvicorn.run(app, host='0.0.0.0', port=8000)
    except Exception as e:
        print("Error executing server. Closing: \n {0}").format(e)

    print("Server finished!")
