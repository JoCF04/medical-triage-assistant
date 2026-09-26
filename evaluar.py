"""Mide qué tan bien el chatbot reconoce síntomas en las frases de casos_prueba.json."""
import json

from chatbot_medico import extract_symptoms

with open("casos_prueba.json", encoding="utf-8") as f:
    casos = json.load(f)

aciertos = encontrados = esperados = correctos = 0
urgentes = urgentes_detectados = falsas_alarmas = 0
fallos = []

for caso in casos:
    sintomas, alarmas = extract_symptoms(caso["texto"])
    esperado = set(caso["sintomas"])
    obtenido = set(sintomas)

    correctos += len(esperado & obtenido)
    encontrados += len(obtenido)
    esperados += len(esperado)

    urgente = bool(alarmas)
    if caso["urgente"]:
        urgentes += 1
        urgentes_detectados += urgente
    else:
        falsas_alarmas += urgente

    if obtenido == esperado and urgente == caso["urgente"]:
        aciertos += 1
    else:
        fallos.append(f'  "{caso["texto"]}" -> esperado {sorted(esperado)}{" + URGENTE" if caso["urgente"] else ""}, '
                      f'obtuvo {sorted(obtenido)}{" + URGENTE" if urgente else ""}')

print(f"Frases evaluadas:            {len(casos)}")
print(f"Frases 100% correctas:       {aciertos} ({aciertos / len(casos):.0%})")
print(f"Síntomas detectados (recall): {correctos}/{esperados} ({correctos / esperados:.0%})")
print(f"Síntomas correctos (precision): {correctos}/{encontrados} ({correctos / max(encontrados, 1):.0%})")
print(f"Urgencias detectadas:        {urgentes_detectados}/{urgentes}")
print(f"Falsas alarmas de urgencia:  {falsas_alarmas}")
if fallos:
    print("\nFrases con error:")
    print("\n".join(fallos))
