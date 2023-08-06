from sqlalchemy import JSON, Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InferenceLog(Base):
    __tablename__ = "mlfoundry_inference_log"

    # Identifying the model
    run_id = Column(String(36), primary_key=True)
    # identifying the inference payload
    inference_id = Column(String(36), primary_key=True)
    features = Column(JSON, nullable=False)
    predictions = Column(JSON, nullable=False)
    occurred_at = Column(DateTime(), nullable=False)

    shap_values = Column(JSON)
    raw_data = Column(JSON)
    actuals = Column(JSON)
