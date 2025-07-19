from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class FileConversion(Base):
    __tablename__ = "file_conversions"
    
    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String(255), nullable=False)
    original_path = Column(String(255), nullable=False)
    converted_path = Column(String(255), nullable=False)
    conversion_type = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
