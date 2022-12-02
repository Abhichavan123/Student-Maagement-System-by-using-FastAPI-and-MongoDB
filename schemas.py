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



def student_info(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name":str(item["name"]),
        "address":str(item["address"]),
        "contact":str(item["contact"]),
        "standard":str(item["standard"])
    }




def student_list(info)->list:
    user_list=[student_info(item) for item in info]
    return user_list






def subject_info(sub)-> dict:
    return {
        "subject_id":str(sub["_id"]),
        "subject":sub["subject"],
        }

def subject_list(each) -> list:
    subject_data=[subject_info(sub) for sub in each]
    return subject_data








def student_subject_list(data) ->dict:
    return {
        "stud_id":str(data["_id"]),
        "student_id":data["student_id"],
        "subject_id":data["subject_id"],
        


    }

def All_student_subject_list(All) -> list:
    sub_data=[student_subject_list(data) for data in All]
    return sub_data








def teacher_info(Teach) -> dict :
    return {
        "teacher_id":str(Teach["_id"]),
        "name":Teach["name"],
        "subject":str(Teach["subject"]),
        "sub_id":str(PyObjectId(Teach["sub_id"]))

    }




def teacher_list(all) -> list:
    teacher_data=[teacher_info(Teach) for Teach in all]
    return teacher_data