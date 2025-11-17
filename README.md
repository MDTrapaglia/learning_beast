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

## Endpoints principales

La API expone los siguientes endpoints principales:

| Endpoint | Método | Descripción |
| --- | --- | --- |
| `/session/start` | POST | Crea una sesión segura y entrega la primera pregunta conversacional. |
| `/session/{session_id}/question` | GET | Obtiene la siguiente pregunta del onboarding conversacional. |
| `/session/{session_id}/question/{question_id}` | POST | Envía una respuesta saneada y avanza en el flujo de descubrimiento. |
| `/node/{node_id}` | GET | Recupera el contenido de un nodo educativo (requiere `X-Session-Id`). |
| `/node/{node_id}/answer` | POST | Recibe la respuesta del usuario y calcula la siguiente actividad. |
| `/profile/{session_id}` | GET | Devuelve el perfil dinámico y los puntos acumulados. |

### Ejemplo de inicio de sesión

```bash
curl -X POST http://localhost:8000/session/start \
  -H "Content-Type: application/json" \
  -d '{"display_name": "Sol"}'
```

**Respuesta JSON:**

```json
{
  "session_id": "b76f...",
  "question": {
    "id": "q1",
    "prompt": "¿Qué temas te inspiran últimamente?",
    "category": "curiosity",
    "follow_up": "¿Cómo lo aplicarías?",
    "weights": {"creatividad": 0.4, "tecnologia": 0.6}
  }
}
```

**Nota:** En caso de no enviar `display_name`, el backend crea la sesión igualmente y la respuesta siempre incluye la primera pregunta del onboarding.

### Flujo de preguntas posteriores

Una vez creada la sesión puedes continuar con el onboarding usando los siguientes endpoints que ahora devuelven respuestas tipadas:

```bash
curl http://localhost:8000/session/<SESSION_ID>/question
```

**Respuesta JSON cuando aún quedan preguntas:**

```json
{
  "question": {
    "id": "q2",
    "prompt": "¿Qué retos creativos te divierten?",
    "category": "creatividad",
    "follow_up": "¿Y cuál intentaste recientemente?",
    "weights": {"creatividad": 0.6, "tecnologia": 0.4}
  },
  "message": null
}
```

Cuando no quedan preguntas el backend responde con el campo `message` poblado y `question` en `null` para que el cliente pueda detectar el fin del flujo sin usar condicionales frágiles.

Al enviar una respuesta, el endpoint `/session/{session_id}/question/{question_id}` devuelve siempre el mismo esquema:

```json
{
  "answered": { "id": "q2", "prompt": "…" },
  "next_question": { "id": "q3", "prompt": "…" }
}
```

Si ya no existen más preguntas, `next_question` será `null`.

## Seguridad aplicada

- **Sesiones cifradas**: se generan tokens con `secrets` y se valida su vigencia en cada request.
- **Saneamiento de textos**: todas las respuestas libres y el `display_name` inicial pasan por un filtro estricto que elimina caracteres peligrosos y hace *HTML escaping* para evitar inyecciones.
- **Cabeceras obligatorias**: los endpoints sensibles de nodos requieren la cabecera `X-Session-Id` para evitar abusos desde la barra de direcciones.
- **CORS restringido**: solo orígenes conocidos pueden interactuar con el backend durante el MVP.

## Datos iniciales

Los archivos JSON en `data/` definen las preguntas conversacionales y los nodos educativos (10 micro-lecciones conectadas) que nutren al motor adaptativo.
