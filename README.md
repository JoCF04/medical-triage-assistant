# Asistente Virtual para Triaje Médico Preliminar (NLP)

Este proyecto desarrolla un sistema de procesamiento de lenguaje natural (NLP) diseñado para realizar un triaje médico automatizado mediante una interfaz de conversación natural. El sistema identifica síntomas específicos en el discurso del usuario y proporciona una jerarquía de posibles condiciones médicas basadas en un análisis de coincidencias probabilísticas.

---

## Metodología y Funcionamiento

* **Procesamiento de Lenguaje Natural (NLP)**: Implementación de la librería **spaCy** para la tokenización y el filtrado de entidades lingüísticas, permitiendo extraer síntomas clave y descartar ruido léxico.
* **Gestión de Conocimiento Estructurado**: Utiliza una base de datos interna orientada a objetos (diccionarios/JSON) para mapear la relación entre sintomatología y diagnósticos preliminares.
* **Algoritmo de Clasificación**: El sistema aplica una lógica de conteo y jerarquización de frecuencias para determinar las condiciones más probables en tiempo real.
* **Control de Flujo Dinámico**: El asistente gestiona una interacción iterativa donde solicita información adicional para refinar el resultado, concluyendo con recomendaciones preventivas y descargos de responsabilidad éticos.

---

## Tecnologías Utilizadas

* **Python**: Lenguaje principal para la lógica de control, manejo de excepciones y flujos de decisión.
* **spaCy (en_core_web_sm)**: Framework avanzado de NLP para el análisis de texto y reconocimiento de entidades.
* **Estructuras de Datos**: Uso intensivo de mapeos y listas para la manipulación eficiente de la información médica.

---

## Estructura del Repositorio

* **chatbot_medico.py**: Script principal que integra el motor de procesamiento y la interfaz de usuario por consola.
* **medical_data.json**: (Estructura interna) Base de conocimientos que define la lógica de diagnóstico y recomendaciones.
