from typing import List, Dict, Any
from enum import IntEnum

from pydantic import BaseModel, Field


class AudioValidationRequest(BaseModel):
    audio_base64: str = Field(default_factory=str)
    expected_text: str = Field(default_factory=str)
    expected_text_with_variables: str = Field(default_factory=str)

    class WordExactValidationRequest(BaseModel):
        word: str = Field(default_factory=str)

        class WordTypeEnumProto(IntEnum):
            MONETARY = 0
            TAX = 1
            DATE = 2
            NAME = 3
            INT = 4
            DONT_USE_IT = 5

        type: WordTypeEnumProto = Field(default_factory=int)
        value: str = Field(default_factory=str)

    words_to_exact_validation: List[WordExactValidationRequest] = Field(default_factory=list)
    process_id: str = Field(default_factory=str)


class AudioValidationResponse(BaseModel):
    extracted_text: str = Field(default_factory=str)
    extracted_text_treated: str = Field(default_factory=str)
    expected_text_treated: str = Field(default_factory=str)
    similarity: int = Field(default_factory=int)
    is_valid_audio: bool = Field(default_factory=bool)

    class WordExactValidationResponse(BaseModel):
        word: str = Field(default_factory=str)
        extracted_value: str = Field(default_factory=str)
        is_valid: bool = Field(default_factory=bool)

    words_to_exact_validation: List[WordExactValidationResponse] = Field(default_factory=list)


class CreateProcessValidationRequest(BaseModel):
    origin: str = Field(default_factory=str)


class CreateProcessValidationResponse(BaseModel):
    id: str = Field(default_factory=str)


class FaceMatchValidationRequest(BaseModel):
    image_base64_one: str = Field(default_factory=str)
    image_base64_two: str = Field(default_factory=str)
    process_id: str = Field(default_factory=str)


class FaceMatchValidationResponse(BaseModel):
    is_valid_face_match: bool = Field(default_factory=bool)


class FacialBiometricsValidationRequest(BaseModel):
    cpf: str = Field(default_factory=str)
    name: str = Field(default_factory=str)
    only_selfie: bool = Field(default_factory=bool)
    image_base64: str = Field(default_factory=str)
    process_id: str = Field(default_factory=str)


class FacialBiometricsValidationResponse(BaseModel):
    facial_process_id: str = Field(default_factory=str)
    score: int = Field(default_factory=int)

    class FacialBiometricsStatusEnumProto(IntEnum):
        PROCESSING = 0
        OK = 1
        ERROR = 2

    status: FacialBiometricsStatusEnumProto = Field(default_factory=int)
    creation_date: int = Field(default_factory=int)


class OCRCNHDataProto(BaseModel):

    class OCRSideEnumProto(IntEnum):
        SIDE_A = 0
        SIDE_B = 1
        SIDE_C = 2

    side: OCRSideEnumProto = Field(default_factory=int)
    birth_date: int = Field(default_factory=int)

    class OCRCNHCategoryEnumProto(IntEnum):
        CATEGORY_A = 0
        CATEGORY_B = 1
        CATEGORY_C = 2
        CATEGORY_D = 3
        CATEGORY_E = 4
        CATEGORY_AB = 5

    category: OCRCNHCategoryEnumProto = Field(default_factory=int)
    cnh_number: str = Field(default_factory=str)
    cpf: str = Field(default_factory=str)
    father_name: str = Field(default_factory=str)
    first_qualification_date: int = Field(default_factory=int)
    identification_number: str = Field(default_factory=str)
    identification_uf: str = Field(default_factory=str)
    mother_name: str = Field(default_factory=str)
    name: str = Field(default_factory=str)
    org_emission: str = Field(default_factory=str)
    doc_emission_place: str = Field(default_factory=str)
    valid_date: int = Field(default_factory=int)
    expedition_date: int = Field(default_factory=int)
    place_of_emission: str = Field(default_factory=str)
    renach: str = Field(default_factory=str)
    observations: str = Field(default_factory=str)
    paid_activity: bool = Field(default_factory=bool)


class OCRCTPSDataProto(BaseModel):

    class OCRSideEnumProto(IntEnum):
        SIDE_A = 0
        SIDE_B = 1
        SIDE_C = 2

    side: OCRSideEnumProto = Field(default_factory=int)
    cpf: str = Field(default_factory=str)
    birth_date: int = Field(default_factory=int)
    expedition_date: int = Field(default_factory=int)
    father_name: str = Field(default_factory=str)
    uf: str = Field(default_factory=str)
    pis_pasesp: str = Field(default_factory=str)
    ctps_serie: str = Field(default_factory=str)
    ctps_number: str = Field(default_factory=str)
    mother_name: str = Field(default_factory=str)
    name: str = Field(default_factory=str)
    marital_status: str = Field(default_factory=str)
    identification_number: str = Field(default_factory=str)


