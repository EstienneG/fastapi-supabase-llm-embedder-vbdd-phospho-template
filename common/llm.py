import phospho
from common.api_global_variables import api_global_variables


def generate_patient_insight(patient_input: str) -> str:
    input_str = (
        "Tu es un agent qui va extraire les informations clés de la journée d'un patient d'un psychiatre."
        + patient_input
    )
    patient_key_insights = (
        api_global_variables.llm.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_str,
                }
            ],
            model="llama3-8b-8192",
        )
        .choices[0]
        .message.content
    )

    phospho.log(input=input_str, output=patient_key_insights)
    print(patient_key_insights)

    return patient_key_insights


def call_groq(question: str) -> str:
    answer = (
        api_global_variables.llm.chat.completions.create(
            messages=[{"role": "user", "content": question}],
            model="llama3-8b-8192",
        )
        .choices[0]
        .message.content
    )
    phospho.log(input=question, output=answer)

    return answer
