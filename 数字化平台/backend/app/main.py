from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas, database
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import openpyxl
from io import BytesIO
from typing import List
import shutil
from datetime import datetime

# 自动建表
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取当前文件所在目录，确保静态资源路径在迁移后依然正确
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(BASE_DIR)
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
STATIC_DIR = os.path.join(BASE_DIR, "static")
ASSETS_DIR = os.path.join(STATIC_DIR, "assets")

# 1. 挂载静态资源目录
if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

# 2. 根目录返回 index.html
@app.get("/")
async def read_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not deployed."}

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- [新增] 专门用于查询的接口 ---
@app.get("/experiments/{code}", response_model=schemas.Experiment)
def read_experiment(code: str, db: Session = Depends(get_db)):
    db_exp = db.query(models.Experiment).filter(models.Experiment.experiment_code == code).first()
    if db_exp is None:
        # 没找到时返回 404，前端以此为标志弹出对话框
        raise HTTPException(status_code=404, detail="Experiment not found")
    return db_exp

@app.get("/experiments/", response_model=List[schemas.Experiment])
def read_experiments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    experiments = db.query(models.Experiment).offset(skip).limit(limit).all()
    return experiments

# 1. 创建或获取实验 (保持不变，用于新建)
@app.post("/experiments/", response_model=schemas.Experiment)
def create_or_get_experiment(experiment: schemas.ExperimentCreate, db: Session = Depends(get_db)):
    db_exp = db.query(models.Experiment).filter(models.Experiment.experiment_code == experiment.experiment_code).first()
    if db_exp:
        return db_exp
    new_exp = models.Experiment(experiment_code=experiment.experiment_code)
    db.add(new_exp)
    db.commit()
    db.refresh(new_exp)
    return new_exp

# 2. 录入数据
@app.post("/biochem/", response_model=schemas.Biochem)
def create_biochem(data: schemas.BiochemCreate, db: Session = Depends(get_db)):
    db_data = models.BiochemData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.put("/biochem/{id}", response_model=schemas.Biochem)
