# -*- coding: utf-8 -*-
# 文件名: app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ---------------------------------------------------------
# 1. 动态计算数据库路径 (跨平台兼容)
# ---------------------------------------------------------
# 获取当前文件 (database.py) 的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 'app' directory
BACKEND_DIR = os.path.dirname(BASE_DIR)              # 'backend' directory
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)           # project root

# Final path: .../data/hospital_demo.db
DB_FILE_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, "data", "hospital_demo.db"))

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)

# ---------------------------------------------------------
# 2. 数据库连接配置
# ---------------------------------------------------------
# SQLite 路径处理：Windows 下需要处理驱动器号，SQLAlchemy 推荐使用绝对路径
# 在 Windows 上绝对路径通常是 sqlite:///C:\path\to\db
# 在 Mac/Linux 上是 sqlite:////path/to/db
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"

print(f"📍 数据库文件路径已定位至: {DB_FILE_PATH}")

# ---------------------------------------------------------
# 3. 创建引擎与会话 (原样保留)
# ---------------------------------------------------------
# check_same_thread=False 必须保留，否则 SQLite 在 FastAPI 多线程下会报错
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()