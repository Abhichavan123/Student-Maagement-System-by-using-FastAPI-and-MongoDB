from pydantic import BaseModel,Field,EmailStr
from typing import Optional
from bson.objectid import ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Student_info(BaseModel):
    
    name:str=Field(name="abhi chavan",max_length=100)
    address:str=Field(max_length=300)
    contact:int
    email:EmailStr=Field(email="xyz@gmail.com")
    standard:int=Field(gt=0,lt=12)
    isdelete:Optional[int]=False



    class Config:
        schema_extra = {
            "example": {
                "name": "abhi chavan",
                "address":"satara",
                "contact":8388383838,
                "email": "chavanabhi97@gmail.com",
                "standard":9
            }
        }







class Subject(BaseModel):
    subject:str=Field(max_length=50)
    isdelete:Optional[int]=0

    class Config:
        schema_extra = {
            "example": {
                "subject":"marathi",

            }
        }
    







class student_subject(BaseModel):
    
    student_id: PyObjectId = Field(default_factory=PyObjectId, alias="student_id")
    subject_id: PyObjectId = Field(default_factory=PyObjectId, alias="subject_id")
    isdelete:Optional[int]=False

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "student_id":"6384c34154624b260cf18b47",
                "subject_id":"638593ed8026a81951e64b78"
               
            }
        }



    

class teacher(BaseModel):
    name:str=Field(name="ankush ",max_length=100)
    subject:str=Field(max_length=50)
    isdelete:Optional[int]=False
    sub_id: PyObjectId = Field(default_factory=PyObjectId, alias="sub_id")
    

    class Config:
        schema_extra = {
            "example": {
                "name": "ankush",
                "subject":"marathi"
            }
        }