import spacy
import json

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

medical_data = {
    "symptoms": {
        "headache": ["common cold", "flu", "migraine", "tension headache", "sinusitis"],
        "fever": ["common cold", "flu", "infection", "strep throat"],
        "cough": ["common cold", "flu", "bronchitis", "pneumonia", "allergies"],
        "fatigue": ["common cold", "flu", "stress", "lack of sleep", "anemia"],
        "dizzy": ["dehydration", "inner ear infection", "low blood sugar"],
        "rash": ["allergies", "chickenpox", "eczema"],
        "itchy": ["allergies", "eczema", "dry skin"]

    },
    "recommendations": {
        "common cold": "Rest, stay hydrated, and consider over-the-counter medications for symptom relief.",
        "flu": "Rest, stay hydrated, and consider over-the-counter medications for symptom relief.",
        "migraine": "Rest in a quiet, dark room. Apply a cold compress to your forehead.",
        "allergies": "Identify and avoid allergens. Consider over-the-counter antihistamines.",
        "dehydration": "Drink plenty of fluids and electrolytes."
    }
}


def extract_symptoms(user_input):
    """Extrae síntomas únicos del input del usuario usando spaCy."""
    doc = nlp(user_input)
    extracted_symptoms = []
    for token in doc:
        word = token.text.lower()
        if word in medical_data["symptoms"] and word not in extracted_symptoms:
            extracted_symptoms.append(word)
    return extracted_symptoms

def analyze_symptoms(extracted_symptoms):
    """Calcula la frecuencia de cada condición según los síntomas extraídos."""
    possible_conditions = {}
    for symptom in extracted_symptoms:
        if symptom in medical_data["symptoms"]:
            for condition in medical_data["symptoms"][symptom]:
                possible_conditions[condition] = possible_conditions.get(condition, 0) + 1
    return possible_conditions

def generate_response(extracted_symptoms, possible_conditions):
    """Genera la respuesta formateada con recomendaciones y disclaimer."""
    response = ""
    if extracted_symptoms:
        response += f"I understand you have {', '.join(extracted_symptoms)}.\n"
        response += "Based on your symptoms, the most likely possibilities are:"
        
        if possible_conditions:
            # Ordenar por probabilidad (conteo de síntomas)
            sorted_conditions = sorted(
                possible_conditions.items(), key=lambda item: item[1], reverse=True
            )
            for condition, count in sorted_conditions:
                response += f"\n- {condition} ({count} matching symptom(s))"
                if condition in medical_data["recommendations"]:
                    rec = medical_data["recommendations"][condition]
                    response += f"\n  * {rec}"
        else:
            response += "\nI'm sorry, I don't recognize those symptoms."
    else:
        response = "I'm sorry, I didn't recognize any symptoms in your description."

    response += "\n\nRemember, I am just a chatbot and cannot provide definitive medical advice. Please consult a doctor."
    return response


def start_chatbot():
    print("--- Medical Diagnosis Assistant ---")

    user_input = input("Please enter your primary concern: ")
    extracted_symptoms = extract_symptoms(user_input)
    possible_conditions = analyze_symptoms(extracted_symptoms)
    response = generate_response(extracted_symptoms, possible_conditions)
    print("\nChatbot:", response)

    while True:
        print("\n" + "-"*30)
        additional = input("Please enter an additional symptom, or 'no' if you have no more: ")
        
        if additional.lower() in ("no", "nope", "none"):
            break
        
        new_symptoms = extract_symptoms(additional)
        if new_symptoms:
            extracted_symptoms.extend(new_symptoms)
            possible_conditions = analyze_symptoms(extracted_symptoms)
            response = generate_response(extracted_symptoms, possible_conditions)
            print("\nChatbot (Updated):", response)
        else:
            print("Chatbot: I didn't recognize that symptom. Please try again.")

    print("\nFinal Result:", response)
    print("Stay safe! Goodbye.")

if __name__ == "__main__":
    start_chatbot()
    
#pip install spacy
#python -m spacy download en_core_web_sm
#python chatbot_medico.py