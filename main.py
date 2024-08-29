#This file is used to create functions or classes that visualize how a route will operate.

from sqlalchemy.orm import Session

import json

from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from schema import UserData as SchemaUser

from models import User as ModelUserInfo


import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

DATABASE_URL = os.environ['DATABASE_URL']

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/dialogflow")
async def handle_dialogflow(request: Request):
    try:
        # Parse the incoming request
        data = await request.json()
        # print("Received request data:", json.dumps(data, indent=4))  # Log the received data for debugging
        #
        # # Extract userId and name from the nested structure
        session_info = data.get("sessionInfo", {})
        parameters = session_info.get("parameters", {})

        user_id = parameters["userid"]
        name = parameters["name"]

        # Check if userId and name are present
        if not user_id or not name:
            return {"fulfillment_response": {
                "messages": [
                    {"text": {"text": ["Missing userId or name in parameters."]}}
                ]
            }}

        # Save user data to the database
        db_user = ModelUserInfo(user_id=user_id, name=name)
        db.session.add(db_user)
        db.session.commit()

        # Respond back to Dialogflow
        return {"fulfillment_response": {
            "messages": [
                {"text": {"text": [f"User {name} with ID {user_id} saved successfully."]}}
            ]
        }}

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        return {"fulfillment_response": {
            "messages": [
                {"text": {"text": [f"Failed to save user data. Error: {str(e)}"]}}
            ]
        }}


# @app.post("/dialogflow")
# async def handle_dialogflow(request: Request):
#     try:
#         # Extract data from the request body
#         data = await request.json()
#
#         # Retrieve the user ID and name from Dialogflow's JSON request
#         user_id = data['sessionInfo']['parameters']['userId'] # 'userId' is the parameter name in schema.py?
#         name = data['sessionInfo']['parameters']['name']
#
#         # user_id = data['userId']  # 'userId' is the parameter name in schema.py?
#         # name = data['name']
#
#         # Create a new user object
#         db_user = ModelUserInfo(user_id=user_id, name=name)
#         # Store in the database
#         db.session.add(db_user)
#         db.session.commit()
#
#         # with SessionLocal() as session:
#         #     user = SchemaUser(userId=user_id, name=name)
#         #     session.add(user)
#         #     session.commit()
#
#         # Return success message to Dialogflow CX
#         return {
#             "fulfillment_response": {
#                 "messages": [
#                     {"text": {"text": [f"User {name} with ID {user_id} saved successfully."]}}
#                 ]
#             }
#         }
#     except Exception as e:
#         return {
#             "fulfillment_response": {
#                 "messages": [
#                     {"text": {"text": [f"Failed to save user data. Error: {str(e)}"]}}
#                 ]
#             }
#         }


@app.post('/user/')
async def user(user: SchemaUser):
    db_user = ModelUserInfo(user_id=user.userId, name=user.name) #this should be from the schema
    db.session.add(db_user)
    db.session.commit()
    return db_user


@app.get('/dialogflow/')
async def user():
    user = db.session.query(ModelUserInfo).all() #this should be from models
    return user






#run the app locally
if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO)
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)
    # ssl = {"keyfile": "certificates/private.key", "certfile": "certificates/server.crt"}
    # uvicorn.run(
    #     app,
    #     host="127.0.0.1",
    #     port=8000,
    #     ssl_keyfile=ssl["keyfile"],
    #     ssl_certfile=ssl["certfile"],
    # )
    # uvicorn.run("app.main:app",
    #             host="127.0.0.1",
    #             port=5000,
    #             reload=True,
    #             ssl_keyfile="./localhost+2-key.pem",
    #             ssl_certfile="./localhost+2.pem"
    #             )
