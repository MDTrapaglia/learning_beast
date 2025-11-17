# Product Requirements Document (PRD)

# Plataforma de Aprendizaje Adaptativo

---

## 1. **Visión del Producto**

La plataforma busca transformar el aprendizaje en una experiencia fluida, personalizada y casi "invisible" para el usuario. Mediante preguntas iniciales, actividades breves y un motor adaptativo inteligente, el sistema descubre los intereses, fortalezas y estilos cognitivos del usuario, guiándolo de forma progresiva hacia contenidos educativos que se sienten como un viaje entretenido, no como un curso tradicional.

La meta: **crear un tutor inteligente gamificado que enseña sin que se sienta como estudiar**.

---

## 2. **Objetivos del Proyecto**

* Identificar intereses del usuario mediante interacciones conversacionales.
* Ofrecer rutas educativas personalizadas basadas en categorías cognitivas.
* Mantener alta retención mediante micro-actividades breves y dinámicas.
* Implementar un sistema de recomendación que evoluciona con cada interacción.
* Construir una arquitectura modular, escalable y lista para incorporar IA.

---

## 3. **Alcance del Proyecto (Scope)**

### 3.1. **Incluido en el alcance actual**

* Diseño de flujo de preguntas iniciales.
* Sistema de ponderación para categorizar intereses del usuario.
* Motor de recomendación basado en vector de usuario (S_u).
* Nodos educativos en formato compacto (micro-lecciones de 3–8 minutos).
* Backend inicial con API (FastAPI) para manejar sesiones, nodos y respuestas.
* Persistencia mínima en memoria o base de datos simple.
* Selección de nodos secuenciales basada en decisiones simples.

### 3.2. **Fuera del alcance actual (pero planificado)**

* Frontend completo con diseño avanzado.
* Análisis colaborativo entre usuarios.
* Notificaciones Push o email.
* Integración con modelos de IA para generación dinámica de contenido.
* Marketplace de creadores de contenido.

---

## 4. **Usuarios objetivo**

* Personas curiosas que desean aprender sin la rigidez de un curso tradicional.
* Profesionales que buscan micro-aprendizajes rápidos.
* Estudiantes autodidactas con intereses amplios.
* Equipos que podrían personalizar aprendizaje interno (etapa futura).

---

## 5. **Requisitos funcionales principales**

### 5.1. **Motor de preguntas iniciales**

* Mostrar 10–15 preguntas.
* Procesar cada respuesta mediante vectores de peso.
* Actualizar S_u (vector de preferencias).

### 5.2. **Selector de nodos educativos**

* Asignar el nodo inicial.
* Mostrar su contenido (texto, actividad, evaluación).
* Emitir un reward basado en desempeño.
* Actualizar el vector S_u.
* Seleccionar próximo nodo: secuencial o adaptado.

### 5.3. **Gestión de sesiones**

* Crear sesión.
* Guardar progreso temporal.
* Mantener continuidad.

### 5.4. **APIs base**

* `/session/start`
* `/node/{id}`
* `/node/{id}/answer`
* `/profile/{id}`

---

## 6. **Requisitos no funcionales**

* Código modular y extensible.
* Baja latencia (<150 ms por request en backend local).
* Arquitectura escalable a microservicios.
* Documentación técnica clara.
* Seguridad básica: JWT + HTTPS (en etapas posteriores).

---

## 7. **MVP — Minimum Viable Product**

### **Objetivo del MVP:** validar el modelo interactivo de aprendizaje + flujo adaptativo básico.

### **Incluye:**

1. Motor de preguntas iniciales funcional.
2. Vector S_u que se actualiza correctamente.
3. 10–15 nodos educativos en JSON.
4. Backend FastAPI con:

   * Inicio de sesión.
   * Presentación de nodos.
   * Evaluación de actividades.
   * Sistema simple para elegir el siguiente nodo.
5. Persistencia en memoria (sin DB obligatoria).
6. Simulaciones básicas (arrastrar/soltar, MCQ, miniprojectos simples).
7. Sistema de reward básico.
8. Selección de nodos basada en pesos y next_nodes predefinidos.

### **No incluye:**

* IA generativa.
* UI avanzada.
* Dashboard de analytics.
* Sistema de notificaciones.
* Base de datos completa.

---

## 8. **Futuras implementaciones (Roadmap)**

### **V1.1 — Persistencia real y escalabilidad**

* Migrar de memoria a Postgres.
* Guardar historial completo de interacciones.
* Redis para manejo rápido de sesiones.

### **V1.2 — Motor adaptativo avanzado**

* Softmax + Epsilon-Greedy para exploración vs explotación.
* Decay temporal del vector S_u.
* Penalización por repetición.
* Reforzamiento dinámico (reward avanzado).

### **V1.3 — Experiencia de aprendizaje superior**

* Sistema de niveles.
* Mapa visual de progreso.
* Rutas narrativas.
* Simuladores avanzados.

### **V2.0 — Integración con IA**

* Generación dinámica de nodos educativos.
* Ajuste automático de dificultad.
* Tutor conversacional dentro de la plataforma.
* Creación de actividades personalizadas.

### **V2.5 — Plataforma colaborativa**

* Perfil de creadores.
* Subida de nuevos nodos educativos.
* Marketplace con revenue-share.

### **V3.0 — Ecosistema completo**

* App móvil.
* Aprendizaje multimodal (voz, imágenes, AR).
* Integración con empresas para entrenamiento interno.

---

## 9. **Métricas clave de éxito (KPIs)**

* Tasa de retención D1, D7, D30.
* Duración promedio por sesión.
* Profundidad de sesiones (número de nodos completados).
* Participación en micro-actividades.
* Evolución del vector S_u.
* NPS general.

---

## 10. **Riesgos y mitigaciones**

* **Riesgo:** sobrecarga de features.

  * *Mitigación:* MVP extremadamente simple.

* **Riesgo:** adaptación demasiado lenta o agresiva.

  * *Mitigación:* parámetros ajustables (ε, β, η).

* **Riesgo:** baja retención sin gamificación.

  * *Mitigación:* micro-actividades + feedback rápido.

---

## 11. **Resumen final del PRD**

Este documento define el corazón de la plataforma: visión, nodos educativos, modelo adaptativo, APIs, MVP y roadmap. El propósito es que cualquier desarrollador o diseñador pueda entender la dirección del proyecto y colaborar sin confusiones.

El siguiente paso natural es: **montar el servidor, cargar los nodos JSON y conectar el primer flujo funcional.**
