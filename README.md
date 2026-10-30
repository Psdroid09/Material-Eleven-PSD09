# Material-Eleven PSD09 para PS Vita

Fork de [Material-Eleven 3.9.0](https://github.com/Perroabuelo/Material-Eleven), basado en [ElevenMPV](https://github.com/joel16/ElevenMPV). Añade una forma de cambiar de pista con la pantalla apagada, inspirada en [ElevenMPV-A](https://github.com/GrapheneCt/ElevenMPV-A).

## Descargas

Consulta [Releases](https://github.com/Psdroid09/Material-Eleven-PSD09/releases).

| Variante | Control con pantalla apagada | Estado |
|---|---|---|
| `Material-Eleven-3.9.0-PSD09-joystick.vpk` | Stick derecho: izquierda = pista anterior; derecha = siguiente | Variante recomendada; probada por el usuario en PS Vita |
| `Material-Eleven-3.9.0-PSD09-cruceta.vpk` | Cruceta: izquierda = pista anterior; derecha = siguiente | Experimental; falta confirmar la lectura de botones con la pantalla apagada |

**Instala solo una variante.** Ambas utilizan el mismo identificador de aplicación, `ELEVENMPV`; instalar una sobre la otra reemplaza la instalación anterior.

## Instalación y uso

1. Descarga el VPK desde una release de este repositorio.
2. Instálalo con VitaShell como cualquier otra aplicación.
3. Abre Material-Eleven y empieza a reproducir música.
4. Pulsa START para solicitar el apagado de la pantalla.
5. En la variante joystick, mueve el stick derecho a izquierda o derecha para cambiar de pista. Vuelve a la zona central antes de hacer otro cambio; así se evita repetir la acción mientras mantienes el stick inclinado.

La variante joystick requiere que el control analógico esté disponible para la aplicación. El parche habilita el muestreo analógico y procesa el movimiento dentro del ciclo normal de lectura de controles; no crea un hilo adicional.

## Compatibilidad y alcance

- Proyecto dirigido a PS Vita y compilado con VitaSDK.
- La variante joystick está probada por el usuario en una PS Vita; no se publica una matriz completa de modelos, firmwares o tarjetas.
- La variante cruceta sigue siendo experimental.
- No requiere instalar plugins taiHEN adicionales ni modificar `ur0:tai/config.txt`.
- El parche no está diseñado para modificar firmware, Ensō, YAMT ni el montaje de almacenamiento.

## Compilación

GitHub Actions obtiene Material-Eleven 3.9.0, aplica el parche de la variante seleccionada desde `scripts/` y compila el VPK con VitaSDK. Los artefactos de compilación se pueden revisar en la ejecución correspondiente de Actions.

Los cambios en los scripts o en este workflow ejecutan la compilación, pero **no publican ni reemplazan una release automáticamente**. La publicación se inicia manualmente desde Actions y debe habilitarse expresamente. Se utiliza una etiqueta nueva para evitar sobrescribir releases existentes.

## Desinstalación

Se desinstala desde el menú de burbujas de PS Vita, como una aplicación normal. Si vas a volver a la versión original, instala el VPK oficial de Material-Eleven. La desinstalación de esta aplicación no requiere borrar archivos de taiHEN ni modificar la configuración del sistema.

## Créditos y licencia

- [Material-Eleven](https://github.com/Perroabuelo/Material-Eleven)
- [ElevenMPV](https://github.com/joel16/ElevenMPV)
- [ElevenMPV-A](https://github.com/GrapheneCt/ElevenMPV-A), inspiración para el control con stick

El código derivado de Material-Eleven se distribuye bajo GNU GPL-3.0-or-later. Se deben conservar los avisos, créditos y licencias de los proyectos originales.
