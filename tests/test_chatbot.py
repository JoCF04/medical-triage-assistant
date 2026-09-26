import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from chatbot_medico import analyze_symptoms, extract_symptoms, responder


def test_reconoce_variantes_de_palabras():
    assert extract_symptoms("I've had headaches and I keep coughing")[0] == ["headache", "cough"]


def test_ignora_sintomas_negados():
    assert extract_symptoms("I have a headache but no fever")[0] == ["headache"]
    assert extract_symptoms("I don't have a fever or a cough")[0] == []


def test_usa_todo_el_json():
    # "bloating" solo existía en el JSON, no en el diccionario que tenía el script antes
    assert extract_symptoms("I feel bloated")[0] == ["bloating"]


def test_senales_de_alarma():
    sintomas, alarmas = extract_symptoms("I have a cough and chest pain")
    assert alarmas == ["chest pain"]
    assert "emergency" in responder("I have chest pain")


def test_ranking_prioriza_coincidencias():
    top = analyze_symptoms(["fever", "cough", "fatigue"])
    assert top[0] == ("common cold", 3)
    assert len(top) == 3
