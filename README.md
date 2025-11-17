# Learning Beast — Backend MVP

Este repositorio contiene un primer MVP del backend para la plataforma de aprendizaje adaptativo descrita en el PRD. Se diseñó con FastAPI y pone especial atención en la seguridad de las entradas libres (respuestas de usuario y parámetros críticos), manteniendo el código documentado y entendible.

## Requisitos

- Python 3.11+
- Pip

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecución local

```bash
uvicorn app.main:app --reload
```

La API expone los siguientes endpoints principales:

| Endpoint | Método | Descripción |
| --- | --- | --- |
| `/session/start` | POST | Crea una sesión segura y entrega la primera pregunta conversacional. |
| `/session/{session_id}/question` | GET | Obtiene la siguiente pregunta del onboarding conversacional. |
| `/session/{session_id}/question/{question_id}` | POST | Envía una respuesta saneada y avanza en el flujo de descubrimiento. |
| `/node/{node_id}` | GET | Recupera el contenido de un nodo educativo (requiere `X-Session-Id`). |
| `/node/{node_id}/answer` | POST | Recibe la respuesta del usuario y calcula la siguiente actividad. |
| `/profile/{session_id}` | GET | Devuelve el perfil dinámico y los puntos acumulados. |

## Seguridad aplicada

- **Sesiones cifradas**: se generan tokens con `secrets` y se valida su vigencia en cada request.
- **Saneamiento de textos**: todas las respuestas libres pasan por un filtro estricto que elimina caracteres peligrosos y hace *HTML escaping* para evitar inyecciones.
- **Cabeceras obligatorias**: los endpoints sensibles de nodos requieren la cabecera `X-Session-Id` para evitar abusos desde la barra de direcciones.
- **CORS restringido**: solo orígenes conocidos pueden interactuar con el backend durante el MVP.

## Datos iniciales

Los archivos JSON en `data/` definen las preguntas conversacionales y los nodos educativos (10 micro-lecciones conectadas) que nutren al motor adaptativo.
