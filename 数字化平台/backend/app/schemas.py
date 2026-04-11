from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- 1. 生化数据模式 ---
class BiochemCreate(BaseModel):
    experiment_id: int
    record_time: str
    sample_site: Optional[str] = None    # [新增]
    sample_source: str
    
    # 肝功能
    alt: Optional[float] = None
    ast: Optional[float] = None
    alb: Optional[float] = None
    tp: Optional[float] = None           # [新增]
    dbil: Optional[float] = None         # [新增]
    tbil: Optional[float] = None         # [新增]
    glob: Optional[float] = None         # [新增]
    ag_ratio: Optional[float] = None     # [新增]
    
    # 肾功能 & 代谢
    crea: Optional[float] = None         # [新增]
    ua: Optional[float] = None           # [新增]
    urea: Optional[float] = None         # [新增]
    urea_crea_ratio: Optional[float] = None # [新增]
    glu: Optional[float] = None
    
    # 血脂
    tg: Optional[float] = None           # [新增]
    tc: Optional[float] = None           # [新增]
    hdl: Optional[float] = None          # [新增]
    ldl: Optional[float] = None          # [新增]

class Biochem(BiochemCreate):
    id: int
    class Config:
        from_attributes = True

# --- 2. 血气数据模式 ---
class BloodGasCreate(BaseModel):
    experiment_id: int
    record_time: str
    sample_site: str
    ph: Optional[float] = None
    po2: Optional[float] = None
    pco2: Optional[float] = None
    lac: Optional[float] = None
    so2: Optional[float] = None
    
    # [新增]
    na: Optional[float] = None
    k: Optional[float] = None
    cl: Optional[float] = None
    ca: Optional[float] = None
    glu: Optional[float] = None
    hct: Optional[float] = None
    tco2: Optional[float] = None
    hb: Optional[float] = None
    hco3: Optional[float] = None
    be_ecf: Optional[float] = None
    be_b: Optional[float] = None
    an_gap: Optional[float] = None

class BloodGas(BloodGasCreate):
    id: int
    class Config:
        from_attributes = True

# --- 3. 基本信息模式 ---
class BasicInfoCreate(BaseModel):
    experiment_id: int
    
    # [新增] 实验日期
    record_date: Optional[str] = None
    
    total_duration: Optional[float] = None
    total_bile: Optional[float] = None
    liver_weight_pre: Optional[float] = None
    liver_weight_post: Optional[float] = None
    cold_ischemia_time: Optional[float] = None
    warm_ischemia_time: Optional[float] = None
    perfusion_liquid_vol: Optional[float] = None
    
    # [新增] 新字段
    donor_breed: Optional[str] = None
    gender: Optional[str] = None
    age_months: Optional[float] = None
    weight_kg: Optional[float] = None

class BasicInfo(BasicInfoCreate):
    id: int
    class Config:
        from_attributes = True

# --- 4. 统计信息模式 ---
class StatisticalInfoCreate(BaseModel):
    experiment_id: int
    fasting_time: Optional[float] = None
    anesthesia_method: Optional[str] = None
    heparin_dosage: Optional[float] = None
    acquisition_time: Optional[str] = None
    trimming_duration: Optional[float] = None
    liver_lobulation: Optional[str] = None
    gallbladder_status: Optional[str] = None
    cannulation_score: Optional[int] = None

class StatisticalInfo(StatisticalInfoCreate):
    id: int
    class Config:
        from_attributes = True

# --- 5. 灌注物理参数模式 ---
class PerfusionFile(BaseModel):
    id: int
    experiment_id: int
    filename: str
    file_path: str
    upload_time: str
    status: str

    class Config:
        from_attributes = True

class PerfusionMachineDataCreate(BaseModel):
    experiment_id: int
    file_id: Optional[int] = None
    record_time: Optional[str] = None
    pv_pressure: Optional[float] = None
    pv_flow: Optional[float] = None
    ha_pressure: Optional[float] = None
    ha_flow: Optional[float] = None
    temperature: Optional[float] = None

class PerfusionMachineData(PerfusionMachineDataCreate):
    id: int
    class Config:
        from_attributes = True

# --- 6. 影像资料模式 ---
class MediaCreate(BaseModel):
    experiment_id: int
    record_time: float
    file_type: str
    file_path: str
    original_filename: str

class Media(MediaCreate):
    id: int
    class Config:
        from_attributes = True

# --- 8. 专家记录模式 ---
class ExpertDescriptionCreate(BaseModel):
    experiment_id: int
    record_time: str
    description: str

class ExpertDescription(ExpertDescriptionCreate):
    id: int
    class Config:
        from_attributes = True

class OperationLogCreate(BaseModel):
    experiment_id: int
    operation_details: str
    operation_reason: str

class OperationLog(OperationLogCreate):
    id: int
    class Config:
        from_attributes = True

# --- 实验模式 (最后定义，因为包含上面的子模式) ---
class ExperimentBase(BaseModel):
    experiment_code: str
    experiment_date: Optional[datetime] = None

class ExperimentCreate(ExperimentBase):
    pass

class Experiment(ExperimentBase):
    id: int
    biochems: List[Biochem] = []
    blood_gases: List[BloodGas] = []
    basic_infos: List[BasicInfo] = []
    statistical_infos: List[StatisticalInfo] = []
    perfusion_files: List[PerfusionFile] = []
    medias: List[Media] = []
    expert_descriptions: List[ExpertDescription] = []
    operation_logs: List[OperationLog] = []
    
    class Config:
        from_attributes = True