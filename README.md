# Material-Eleven PSD09 para PS Vita

Modificación experimental de [Material-Eleven 3.9.0](https://github.com/Perroabuelo/Material-Eleven), basada en [ElevenMPV](https://github.com/joel16/ElevenMPV) y con la idea de control mediante stick durante pantalla apagada de [ElevenMPV-A](https://github.com/GrapheneCt/ElevenMPV-A).

## Descargar

Consulta la sección [Releases](https://github.com/Psdroid09/Material-Eleven-PSD09/releases).

En la release **v3.9.0-PSD09.1** hay dos VPK:
- **Material-Eleven-3.9.0-PSD09-joystick.vpk**: joystick derecho, hacia izquierda o derecha, cambia la pista mientras la pantalla está apagada tras usar START. **Probado en PS Vita por el usuario.**
- **Material-Eleven-3.9.0-PSD09-cruceta.vpk**: cruceta izquierda/derecha, **experimental**; todavía falta probar si las entradas digitales llegan con la pantalla apagada.

Solo debes instalar uno a la vez. Ambos usan el ID `ELEVENMPV` y sustituyen la instalación anterior.

## Cómo se compila

GitHub Actions descarga el código de Material-Eleven 3.9.0, aplica el parche seleccionado desde `scripts/` y compila usando VitaSDK. Los VPK se publican automáticamente en Releases. Se conservan las licencias originales incluidas en cada VPK.

## RepoHub y privacidad

**El repositorio es privado.** RepoHub (robDevs) obtiene repositorios mediante el endpoint `/users/{owner}/repos` de GitHub, que no lista repositorios privados. Por ello, aunque exista una release, no se puede garantizar que aparezca al buscarla desde RepoHub. Para RepoHub la opción más compatible es hacer público el repositorio, **solo si su dueño decide cambiar la visibilidad**.

## Licencia

Código derivado de Material-Eleven bajo GNU GPL-3.0-or-later; se mantienen créditos, avisos y licencias del proyecto original dentro del VPK.
