from sqlalchemy import JSON, BigInteger, Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InferenceLog(Base):
    __tablename__ = "mlfoundry_inference_log"
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Identifying the model
    model_name = Column(String(256), nullable=False)
    model_version = Column(String(64), nullable=False)
    # identifying the inference payload
    inference_id = Column(String(36), nullable=False)
    features = Column(JSON, nullable=False)
    predictions = Column(JSON, nullable=False)
    occurred_at = Column(DateTime(), nullable=False)

    shap_values = Column(JSON)
    raw_data = Column(JSON)
    actuals = Column(JSON)
