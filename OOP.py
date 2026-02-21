from pydantic import BaseModel, Field,EmailStr,ConfigDict



data = {
    "email": "abc@gmail.com",
    "bio": "12424243",

}


data2 = {
"email": "ab@gmail.com",
    "bio": None,
    "age": 12,
}


class UserWoAge(BaseModel):
    email: str
    bio: str | None = Field(max_length=15)

    model_config = ConfigDict(extra="forbid")


class UserWithAge(UserWoAge):
    age: int = Field(ge=0, le=130)



print(repr(UserWoAge(**data)))
print(repr(UserWithAge(**data2)))