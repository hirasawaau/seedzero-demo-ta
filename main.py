from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from model import ProfileBody
from db import Profile
from typing import List
app = FastAPI()


@app.on_event("startup")
async def startup():
  client = AsyncIOMotorClient("mongodb://localhost:27017")

  await init_beanie(database=client.somchai, document_models=[Profile])


@app.post("/profiles", status_code=201)
async def create_profile(profile_body: ProfileBody) -> Profile:
  profile = Profile(**profile_body.model_dump())
  await profile.insert()
  return profile


@app.get('/profiles')
async def get_profiles() -> List[Profile]:
  profiles = await Profile.find().to_list()
  return profiles


@app.get("/profiles/{id}")
async def get_profile(id: str) -> Profile:
  profile = await Profile.get(id)
  return profile


@app.put("/profiles/{id}", status_code=204)
async def replace_profile(id: str, profile_body: ProfileBody):
  profile = await Profile.get(id)
  profile.name = profile_body.name
  profile.surname = profile_body.surname
  profile.age = profile_body.age

  await profile.save()

@app.delete("/profiles/{id}", status_code=204)
async def delete_profile(id: str):
  profile = await Profile.get(id)
  await profile.delete()
  
