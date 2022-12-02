from schemas.schemas import student_info,student_list,subject_info,student_subject_list,subject_list,teacher_list,All_student_subject_list,teacher_info
from Databases.db import db
# ,db2_,db3_,db4_
from fastapi import Body, HTTPException
from models.models import Student_info,Subject,student_subject,teacher
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI,Request
import json
from bson import json_util
from starlette.responses import JSONResponse, Response

# from routes import app
F_app = FastAPI()
# F_app.include_router(app)




@F_app.get("/")
async def Read_student():
    get_user= student_list(db.student.find())
    if len(get_user)==0:
        raise HTTPException(status_code=404, detail="item not found")
    return get_user
    # return {"test":"test"}







@F_app.get("/fetch_student/{id}")
async def get_one_student(id:str):
    try:
        data =db.student.find_one({"isDelete": 0,"_id":ObjectId(id)})
        if data != None:
            return student_info(dict(data))
        else:
            return HTTPException("No record found", status_code=400)
    except Exception as e:
        return HTTPException("Internal server error", status_code=500)






@F_app.post("/create_student/")
async def create_student(info_user:Student_info):
    try:
        item=jsonable_encoder(info_user)
        studentexist=json.loads(json_util.dumps(db.student.find({"name":item["name"],
            "address":item["address"],
            "contact":item["contact"],
            "standard":item["standard"]})))
        if not len(studentexist):
            _id=db.student.insert_one(dict(info_user))
            user=student_list(db.student.find({"_id":_id.inserted_id}))
            return {"status":"ok","data":user}
        else:
            return HTTPException(status_code=409,details="student already exists")
    except Exception as e:
        return HTTPException(detail="Internal server error", status_code=500)






@F_app.put("/update_student/{id}")
async def update_student(id:str,info_user:Student_info,):
    try:
        db.student.find_one_and_update({"_id":ObjectId(id)},
        {
            "$set":dict(info_user)
        })
        user= db.student.find({"_id":ObjectId(id)})
        return {"status":"ok","data":user}
    except Exception as e:
        return {"error":e}





@F_app.delete("/delete_student/{id}")
async def delete_student(id:str):
    db.student.find_one_and_delete({"_id":ObjectId(id)})
    return {"status":"ok"}
    

@F_app.post("/add_subject")
async def create_subject(info_user:Subject):
    _id=db.subject.insert_one(dict(info_user))
    list=subject_list(db.subject.find({"_id":_id.inserted_id}))
    return {"status":"ok","data":list}




@F_app.get("/display_subject/")
async def Read_subject():
    get_list= subject_list(db.subject.find())
    if get_list is None:
        raise HTTPException(status_code=404, detail="item not found")
    return get_list







@F_app.delete("/delete_subject/{id}")
async def delete_subject(id:str):
    user=db.subject.find_one_and_delete({"_id":ObjectId(id)})
    if user:
        return {"status":"ok"}
    else:
        raise HTTPException(status_code=404, detail="item not found")
        







@F_app.post("/create_student_subject/")
# async def create_student_subject(base:student_subject):
async def create_student_subject(base: student_subject = Body(...)):
    try:
        data=jsonable_encoder(base)
        # result = db.student_subject.find({"student_id":data["student_id"],"subject_id":data["subject_id"]})
        dataexist=json.loads(json_util.dumps(db.student_subject.find({"student_id":data["student_id"],"subject_id":data["subject_id"]})))
        if not len(dataexist):
            new_data=db.student_subject.insert_one({
                "student_id":ObjectId(data["student_id"]),
                "subject_id":ObjectId(data["subject_id"]),
                "isdelete": False
            })
        # user=All_student_subject_list(db.student_subject.find({"_id":new_data.inserted_id}))
            return {"status":"ok"}
        else:
            return HTTPException(status_code=409,details="student already exists")
        # return json.loads(json_util.dumps(result))
    except Exception as e:
        # return e
        return HTTPException(detail="Internal server error", status_code=500)
 




@F_app.get("/display_Student_subject/")
async def Read_Student_subject():
    try:
        result = db.student_subject.aggregate([
                {
                    "$lookup": {
                        "from": "student",
                        "localField": "id",
                        "foreignField": "student_id",
                        "as": "Student_Data"
                    }
                },
                {
                    "$lookup": {
                        "from": "subject",
                        "localField": "id",
                        "foreignField": "subject_id",
                        "as": "Subject_Data"
                    }
                },
                { "$unwind": { "path": "$Student_Data", "preserveNullAndEmptyArrays": True }},
                { "$unwind": { "path": "$Subject_Data", "preserveNullAndEmptyArrays": True }},
                {
                                "$project": {"Student_Data._id":1,"Student_Data.name":1,"Subject_Data._id":1,"Subject_Data.subject":1}
                                }
                    ])
        return json.loads(json_util.dumps(result))
        
    except Exception as e:
        return HTTPException(detail="internal server error", status_code=500)






@F_app.get("/student/{stu_id}")
async def get_one_student_subject(id:str):
    try:
        user= student_subject_list(db.student_subject.find_one({"_id":ObjectId(id)}))
        if user:
            return {"status":"ok","data":user}
        else:
            return HTTPException(status_code=409,details="teacher not found")
    except Exception as e:
        return HTTPException(detail="Interal server error", status_code=500)






@F_app.get("/getstudentbysubject/")
async def get_by_subject(subject:str):
    try:
        user= teacher_info(db.student_subject.find_one({"subject":subject}))
        if user:
            return {"status":"ok","data":user}
        else:
            return HTTPException(status_code=409,details="teacher not found")
    except Exception as e:
        return HTTPException(detail="Interal server error", status_code=500)













@F_app.post("/create_teacher_subject/")
async def create_teacher(main:teacher):
    try:
        data=jsonable_encoder(main)
        teacherexist=json.loads(json_util.dumps(db.teacher.find_one({"name":data["name"]})))

        if teacherexist is None:

            new_data=db.teacher.insert_one(dict(main))

            user=teacher_list(db.teacher.find({"_id":ObjectId(new_data.inserted_id)}))
            

            return {"status":"ok","data":user}

        else:
            return HTTPException(status_code=409,details="teacher already exists")
    except Exception as e:
        return HTTPException(detail="Internal server error", status_code=500)
 





@F_app.get("/teacher/{teacher_id}")
async def get_one_teacher_subject(id:str):
    try:
        user= teacher_info(db.teacher.find_one({"_id":ObjectId(id)}))
        if user:
            return {"status":"ok","data":user}
        else:
            return HTTPException(status_code=409,details="teacher not found")
    except Exception as e:
        return HTTPException(detail="Interal server error", status_code=500)









@F_app.get("/teacherbysubject/{subject}")
async def get_teacher_by_subject(subject:str):
    try:
        user= teacher_info(db.teacher.find_one({"subject":subject}))
        if user:
            return {"status":"ok","data":user}
        else:
            return HTTPException(status_code=409,details="teacher not found")
    except Exception as e:
        return HTTPException(detail="Interal server error", status_code=500)



    



    


@F_app.delete("/delete_teacher/{teacher_id}")
async def delete_teacher(id:str):
    try:
        user= teacher_info(db.teacher.find_one({"_id":ObjectId(id)}))
        if user:
            return {"status":"ok","data":user}
        else:
            return HTTPException(status_code=409,details="teacher not found")
    except Exception as e:
        return HTTPException(detail="Interal server error", status_code=500)