class OCRCartaoCPFDataProto(BaseModel):

    class OCRSideEnumProto(IntEnum):
        SIDE_A = 0
        SIDE_B = 1
        SIDE_C = 2

    side: OCRSideEnumProto = Field(default_factory=int)
    birth_date: int = Field(default_factory=int)
    cpf: str = Field(default_factory=str)
    name: str = Field(default_factory=str)


class OCRProcessingRequest(BaseModel):
    image_base64: str = Field(default_factory=str)
    process_id: str = Field(default_factory=str)


class OCRProcessingResponse(BaseModel):

    class OCRDocTypeEnumProto(IntEnum):
        CNH = 0
        RG = 1
        NEWRG = 2
        CTPS = 3
        UNDEFINED = 4
        RNE = 5
        CARTAO_CPF = 6

    doc_type: OCRDocTypeEnumProto = Field(default_factory=int)

    class OCRCNHDataProto(BaseModel):

        class OCRSideEnumProto(IntEnum):
            SIDE_A = 0
            SIDE_B = 1
            SIDE_C = 2

        side: OCRSideEnumProto = Field(default_factory=int)
        birth_date: int = Field(default_factory=int)

        class OCRCNHCategoryEnumProto(IntEnum):
            CATEGORY_A = 0
            CATEGORY_B = 1
            CATEGORY_C = 2
            CATEGORY_D = 3
            CATEGORY_E = 4
            CATEGORY_AB = 5

        category: OCRCNHCategoryEnumProto = Field(default_factory=int)
        cnh_number: str = Field(default_factory=str)
        cpf: str = Field(default_factory=str)
        father_name: str = Field(default_factory=str)
        first_qualification_date: int = Field(default_factory=int)
        identification_number: str = Field(default_factory=str)
        identification_uf: str = Field(default_factory=str)
        mother_name: str = Field(default_factory=str)
        name: str = Field(default_factory=str)
        org_emission: str = Field(default_factory=str)
        doc_emission_place: str = Field(default_factory=str)
        valid_date: int = Field(default_factory=int)
        expedition_date: int = Field(default_factory=int)
        place_of_emission: str = Field(default_factory=str)
        renach: str = Field(default_factory=str)
        observations: str = Field(default_factory=str)
        paid_activity: bool = Field(default_factory=bool)

    ocr_cnh_data: OCRCNHDataProto = Field(default_factory=OCRCNHDataProto)

    class OCRRGDataProto(BaseModel):
        doc_emission_place: str = Field(default_factory=str)
        place_of_birth: str = Field(default_factory=str)
        identification_uf: str = Field(default_factory=str)
        birth_date: int = Field(default_factory=int)
        cpf: str = Field(default_factory=str)
        expedition_date: int = Field(default_factory=int)
        father_name: str = Field(default_factory=str)
        identification_number: str = Field(default_factory=str)
        mother_name: str = Field(default_factory=str)
        name: str = Field(default_factory=str)

        class OCRSideEnumProto(IntEnum):
            SIDE_A = 0
            SIDE_B = 1
            SIDE_C = 2

        side: OCRSideEnumProto = Field(default_factory=int)
        valid_date: int = Field(default_factory=int)

    ocr_rg_data: OCRRGDataProto = Field(default_factory=OCRRGDataProto)

    class OCRCTPSDataProto(BaseModel):

        class OCRSideEnumProto(IntEnum):
            SIDE_A = 0
            SIDE_B = 1
            SIDE_C = 2

        side: OCRSideEnumProto = Field(default_factory=int)
        cpf: str = Field(default_factory=str)
        birth_date: int = Field(default_factory=int)
        expedition_date: int = Field(default_factory=int)
        father_name: str = Field(default_factory=str)
        uf: str = Field(default_factory=str)
        pis_pasesp: str = Field(default_factory=str)
        ctps_serie: str = Field(default_factory=str)
        ctps_number: str = Field(default_factory=str)
        mother_name: str = Field(default_factory=str)
        name: str = Field(default_factory=str)
        marital_status: str = Field(default_factory=str)
        identification_number: str = Field(default_factory=str)

    ocr_ctps_data: OCRCTPSDataProto = Field(default_factory=OCRCTPSDataProto)

    class OCRRNEDataProto(BaseModel):

        class OCRSideEnumProto(IntEnum):
            SIDE_A = 0
            SIDE_B = 1
            SIDE_C = 2

        side: OCRSideEnumProto = Field(default_factory=int)
        place_of_birth: str = Field(default_factory=str)
        rne: str = Field(default_factory=str)
        birth_date: int = Field(default_factory=int)
        expedition_date: int = Field(default_factory=int)
        father_name: str = Field(default_factory=str)
        classification: str = Field(default_factory=str)
        gender: str = Field(default_factory=str)
        nacionality: str = Field(default_factory=str)
        naturality: str = Field(default_factory=str)
        org_emission: str = Field(default_factory=str)
        entry_date: int = Field(default_factory=int)
        mother_name: str = Field(default_factory=str)
        name: str = Field(default_factory=str)
        valid_date: int = Field(default_factory=int)

    ocr_rne_data: OCRRNEDataProto = Field(default_factory=OCRRNEDataProto)

    class OCRCartaoCPFDataProto(BaseModel):

        class OCRSideEnumProto(IntEnum):
            SIDE_A = 0
            SIDE_B = 1
            SIDE_C = 2

        side: OCRSideEnumProto = Field(default_factory=int)
        birth_date: int = Field(default_factory=int)
        cpf: str = Field(default_factory=str)
        name: str = Field(default_factory=str)

    ocr_cartao_cpf_data: OCRCartaoCPFDataProto = Field(default_factory=OCRCartaoCPFDataProto)
    error_message: str = Field(default_factory=str)
    processing_date: int = Field(default_factory=int)


