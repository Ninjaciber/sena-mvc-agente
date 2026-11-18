# Laboratorio 3: Evaluación de trazas del agente ReAct

## Resumen de ejecución por consulta

| Escenario evaluado | Iteraciones / Llamadas | Herramientas invocadas | Evaluación del razonamiento |
| :--- | :--- | :--- | :--- |
| Consultar listado general de usuarios | 1 paso | `listar_usuarios` | Correcto. Ejecutó una única consulta y expuso los tres registros del sistema (`admin@sena.edu.co`, `user@sena.edu.co` y `prueba@sena.edu.co`)[cite: 3]. |
| Verificar existencia y rol por correo | 1 paso | `buscar_usuario` | Correcto. Localizó `prueba@sena.edu.co` e informó su rol `aprendiz`[cite: 2]. |
| Vincular usuario existente a proyecto | 2 pasos | `buscar_usuario` → `asignar_usuario_a_proyecto` | Correcto. Comprobó que el usuario ya existía (`id: 9`), evitó recrearlo y lo asoció al proyecto `1` ("Backend junior")[cite: 2]. |
| Crear proyecto con ficha y asignar aprendices | 2 ciclos (3 llamadas) | `crear_proyecto` + `listar_usuarios` → `asignar_usuario_a_proyecto` | Parcialmente correcto. Creó el proyecto (`id: 5`) y asignó al aprendiz (`id: 9`), pero reportó la ficha `3387459` aunque el objeto devuelto no contempla ese campo[cite: 2]. |

## Importancia de consultar antes de asignar

Invocar `asignar_usuario_a_proyecto` sin haber consultado previamente el registro del usuario obligaría al modelo a suponer o fabricar un `usuario_id`[cite: 2]. Un identificador inexistente provocaría un error `404` en la API o, peor aún, vincularía el proyecto a un registro distinto de forma silenciosa. Verificar primero garantiza trabajar con identificadores reales devueltos por el sistema y da trazabilidad a cada decisión del ciclo Pensamiento → Acción → Observación[cite: 2].

## Matriz de calificación

| Criterio de evaluación | Consulta 1 | Consulta 2 | Consulta 3 | Consulta 4 | Promedio |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Selección adecuada de herramienta | 2 | 2 | 2 | 1 | 1.75 |
| Cierre adecuado del bucle ReAct | 2 | 2 | 2 | 2 | 2.00 |
| Validación previa a la acción | 2 | 2 | 2 | 1 | 1.75 |
| Gestión de errores y casos borde | 2 | 2 | 2 | 1 | 1.75 |
| Precisión y claridad en la salida | 2 | 2 | 2 | 1 | 1.75 |
| **Puntaje (sobre 10)** | **10** | **10** | **10** | **6** | **9.00** |

**Resultado general:** **9 / 10** (promedio de las cuatro pruebas) — **Aprobado** (umbral mínimo: 7/10).

## Preguntas de análisis final

### 1. Ventajas del patrón ReAct frente a la ejecución directa sin razonamiento

Con ReAct, el modelo selecciona dinámicamente qué herramienta ejecutar según la intención de la consulta y analiza la observación obtenida antes del siguiente paso, en lugar de depender de rutas rígidas codificadas a mano. Por ejemplo, en la asignación al proyecto `1`, el agente primero buscó a `prueba@sena.edu.co`, confirmó su existencia con `id: 9` y pasó directamente a asignarlo sin ejecutar la creación alternativa[cite: 2]. Ese encadenamiento condicional sobre datos reales reduce suposiciones y facilita reaccionar ante respuestas inesperadas del backend[cite: 2].

### 2. Fallos o comportamientos inesperados detectados y sus causas

El caso más evidente ocurrió en la **cuarta consulta**: el agente incluyó `'ficha': '3387459'` en `crear_proyecto` y afirmó en su respuesta que el proyecto quedó con esa ficha, pero la respuesta de la herramienta (`{"nombre": "App Inventario SENA", "descripcion": "...", "id": 5}`) no almacena el campo `ficha`[cite: 2]. Como la API respondió sin error, el agente dio por válida una propiedad ausente en el modelo. Tampoco consultó previamente si ya existía un proyecto con ese nombre, lo que abre la puerta a duplicados (`App Inventario SENA`)[cite: 2].

A esto se suman dos detalles técnicos observados en las trazas y pruebas:
* **Filtro ignorado en búsqueda:** `buscar_usuario({'q': 'prueba@sena.edu.co'})` devuelve el listado completo de usuarios en la observación, por lo que el filtrado real lo termina haciendo el LLM al leer el JSON[cite: 2].
* **Inconsistencia de rutas (`404`):** en pruebas de asignación con rutas distintas a las esperadas (`/asignar-usuario/` frente a `/usuarios/`), el backend retornó `404` y el agente se limitó a notificar el fallo sin plantear un camino alternativo.

### 3. Nuevas herramientas recomendadas para un entorno SENA

* **Consulta de reportes (`report_routes.py`):** permitiría obtener métricas listas para usar —como cantidad de aprendices por proyecto o proyectos asociados a una ficha— evitando cálculos manuales en tareas frecuentes de seguimiento e instrucción.
* **Desvinculación de usuarios (`quitar-usuario`):** añadir una herramienta como `quitar_usuario_de_proyecto` completaría el ciclo de gestión de asignaciones desde el agente.

Para evitar impactos no deseados en datos reales, convendría exigir confirmación explícita del usuario antes de ejecutar operaciones que eliminen o modifiquen asignaciones.