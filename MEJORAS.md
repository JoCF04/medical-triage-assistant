# Mejoras respecto a la primera versión

La primera versión funcionaba, pero al probarla con frases normales encontré varios problemas:

1. **No usaba el JSON.** El script tenía escrita a mano una copia más chica de los datos (7 síntomas), así que 20 de los 27 síntomas del JSON nunca se reconocían.
2. **Solo reconocía la palabra exacta.** *headache* sí, pero *headaches*, *coughing* o *tired* no.
3. **No entendía negaciones.** "I have a headache but no fever" devolvía *headache* y *fever*.
4. **No distinguía lo urgente.** "I have chest pain" se trataba igual que un resfrío.
5. **Listaba todas las condiciones posibles**, incluidas algunas graves, aunque solo coincidiera un síntoma. Ahora muestra las 3 más probables.

Para medir el cambio escribí 40 frases de prueba (`casos_prueba.json`) con los síntomas que debería encontrar en cada una, incluyendo negaciones, emergencias y algunas frases difíciles a propósito:

| | Versión anterior | Versión actual |
|---|---|---|
| Frases resueltas perfecto | 7 de 40 | 38 de 40 |
| Síntomas detectados | 12 de 39 (31 %) | 37 de 39 (95 %) |
| Síntomas detectados que eran correctos | 12 de 17 (71 %) | 37 de 38 (97 %) |
| Emergencias detectadas | 0 de 6 | 6 de 6 |

Las dos frases que todavía falla son expresiones coloquiales: *"I've had the runs"* (diarrea) y *"I feel like throwing up"*, que confunde náuseas con vómitos. Resolver ese tipo de casos requeriría un modelo que entienda significado y no solo palabras, por ejemplo con embeddings.

Un detalle importante: las frases de prueba y las variantes de cada síntoma las escribí yo, así que estos números muestran que la lógica funciona. No son una medida de cómo le iría con pacientes reales.

Para repetir la medición: `python evaluar.py`.
