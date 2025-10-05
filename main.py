from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated,Literal,Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str, Field(..., description = "ID of the patient.", examples=['P001'])]
    name : Annotated[str, Field(..., description="Name of the patient.")]
    city : Annotated[str, Field(..., description = "name of city where patient lives")]
    age : Annotated[int, Field(..., gt=0, lt=120, description="age of the patient")]
    gender : Annotated[Literal['male','female','others'], Field(..., description="gender of the patient")]
    height : Annotated[float, Field(..., description = "height of the patient in metres")]
    weight : Annotated[float, Field(..., description = "weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round((self.weight/self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi <25 :
            return "Normal"
        elif self.bmi < 40 :
            return "Normal"
        else:
            return "obese"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]



def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data,f)


@app.get("/")
def hello():
    return{"message":"Patient Management System API"}

@app.get("/about")
def about():
    return({"A fully functional API to manage your patient record."})

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(..., description="ID of the patient",example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail = "Patient not found.")

@app.get("/sort")
def sort_patient(sort_by:str = Query(..., description="sort on the basis of heigh,weight,bmi"),order: str = Query("asc",description="sort in asc or desc order")):
    
    valid_fields=['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'invalid field select from {valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail = 'sort in asc or desc order')
    
    data =load_data()
    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: PatientUpdate):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exist")

    data[patient.id] = patient.model_dump(exclude = ['id'])

    save_data(data)

    return JSONResponse(status_code=200 , content={"message":"patient created successfully"})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')
    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})
