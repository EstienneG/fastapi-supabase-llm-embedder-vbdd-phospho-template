from common import llm


def generate_patient_insight(rfp_title: str, rfp: bytes) -> str:
    return llm.generate_patient_insight(rfp_title, rfp)
