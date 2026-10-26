# Reto Unidad 5: Análisis Visual de Datos Reales

**Estudiante:** Jose Miguel Vasquez Echavarria y Isabela Motaño
**Materia:** Programación

## ¿Qué datos usé y de dónde salieron?

Para este proyecto escogí dos tipos de archivos para probar que el programa sí sirve para cosas del mundo real:

*   **El CSV (ventas.csv):** Es un registro de ventas de una tienda. Básicamente tiene columnas de fechas, ciudades (Bogotá, Medellín, Cali), qué se vendió (Tecnología, Ropa, Hogar) y por cuánto. Lo armé basándome en datasets reales que encontré en Kaggle. Me gustó este tema porque así puedo ver gráficas de tendencias y de categorías, tal como pide el reto.

*   **El TXT (log.txt):** Es un archivo de registro (log) sacado de un servidor web. Estos archivos son los que guardan todo lo que pasa cuando entras a una página (las peticiones, las imágenes que cargan, etc.). Sirve perfecto para la parte de buscar patrones, porque ahí aparecen los típicos errores "404" o "500".

## Mis conclusiones (lo que descubrí con las gráficas)

Después de correr el programa y ver los gráficos, esto fue lo que más me llamó la atención:

1.  **El pico de ventas (Gráfico de Líneas):** Mirando el gráfico de tendencia, noté que las ventas son más o menos normales durante el año, pero en **Agosto** se disparan feo (llegan a 1700.00). Creo que esto pasa porque es la temporada de regreso a clases o hubo alguna promo fuerte ese mes.
2.  **Tecnología manda la parada (Gráfico de Pastel):** El gráfico de pastel muestra clarísimo que la categoría de **Tecnología** es la que más vende, por mucho. Ropa y Hogar se reparten lo que queda. Esto tiene sentido porque en el CSV se nota que los productos tech son los que dejan más plata por transacción.
3.  **No todo es cantidad (Gráfico de Dispersión):** Hice un gráfico de dispersión cruzando la cantidad de productos con el monto de la venta, y me di cuenta de que no siempre comprar más significa pagar más. Por ejemplo, alguien puede comprar 3 camisetas por 350.000, pero otra persona compra solo 1 celular y paga 1.500.000. Los puntos en la gráfica quedan súper dispersos.
4.  **El servidor está fallando (Análisis de texto):** Al usar la opción de buscar patrones en el archivo .txt, busqué la palabra "ERROR" y "404". Encontré varios. Hay imágenes que no cargan (`missing-image.jpg`) y errores de base de datos (Error 500). Conclusión: el dueño de esa página web tiene que arreglar esos enlaces ya mismo.

## Notas técnicas (Cosas que tuve que resolver)

*   **Cálculos a mano:** Como en la rúbrica decía que no podíamos usar pandas ni numpy, me tocó programar la fórmula del promedio y la mediana yo mismo con Python puro. Para la mediana, tuve que ordenar la lista y usar un `if` para ver si la cantidad de datos era par o impar y así sacar el valor del medio. 
*   **Datos sucios:** En el CSV dejé a propósito un par de celdas vacías (en la columna de Monto_Venta) para demostrar que el programa es lo suficientemente inteligente para ignorar esos datos nulos y no explotar cuando hace los cálculos.