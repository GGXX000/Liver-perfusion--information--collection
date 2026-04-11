from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_code = Column(String, unique=True, index=True)
    experiment_date = Column(DateTime, default=datetime.now)
    
    biochems = relationship("BiochemData", back_populates="experiment")
    blood_gases = relationship("BloodGasData", back_populates="experiment")
    basic_infos = relationship("BasicInfoData", back_populates="experiment")
    statistical_infos = relationship("StatisticalInfoData", back_populates="experiment")
    perfusion_files = relationship("PerfusionFile", back_populates="experiment")
    perfusion_machines = relationship("PerfusionMachineData", back_populates="experiment")
    medias = relationship("MediaData", back_populates="experiment")
    expert_descriptions = relationship("ExpertDescription", back_populates="experiment")
    operation_logs = relationship("OperationLog", back_populates="experiment")

class ExpertDescription(Base):
    __tablename__ = "data_expert_description"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    record_time = Column(String)  # T=x h
    description = Column(String)  # 专家主观描述
    
    experiment = relationship("Experiment", back_populates="expert_descriptions")

class OperationLog(Base):
    __tablename__ = "data_operation_log"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    # log_time = Column(String) # Removed per user request
    operation_details = Column(String)
    operation_reason = Column(String)
    
    experiment = relationship("Experiment", back_populates="operation_logs")

class BiochemData(Base):
    __tablename__ = "data_biochem"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    record_time = Column(String)
    sample_site = Column(String)    # [新增] 采样部位 (PV/IVC)
    sample_source = Column(String)  # [新增] 来源 (OnSite/Lab)
    
    # 肝功能
    alt = Column(Float)             # ALT (U/L)
    ast = Column(Float)             # AST (U/L)
    alb = Column(Float)             # 白蛋白 (g/dL)
    tp = Column(Float)              # [新增] 总蛋白 (g/dL)
    dbil = Column(Float)            # [新增] 直接胆红素 (umol/L)
    tbil = Column(Float)            # [新增] 总胆红素 (umol/L)
    glob = Column(Float)            # [新增] 球蛋白 (g/dL)
    ag_ratio = Column(Float)        # [新增] 白球比值
    
    # 肾功能 & 代谢
    crea = Column(Float)            # [新增] 肌酐 (umol/L)
    ua = Column(Float)              # [新增] 尿酸 (umol/L)
    urea = Column(Float)            # [新增] 尿素 (mmol/L)
    urea_crea_ratio = Column(Float) # [新增] 尿素/肌酐比值
    glu = Column(Float)             # 葡萄糖 (mmol/L)
    
    # 血脂
    tg = Column(Float)              # [新增] 甘油三酯 (mmol/L)
    tc = Column(Float)              # [新增] 总胆固醇 (mmol/L)
    hdl = Column(Float)             # [新增] HDL-C (mmol/L)
    ldl = Column(Float)             # [新增] LDL-C (mmol/L)
    
    experiment = relationship("Experiment", back_populates="biochems")

class BloodGasData(Base):
    __tablename__ = "data_blood_gas"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    record_time = Column(String)
    sample_site = Column(String)
    ph = Column(Float)
    po2 = Column(Float)
    pco2 = Column(Float)
    lac = Column(Float)
    so2 = Column(Float)
    
    # [新增] 电解质
    na = Column(Float)      # 钠离子 (mmol/L)
    k = Column(Float)       # 钾离子 (mmol/L)
    cl = Column(Float)      # 氯离子 (mmol/L)
    ca = Column(Float)      # 钙离子 (mmol/L)
    
    # [新增] 代谢物 & 其他
    glu = Column(Float)     # 葡萄糖 (mmol/L)
    hct = Column(Float)     # 红细胞压积 (%PCV)
    tco2 = Column(Float)    # 总二氧化碳 (mmol/L)
    hb = Column(Float)      # 血红蛋白 (g/dL)
    hco3 = Column(Float)    # 碳酸氢根 (mmol/L)
    be_ecf = Column(Float)  # 细胞外液碱剩余 (mmol/L)
    be_b = Column(Float)    # 血中碱剩余 (mmol/L)
    an_gap = Column(Float)  # 阴离子间隙 (mmol/L)

    experiment = relationship("Experiment", back_populates="blood_gases")

