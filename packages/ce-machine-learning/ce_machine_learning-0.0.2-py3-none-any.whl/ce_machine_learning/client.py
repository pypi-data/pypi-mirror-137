import base64

import grpc
from google.protobuf.pyext._message import Message, RepeatedCompositeContainer

from .gen import ce_machine_learning_pb2 as gen
from .gen import ce_machine_learning_pb2_grpc as gen_grpc
from .gen import model


def create_stub(server_url):  # pragma: no cover
    if not server_url:
        server_url = "localhost:50051"
    channel = grpc.insecure_channel(server_url)
    return gen_grpc.CeMachineLearningStub(channel)


def grpc_to_dict(grpc_resp) -> dict:
    def transform_data(data):
        if isinstance(data, RepeatedCompositeContainer):
            return [transform_data(d) for d in data]
        if isinstance(data, Message):
            return {d[0].name: transform_data(d[1]) for d in data.ListFields()}
        return data

    return transform_data(grpc_resp[0])


class Client:
    _stub = None  # type: gen_grpc.CeMachineLearningStub

    def __init__(self, server_url=None):
        if not self._stub:
            self._stub = create_stub(server_url)

    def create_process(self, request: model.CreateProcessValidationRequest):
        result = self._stub.CreateProcessValidation.with_call(
            gen.CreateProcessValidationRequest(**request.dict())
        )
        return model.CreateProcessValidationResponse(**grpc_to_dict(result))

    def audio_validation(
        self, request: model.AudioValidationRequest
    ) -> model.AudioValidationResponse:
        dict_data = request.dict()
        dict_data["audio_base64"] = base64.b64decode(dict_data["audio_base64"])
        result = self._stub.AudioValidation.with_call(
            gen.AudioValidationRequest(**dict_data)
        )

        return model.AudioValidationResponse(**grpc_to_dict(result))

    def face_match(
        self, request: model.FaceMatchValidationRequest
    ) -> model.FaceMatchValidationResponse:
        dict_data = request.dict()
        dict_data["image_base64_one"] = base64.b64decode(dict_data["image_base64_one"])
        dict_data["image_base64_two"] = base64.b64decode(dict_data["image_base64_two"])
        result = self._stub.FaceMatchValidation.with_call(
            gen.FaceMatchValidationRequest(**dict_data)
        )
        return model.FaceMatchValidationResponse(**grpc_to_dict(result))

    def ocr(self, request: model.OCRProcessingRequest) -> model.OCRProcessingResponse:
        dict_data = request.dict()
        dict_data["image_base64"] = base64.b64decode(dict_data["image_base64"])
        result = self._stub.OCRProcessing.with_call(
            gen.OCRProcessingRequest(**dict_data)
        )
        return model.OCRProcessingResponse(**grpc_to_dict(result))

    def personal_data(
        self, request: model.PersonalDataQueryRequest
    ) -> model.PersonalDataQueryResponse:
        result = self._stub.PersonalDataQuery.with_call(
            gen.PersonalDataQueryRequest(**request.dict())
        )
        return model.PersonalDataQueryResponse(**grpc_to_dict(result))

    def facial_biometrics(
        self, request: model.FacialBiometricsValidationRequest
    ) -> model.FacialBiometricsValidationResponse:
        dict_data = request.dict()
        dict_data["image_base64"] = base64.b64decode(dict_data["image_base64"])
        result = self._stub.FacialBiometricsValidation.with_call(
            gen.FacialBiometricsValidationRequest(**dict_data)
        )
        return model.FacialBiometricsValidationResponse(**grpc_to_dict(result))
