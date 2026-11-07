# 🦒 GiraffeCode / SavannaCode 🐆 🦦

> 🌐 **Idioma / Language:** [English (`README.md`)](README.md) | **Español (`README_ES.md`)**

**SavannaCode** (anteriormente GiraffeCode) es un juego educativo de programación diseñado para introducir a niños y niñas (de 5 a 9 años) al pensamiento computacional y los principios de la programación mediante una experiencia visual y divertida.

Los jugadores pueden elegir a su héroe animal favorito —una **Jirafa** hambrienta, un **Guepardo** veloz o una **Nutria** juguetona— y guiarlos por una cuadrícula secuenciando comandos direccionales (`AVANZAR`, `IZQUIERDA`, `DERECHA`) para alcanzar su meta (**Hojas de Acacia**, una **Gacela** o un **Pez de Río**). Mientras que la Jirafa y el Guepardo caminan por tierra firme evitando rocas y charcos de agua, la **Nutria** acuática **solo puede nadar por los canales de agua** y debe evitar las orillas de tierra y las rocas del río.

---

## 🌟 Características

- **Elige tu Héroe (3 Animales Jugables):** Pantalla interactiva de selección de personaje. ¡Juega como la **Jirafa** para alcanzar las hojas de acacia, el **Guepardo** para atrapar la gacela en la sabana o la **Nutria** para nadar por el río y atrapar el pez!
- **Depurador Paso a Paso (`PASO ⏭️`):** Herramienta educativa esencial que permite ejecutar el código instrucción por instrucción mientras la píldora de código activa se ilumina en dorado.
- **Velocidad de Ejecución Ajustable (🐢 Normal / ⚡ Rápido):** Alterna entre pasos suaves de 600ms para principiantes y velocidad turbo de 250ms para comprobar soluciones largas.
- **Selector de Niveles Paginado en 10 Capítulos (🗺️):** Cada campaña cuenta con 200 niveles organizados en 10 capítulos temáticos (20 niveles por capítulo en una cuadrícula 5x4): 10 biomas de sabana para la Jirafa/Guepardo y 10 mundos fluviales/acuáticos para la Nutria.
- **Localización Bilingüe Inglés 🇬🇧 / Español 🇪🇸:** Cambio de idioma con un solo clic (`L` o botón superior derecho) que traduce al instante todos los comandos, píldoras de código, tutoriales, diálogos y los títulos de los 400 niveles.
- **Silenciador Global de Sonido (🔊 / 🔇):** Silencia o activa todos los efectos de sonido con un clic o con la tecla `M`.
- **Efectos Visuales y de Partículas (✨):** Explosión de hojas al llegar al árbol de acacia, estrellas doradas cuando el guepardo alcanza la gacela, burbujas acuáticas y destellos cuando la nutria atrapa el pez, nubes de polvo al correr, estelas de agua al nadar y confeti de victoria.
- **Editor de Niveles Integrado (🛠️):** ¡Diseña y guarda tus propios mapas terrestres o acuáticos! Adapta automáticamente el terreno base y las herramientas al héroe seleccionado (suelo de hierba con obstáculos de roca/agua para Jirafa/Guepardo, o canales de agua con obstáculos de roca/tierra firme para la Nutria) e incluye un verificador matemático BFS que garantiza que cada nivel sea 100% resoluble antes de jugar.
- **Motor de Audio Divertido (🎵):** Efectos de sonido para pasos, giros, botones, choques y melodía de victoria con soporte automático para equipos sin tarjeta de sonido.
- **Bucles Educativos (`REPETIR`):** Enseña pensamiento computacional y estructuras de repetición.
- **400 Niveles Resolubles (200 de Sabana + 200 Acuáticos):** 200 niveles terrestres para la Jirafa y el Guepardo más 200 niveles personalizados de canales de agua para la Nutria, todos verificados matemáticamente mediante búsqueda en anchura (BFS) y con guardado de progreso independiente.
- **Deshacer (`⌫`) y Parada de Emergencia (`⏹`):** Borra únicamente el último comando con **DESHACER** (`Backspace`) o detén la ejecución al instante con **PARAR**.
- **Modos Pantalla Completa y Ventana (`F11`):** Escalado dinámico de cuadrícula que garantiza que todo el tablero sea 100% visible en cualquier monitor.

---

## 🎮 Cómo Jugar y Controles

### Objetivo
Planifica una secuencia de instrucciones para guiar a tu animal hasta la casilla de meta sin chocar contra los obstáculos (rocas y agua para Jirafa/Guepardo; orillas de tierra y rocas para la Nutria) ni salirte del tablero.

### ⌨️ Atajos de Teclado
| Tecla | Acción |
| :--- | :--- |
| **`W` o `↑ Flecha Arriba`** | Añadir comando `AVANZAR` |
| **`A` o `← Flecha Izquierda`** | Añadir comando `IZQUIERDA` |
| **`D` o `→ Flecha Derecha`** | Añadir comando `DERECHA` |
| **`R`** | Añadir bucle `REPETIR` (🔁) |
| **`Backspace (Borrar)`** | `DESHACER` el último comando (⌫) |
| **`C`** | `BORRAR` toda la cola de comandos |
| **`S`** | `PASO` (Depurador paso a paso) |
| **`Enter`** | `EJECUTAR` / `PARAR` programa |
| **`T`** | Cambiar velocidad (`Normal` / `Rápido`) |
| **`M`** | Silenciar / Activar sonido (`SÍ` / `NO`) |
| **`L`** | Cambiar idioma (`EN` / `ES`) |
| **`←` / `→` o `RePág` / `AvPág`** | Capítulo anterior / siguiente en el menú |
| **`ESPACIO`** | Siguiente nivel (tras ganar) o Reintentar (tras chocar) |
| **`ESC`** | Volver al Menú Principal / Editor |
| **`F11`** | Alternar Pantalla Completa / Ventana |

---

## 🚀 Ejecutar desde el Código Fuente

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

---

## 📦 Compilar Ejecutable Independiente (PyInstaller)

```bash
source venv/bin/activate
pyinstaller GiraffeCode.spec --noconfirm
```

El binario compilado estará disponible en:
- **Linux:** `./dist/GiraffeCode`
- **Windows:** `dist\GiraffeCode.exe`

---

## 📄 Licencia

Este proyecto es de código abierto bajo la [Licencia MIT](LICENSE).