# --- 基本信息表 ---
class BasicInfoData(Base):
    __tablename__ = "data_basic_info"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    
    # [新增] 0. 实验日期 (放在第一位)
    record_date = Column(String) 
    
    # 1. 总灌注时间
    total_duration = Column(Float)
    # 2. 总胆汁量
    total_bile = Column(Float)
    # 3. 灌注前肝脏质量
    liver_weight_pre = Column(Float)
    # 4. 灌注后肝脏质量
    liver_weight_post = Column(Float)
    # 5. 冷缺血时间
    cold_ischemia_time = Column(Float)
    # 6. 热缺血时间
    warm_ischemia_time = Column(Float)
    # 7. 灌注液体系量
    perfusion_liquid_vol = Column(Float)
    
    # [新增] 8. 供体品种
    donor_breed = Column(String)
    # [新增] 9. 性别
    gender = Column(String)
    # [新增] 10. 月龄 (月)
    age_months = Column(Float)
    # [新增] 11. 体重 (kg)
    weight_kg = Column(Float)

    experiment = relationship("Experiment", back_populates="basic_infos")

# --- 统计信息表 ---
class StatisticalInfoData(Base):
    __tablename__ = "data_statistical_info"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))

    # 1. 术前禁食时间 (h)
    fasting_time = Column(Float)
    # 2. 麻醉方式
    anesthesia_method = Column(String)
    # 3. 肝素化剂量 (mg/kg)
    heparin_dosage = Column(Float)
    # 4. 取肝时间 (09:30AM)
    acquisition_time = Column(String)
    # 5. 修肝时长 (min)
    trimming_duration = Column(Float)
    # 6. 肝脏分叶情况
    liver_lobulation = Column(String)
    # 7. 胆囊状态 (切除/保留)
    gallbladder_status = Column(String)
    # 8. 插管质量评分 (1-5)
    cannulation_score = Column(Integer)

    experiment = relationship("Experiment", back_populates="statistical_infos")

# --- 灌注物理参数文件记录表 ---
class PerfusionFile(Base):
    __tablename__ = "data_perfusion_files"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    filename = Column(String)
    file_path = Column(String) # 绝对路径
    upload_time = Column(String)
    status = Column(String) # "converted", "error"

    experiment = relationship("Experiment", back_populates="perfusion_files")
    machine_data = relationship("PerfusionMachineData", back_populates="file", cascade="all, delete-orphan")


# --- 灌注物理参数表 ---
class PerfusionMachineData(Base):
    __tablename__ = "data_perfusion_machine"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    file_id = Column(Integer, ForeignKey("data_perfusion_files.id")) # 关联到文件
    record_time = Column(String) # 灌注时间
    pv_pressure = Column(Float)  # 门静脉灌注压力（mmHg）
    pv_flow = Column(Float)      # 门静脉灌注流量（ml/min）
    ha_pressure = Column(Float)  # 肝动脉灌注压力（mmHg）
    ha_flow = Column(Float)      # 肝动脉灌注流量（ml/min）
    temperature = Column(Float)  # 灌注液温度（℃）

    experiment = relationship("Experiment", back_populates="perfusion_machines")
    file = relationship("PerfusionFile", back_populates="machine_data")

# --- 影像资料表 ---
class MediaData(Base):
    __tablename__ = "data_media"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    
    record_time = Column(Float)      # 时间点 T= (h)
    file_type = Column(String)       # 类型: macro, infrared, video, pathology
    file_path = Column(String)       # 相对路径
    original_filename = Column(String) # 原始文件名
    
    experiment = relationship("Experiment", back_populates="medias")