class OCRRGDataProto(BaseModel):
    doc_emission_place: str = Field(default_factory=str)
    place_of_birth: str = Field(default_factory=str)
    identification_uf: str = Field(default_factory=str)
    birth_date: int = Field(default_factory=int)
    cpf: str = Field(default_factory=str)
    expedition_date: int = Field(default_factory=int)
    father_name: str = Field(default_factory=str)
    identification_number: str = Field(default_factory=str)
    mother_name: str = Field(default_factory=str)
    name: str = Field(default_factory=str)

    class OCRSideEnumProto(IntEnum):
        SIDE_A = 0
        SIDE_B = 1
        SIDE_C = 2

    side: OCRSideEnumProto = Field(default_factory=int)
    valid_date: int = Field(default_factory=int)


class OCRRNEDataProto(BaseModel):

    class OCRSideEnumProto(IntEnum):
        SIDE_A = 0
        SIDE_B = 1
        SIDE_C = 2

    side: OCRSideEnumProto = Field(default_factory=int)
    place_of_birth: str = Field(default_factory=str)
    rne: str = Field(default_factory=str)
    birth_date: int = Field(default_factory=int)
    expedition_date: int = Field(default_factory=int)
    father_name: str = Field(default_factory=str)
    classification: str = Field(default_factory=str)
    gender: str = Field(default_factory=str)
    nacionality: str = Field(default_factory=str)
    naturality: str = Field(default_factory=str)
    org_emission: str = Field(default_factory=str)
    entry_date: int = Field(default_factory=int)
    mother_name: str = Field(default_factory=str)
    name: str = Field(default_factory=str)
    valid_date: int = Field(default_factory=int)


class PersonalDataQueryRequest(BaseModel):
    cpf: str = Field(default_factory=str)
    process_id: str = Field(default_factory=str)


class PersonalDataQueryResponse(BaseModel):
    data_origin: str = Field(default_factory=str)
    cpf: str = Field(default_factory=str)
    rg: str = Field(default_factory=str)
    cnh: str = Field(default_factory=str)
    voter_id: str = Field(default_factory=str)
    name: str = Field(default_factory=str)

    class PersonalDataGenderEnumProto(IntEnum):
        GENDER_M = 0
        GENDER_F = 1
        GENDER_U = 2

    gender: PersonalDataGenderEnumProto = Field(default_factory=int)
    mother_name: str = Field(default_factory=str)
    father_name: str = Field(default_factory=str)

    class PersonalDataMaritalStatusEnumProto(IntEnum):
        SINGLE = 0
        MARRIED = 1

    marital_status: PersonalDataMaritalStatusEnumProto = Field(default_factory=int)
    birth_date: int = Field(default_factory=int)
    nacionality: str = Field(default_factory=str)


class WordExactValidationRequest(BaseModel):
    word: str = Field(default_factory=str)

    class WordTypeEnumProto(IntEnum):
        MONETARY = 0
        TAX = 1
        DATE = 2
        NAME = 3
        INT = 4
        DONT_USE_IT = 5

    type: WordTypeEnumProto = Field(default_factory=int)
    value: str = Field(default_factory=str)


class WordExactValidationResponse(BaseModel):
    word: str = Field(default_factory=str)
    extracted_value: str = Field(default_factory=str)
    is_valid: bool = Field(default_factory=bool)