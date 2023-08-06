import typing

import orjson
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ..inference_packet import InferencePacket
from .abstract_inference_store import AbstractInferenceStore
from .db_models import Base, InferenceLog


def orjson_serializer(obj):
    return orjson.dumps(obj, option=orjson.OPT_SERIALIZE_NUMPY).decode()


def orjson_deserializer(serialized_obj):
    return orjson.loads(serialized_obj)


def create_sqlalchemy_engine(db_uri: str) -> Engine:
    engine = create_engine(
        db_uri, json_serializer=orjson_serializer, json_deserializer=orjson_deserializer
    )
    return engine


# NOTE: for now I am keeping the above helper function in this file,
# later we may need to create a seperate db util file to keep this functions


class SqlAlchemyInferenceStore(AbstractInferenceStore):
    def __init__(self, db_uri: str):
        self.engine: Engine = create_sqlalchemy_engine(db_uri)

        # TODO: Explore albemic later
        Base.metadata.create_all(self.engine)
        self.session = scoped_session(sessionmaker(self.engine))

    def batch_log_inference(self, inference_packets: typing.List[InferencePacket]):
        with self.session() as session, session.begin():
            # https://github.com/sqlalchemy/sqlalchemy/issues/6519
            inference_log_objects = [
                InferenceLog(
                    model_name=inference.model_name,
                    model_version=inference.model_version,
                    inference_id=inference.inference_id,
                    features=inference.features,
                    predictions=inference.predictions,
                    occurred_at=inference.occurred_at,
                    raw_data=inference.raw_data,
                    actuals=inference.actuals,
                    shap_values=inference.shap_values,
                )
                for inference in inference_packets
            ]
            session.add_all(inference_log_objects)
