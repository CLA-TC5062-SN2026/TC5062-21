# Evaluación básica de accesibilidad

Equipo 21 · 3 de noviembre de 2026. Alcance: login, componentes, panel, inventario y detalle; contraste, teclado, nombres accesibles y adaptación móvil. Referencia: WCAG 2.1 AA. Esta revisión no acredita conformidad completa ni incluyó lector de pantalla o pruebas con personas usuarias.

## Problemas encontrados y corregidos

| Problema real en la primera versión | Corrección aplicada | Criterio de referencia |
| --- | --- | --- |
| Borde de campo `#becdc7` sobre blanco: **1.65:1**. El contorno no distinguía suficientemente el control. | `#7c9186`: **3.36:1**, aplicado a Input y selectores. | [1.4.11 Contraste no textual](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html): 3:1 para información visual necesaria para identificar componentes/estados. |
| Ayuda pequeña `#74826c` sobre `#fafcf7`: **3.95:1**. | `#5d705c`: **5.16:1**. Nota de inventario también ajustada a `#536b58` sobre `#f6f8f5`: **5.44:1**. | [1.4.3 Contraste mínimo](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html): 4.5:1 para texto normal. |
| Escape cerraba el menú móvil sin devolver explícitamente el foco al botón de apertura. | Navbar conserva una referencia al disparador y le devuelve el foco. | Apoya [2.1.1 Teclado](https://www.w3.org/WAI/WCAG21/Understanding/keyboard.html) y [2.4.3 Orden del foco](https://www.w3.org/WAI/WCAG21/Understanding/focus-order.html). Escape es la conducta elegida para el menú, no un requisito textual del criterio. |

Se calculó luminancia relativa sRGB con `python3 scripts/verificar_contraste.py`. `evidencias/contraste.json` conserva ocho pares: texto principal **13.11:1**, secundario **5.28:1**, botón primario **6.43:1**, tres correcciones anteriores y foco sobre fondos claro/oscuro **4.58:1 / 3.21:1**. El umbral se evalúa sin redondear. Estas mediciones no implican que todos los estados o píxeles hayan sido auditados.

## Nombres y errores

- Input exige etiqueta visible asociada; el placeholder solo aporta un ejemplo. Error/ayuda usan identificadores únicos y aria-describedby; errores usan aria-invalid ([3.3.1 Identificación de errores](https://www.w3.org/WAI/WCAG21/Understanding/error-identification.html), [3.3.2 Etiquetas o instrucciones](https://www.w3.org/WAI/WCAG21/Understanding/labels-or-instructions.html)).
- Menú y cierre de sesión tienen nombre; iconos decorativos usan aria-hidden. El menú expone aria-expanded/aria-controls ([4.1.2 Nombre, función, valor](https://www.w3.org/WAI/WCAG21/Understanding/name-role-value.html)).
- La carga tiene texto y región de estado. Errores HTTP/red muestran avisos y reintento. El formulario lleva el foco al primer campo inválido o al aviso de credenciales rechazadas; el error no depende solo del color.

## Foco y adaptación

Los controles HTML conservan foco visible mediante `:focus-visible`. Hay enlace para saltar al contenido y cambios de título/foco principal al navegar ([2.4.7 Foco visible](https://www.w3.org/WAI/WCAG21/Understanding/focus-visible.html), [2.4.1 Evitar bloques](https://www.w3.org/WAI/WCAG21/Understanding/bypass-blocks.html)).

Se probó Chrome a 390 × 844: tarjetas/filtros se apilan, el menú se abre/cierra y Escape devuelve el foco. La tabla puede desplazarse en su contenedor sin desbordar el documento. Evidencia: `evidencias/movil.jpg`. Es una comprobación de ese tamaño, no cobertura completa de reflujo 1.4.10.

Tres pruebas de componentes verifican etiqueta/error, identificadores únicos y bloqueo durante carga. `componentes.jpg`, `movil.jpg` y capturas de A2 muestran los estados. Los estilos respetan movimiento reducido. Quedan pendientes auditoría exhaustiva, combinaciones navegador/lector y evaluación con usuarios.