def update_biochem(id: int, data: schemas.BiochemCreate, db: Session = Depends(get_db)):
    db_data = db.query(models.BiochemData).filter(models.BiochemData.id == id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Biochem record not found")
    
    for key, value in data.dict().items():
        setattr(db_data, key, value)
    
    db.commit()
    db.refresh(db_data)
    return db_data

# --- [新增] 基本信息接口 ---
@app.post("/basic-info/", response_model=schemas.BasicInfo)
def create_basic_info(data: schemas.BasicInfoCreate, db: Session = Depends(get_db)):
    # 存入数据库
    db_data = models.BasicInfoData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.put("/basic-info/{id}", response_model=schemas.BasicInfo)
def update_basic_info(id: int, data: schemas.BasicInfoCreate, db: Session = Depends(get_db)):
    db_data = db.query(models.BasicInfoData).filter(models.BasicInfoData.id == id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Basic info not found")
    
    # Update fields
    for key, value in data.dict().items():
        setattr(db_data, key, value)
    
    db.commit()
    db.refresh(db_data)
    return db_data

@app.post("/bloodgas/", response_model=schemas.BloodGas)
def create_bloodgas(data: schemas.BloodGasCreate, db: Session = Depends(get_db)):
    db_data = models.BloodGasData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.put("/bloodgas/{id}", response_model=schemas.BloodGas)
def update_bloodgas(id: int, data: schemas.BloodGasCreate, db: Session = Depends(get_db)):
    db_data = db.query(models.BloodGasData).filter(models.BloodGasData.id == id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Blood gas record not found")
    
    for key, value in data.dict().items():
        setattr(db_data, key, value)
    
    db.commit()
    db.refresh(db_data)
    return db_data

# --- [新增] 统计信息接口 ---
@app.post("/statistical-info/", response_model=schemas.StatisticalInfo)
def create_statistical_info(data: schemas.StatisticalInfoCreate, db: Session = Depends(get_db)):
    db_data = models.StatisticalInfoData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.put("/statistical-info/{id}", response_model=schemas.StatisticalInfo)
def update_statistical_info(id: int, data: schemas.StatisticalInfoCreate, db: Session = Depends(get_db)):
    db_data = db.query(models.StatisticalInfoData).filter(models.StatisticalInfoData.id == id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Statistical info not found")
    
    for key, value in data.dict().items():
        setattr(db_data, key, value)
    
    db.commit()
    db.refresh(db_data)
    return db_data

@app.delete("/statistical-info/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_statistical_info(id: int, db: Session = Depends(get_db)):
    record = db.query(models.StatisticalInfoData).filter(models.StatisticalInfoData.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(record)
    db.commit()
    return None

# 3. 删除接口
@app.delete("/biochem/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_biochem(id: int, db: Session = Depends(get_db)):
    record = db.query(models.BiochemData).filter(models.BiochemData.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    db.delete(record)
    db.commit()
    return None

@app.delete("/bloodgas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bloodgas(id: int, db: Session = Depends(get_db)):
    record = db.query(models.BloodGasData).filter(models.BloodGasData.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    db.delete(record)
    db.commit()
    return None

@app.delete("/basic-info/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_basic_info(id: int, db: Session = Depends(get_db)):
    # 删除记录
    record = db.query(models.BasicInfoData).filter(models.BasicInfoData.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(record)
    db.commit()
    return None

# --- [新增] 灌注物理参数接口 ---
EXCEL_ROOT = os.getenv("EXCEL_ROOT", os.path.join(PROJECT_ROOT, "storage", "source", "excel"))
os.makedirs(EXCEL_ROOT, exist_ok=True)

@app.post("/experiments/{experiment_id}/perfusion-machine-data/upload")
async def upload_perfusion_machine_data(
    experiment_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # 1. 保存文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    save_path = os.path.join(EXCEL_ROOT, safe_filename)
    
    contents = await file.read()
    with open(save_path, "wb") as f:
        f.write(contents)

    # 2. 创建文件记录
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_file = models.PerfusionFile(
        experiment_id=experiment_id,
        filename=file.filename,
        file_path=safe_filename, # Store filename/relative path
        upload_time=upload_time,
        status="已转化" # Default status since we process immediately
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    try:
        # 3. 解析Excel并入库
        wb = openpyxl.load_workbook(filename=BytesIO(contents))
        ws = wb.active
        
        # Assuming first row is header, skip it
        rows = ws.iter_rows(min_row=2, values_only=True)
        
        records = []
        for row in rows:
            # row structure:
            # Index: 0=None, 1=Time, 2=PV_P, 3=PV_F, 4=HA_P, 5=HA_F, 6=Temp
            
            # Check if row has enough columns
            if len(row) < 7:
                continue

            if not row[1]: # Skip empty rows if time is missing
                continue
                
            record_time = row[1]
            # Convert datetime to string if it is a datetime object
            if hasattr(record_time, 'strftime'):
                record_time = record_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                record_time = str(record_time)

            data = models.PerfusionMachineData(
                experiment_id=experiment_id,
                file_id=db_file.id, # Link to file
                record_time=record_time,
                pv_pressure=float(row[2]) if row[2] is not None else None,
                pv_flow=float(row[3]) if row[3] is not None else None,
                ha_pressure=float(row[4]) if row[4] is not None else None,
                ha_flow=float(row[5]) if row[5] is not None else None,
                temperature=float(row[6]) if row[6] is not None else None,
            )
            db.add(data)
            records.append(data)
        
        db.commit()
        return {"message": f"Successfully uploaded {len(records)} records"}
    except Exception as e:
        # If parsing fails, update status (optional, but good practice)
        db_file.status = "转化失败"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to parse file: {str(e)}")

@app.get("/experiments/{experiment_id}/perfusion-files", response_model=List[schemas.PerfusionFile])
def read_perfusion_files(experiment_id: int, db: Session = Depends(get_db)):
    return db.query(models.PerfusionFile).filter(models.PerfusionFile.experiment_id == experiment_id).all()

@app.delete("/perfusion-files/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_perfusion_file(id: int, db: Session = Depends(get_db)):
    file_record = db.query(models.PerfusionFile).filter(models.PerfusionFile.id == id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File record not found")
    
    # Delete actual file
    full_path = os.path.join(EXCEL_ROOT, file_record.file_path)
    if os.path.exists(full_path):
        os.remove(full_path)
    
    # Delete DB record (cascade deletes machine_data)
    db.delete(file_record)
    db.commit()
    return None

@app.get("/perfusion-files/{id}/data", response_model=List[schemas.PerfusionMachineData])
def read_perfusion_file_data(id: int, db: Session = Depends(get_db)):
    # Verify file exists (optional)
    return db.query(models.PerfusionMachineData).filter(models.PerfusionMachineData.file_id == id).all()

@app.get("/perfusion-files/{id}/json")
def download_perfusion_file_json(id: int, db: Session = Depends(get_db)):
    file_record = db.query(models.PerfusionFile).filter(models.PerfusionFile.id == id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
        
    data = db.query(models.PerfusionMachineData).filter(models.PerfusionMachineData.file_id == id).all()
    
    # Convert to list of dicts
    result = []
    for item in data:
        result.append({
            "record_time": item.record_time,
            "pv_pressure": item.pv_pressure,
            "pv_flow": item.pv_flow,
            "ha_pressure": item.ha_pressure,
            "ha_flow": item.ha_flow,
            "temperature": item.temperature
        })
    
    from fastapi.responses import JSONResponse
    from urllib.parse import quote
    
    # URL encode the filename to handle non-ASCII characters (e.g., Chinese)
    encoded_filename = quote(file_record.filename)
    
    return JSONResponse(
        content=result,
        # Use filename*=UTF-8''... for modern browsers to support non-ASCII filenames
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}.json"}
    )

# --- [新增] 影像资料接口 ---
MEDIA_ROOT = os.getenv("MEDIA_ROOT", os.path.join(PROJECT_ROOT, "storage", "source"))
os.makedirs(MEDIA_ROOT, exist_ok=True)

app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")

@app.post("/experiments/{experiment_id}/media/upload", response_model=schemas.Media)
async def upload_media(
    experiment_id: int,
    file: UploadFile = File(...),
    file_type: str = Form(...), # macro, infrared, video, pathology
    record_time: float = Form(...),
    db: Session = Depends(get_db)
):
    # 1. 验证 file_type
    valid_types = ["macro", "infrared", "video", "pathology"]
    if file_type not in valid_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 2. 构建保存路径
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    
    # 相对路径 (存入数据库)
    relative_path = f"{file_type}/{safe_filename}"
    
    # 绝对路径 (用于保存)
    save_dir = os.path.join(MEDIA_ROOT, file_type)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    save_path = os.path.join(save_dir, safe_filename)
    
    # 3. 保存文件
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 4. 存入数据库
    db_media = models.MediaData(
        experiment_id=experiment_id,
        record_time=record_time,
        file_type=file_type,
        file_path=relative_path, # 存相对路径
        original_filename=file.filename
    )
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    
    return db_media

@app.get("/experiments/{experiment_id}/media", response_model=List[schemas.Media])
def read_media(experiment_id: int, db: Session = Depends(get_db)):
    return db.query(models.MediaData).filter(models.MediaData.experiment_id == experiment_id).all()

@app.delete("/media-records/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_media(id: int, db: Session = Depends(get_db)):
    record = db.query(models.MediaData).filter(models.MediaData.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(record)
    db.commit()
    return None

# --- [新增] 专家记录 & 操作日志接口 ---

# 1. 专家主观描述
@app.post("/experiments/{experiment_id}/expert-descriptions", response_model=schemas.ExpertDescription)
def create_expert_description(experiment_id: int, description: schemas.ExpertDescriptionCreate, db: Session = Depends(get_db)):
    db_desc = models.ExpertDescription(**description.dict())
    # 确保 experiment_id 一致（虽然前端传了，但通常以 path param 为准或校验）
    db_desc.experiment_id = experiment_id 
    db.add(db_desc)
    db.commit()
    db.refresh(db_desc)
    return db_desc

@app.delete("/expert-descriptions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expert_description(id: int, db: Session = Depends(get_db)):
    record = db.query(models.ExpertDescription).filter(models.ExpertDescription.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
    return None

# 2. 干预与操作日志
@app.post("/experiments/{experiment_id}/operation-logs", response_model=schemas.OperationLog)
def create_operation_log(experiment_id: int, log: schemas.OperationLogCreate, db: Session = Depends(get_db)):
    db_log = models.OperationLog(**log.dict())
    db_log.experiment_id = experiment_id
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.delete("/operation-logs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operation_log(id: int, db: Session = Depends(get_db)):
    record = db.query(models.OperationLog).filter(models.OperationLog.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
    return None
