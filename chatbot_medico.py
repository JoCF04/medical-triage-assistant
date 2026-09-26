import json
import sys
from pathlib import Path

import spacy
from spacy.matcher import PhraseMatcher
from spacy.util import filter_spans

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# La base de conocimiento vive en el JSON (antes el script usaba una copia más chica escrita a mano)
with open(Path(__file__).parent / "medical_data.json", encoding="utf-8") as f:
    medical_data = json.load(f)

TOP_CONDICIONES = 3
NEGACIONES = {"no", "not", "n't", "never", "without", "none", "nor"}
CORTES = {"but", "though", "although", "however", "only", "just", ",", ".", ";", "!", "?"}

# Dos buscadores: uno por palabra exacta y otro por lema ("headaches" -> "headache", "coughing" -> "cough")
por_texto = PhraseMatcher(nlp.vocab, attr="LOWER")
por_lema = PhraseMatcher(nlp.vocab, attr="LEMMA")

for sintoma in medical_data["symptoms"]:
    frases = [sintoma] + medical_data["aliases"].get(sintoma, [])
    patrones = list(nlp.pipe(frases))
    por_texto.add(sintoma, patrones)
    por_lema.add(sintoma, patrones)

por_texto.add("RED_FLAG", list(nlp.pipe(medical_data["red_flags"])))


def esta_negado(doc, inicio):
    """Mira hacia atrás en la misma frase: 'I don't have a fever' o 'no cough'."""
    for i in range(inicio - 1, max(inicio - 7, -1), -1):
        palabra = doc[i].lower_
        if palabra in CORTES:
            return False
        if palabra in NEGACIONES:
            return True
    return False


def extract_symptoms(user_input):
    """Devuelve (síntomas encontrados, señales de alarma), sin repetir y sin los que están negados."""
    doc = nlp(user_input)
    spans = []
    for matcher in (por_texto, por_lema):
        for match_id, inicio, fin in matcher(doc):
            span = doc[inicio:fin]
            span.label_ = nlp.vocab.strings[match_id]
            spans.append(span)

    sintomas, alarmas = [], []
    # filter_spans se queda con la coincidencia más larga ("chest pain" gana sobre "pain")
    for span in sorted(filter_spans(spans), key=lambda s: s.start):
        if esta_negado(doc, span.start):
            continue
        if span.label_ == "RED_FLAG":
            if span.text.lower() not in alarmas:
                alarmas.append(span.text.lower())
        elif span.label_ not in sintomas:
            sintomas.append(span.label_)
    return sintomas, alarmas


def analyze_symptoms(extracted_symptoms):
    """Cuenta cuántos síntomas apuntan a cada condición. En empate gana la más común (va primero en el JSON)."""
    conteo, orden = {}, {}
    for sintoma in extracted_symptoms:
        for posicion, condicion in enumerate(medical_data["symptoms"][sintoma]):
            conteo[condicion] = conteo.get(condicion, 0) + 1
            orden[condicion] = min(orden.get(condicion, posicion), posicion)
    ranking = sorted(conteo.items(), key=lambda c: (-c[1], orden[c[0]]))
    return ranking[:TOP_CONDICIONES]


def generate_response(extracted_symptoms, alarmas, possible_conditions):
    if alarmas:
        return medical_data["urgent_message"].format(flags=", ".join(alarmas))

    if not extracted_symptoms:
        return "I'm sorry, I didn't recognize any symptoms in your description. Try describing how you feel in other words."

    response = f"I understand you have: {', '.join(extracted_symptoms)}.\n"
    response += "Some common causes for these symptoms are:"
    for condicion, count in possible_conditions:
        rec = medical_data["recommendations"].get(condicion, medical_data["default_recommendation"])
        response += f"\n- {condicion} ({count} matching symptom{'s' if count > 1 else ''})\n  {rec}"

    response += "\n\nRemember, I am just a chatbot and cannot give a diagnosis. Please consult a doctor."
    return response


def responder(texto):
    sintomas, alarmas = extract_symptoms(texto)
    return generate_response(sintomas, alarmas, analyze_symptoms(sintomas))


def start_chatbot():
    print("--- Medical Symptom Checker ---")
    print("(This is a practice project, not medical advice.)\n")

    user_input = input("Please describe how you feel: ")
    extracted_symptoms, alarmas = extract_symptoms(user_input)
    response = generate_response(extracted_symptoms, alarmas, analyze_symptoms(extracted_symptoms))
    print("\nChatbot:", response)

    while not alarmas:
        print("\n" + "-" * 30)
        additional = input("Any other symptom? (type 'no' to finish): ")
        if additional.strip().lower() in ("no", "nope", "none", ""):
            break

        new_symptoms, alarmas = extract_symptoms(additional)
        if new_symptoms or alarmas:
            extracted_symptoms += [s for s in new_symptoms if s not in extracted_symptoms]
            response = generate_response(extracted_symptoms, alarmas, analyze_symptoms(extracted_symptoms))
            print("\nChatbot (updated):", response)
        else:
            print("Chatbot: I didn't recognize that symptom. Please try again.")

    print("\nStay safe! Goodbye.")


if __name__ == "__main__":
    # python chatbot_medico.py "I have a headache and I feel dizzy"  -> responde una vez y termina
    if len(sys.argv) > 1:
        print(responder(" ".join(sys.argv[1:])))
    else:
        start_chatbot()
