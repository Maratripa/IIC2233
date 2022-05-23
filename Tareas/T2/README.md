# Tarea 2: DCComando Espacial :school_satchel:

DCComando espacial es un juego donde se espera entrenar la IA encargada de las defensas contra los aliens que conquistaron el planeta tierra para el año 2050.

En el juego se pueden escoger 3 escenarios, tutorial, entrenamiento e invasión, cada uno más desafiante que el anterior. En cada nivel aparecerán una cierta cantidad de aliens y el objetivo es disparar a todos los aliens del nivel para poder pasar al siguiente. 

Para disparar a los aliens se cuenta con un arma de última tecnología que dispara balas especiales al presionar la tecla ```espacio```. Para mover el arma puedes presionar las teclas ```w a s d``` las cuales moverán la mira en la direccion deseada, si se presionan dos teclas no opuestas, la mira se moverá diagonalmente.

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Ventana de Inicio: 4 pts (4%)
#### Ventana de Ranking: 5 pts (5%)
#### Ventana principal: 7 pts (7%)
#### Ventana de juego: 14 pts (13%)
#### Ventana de post-nivel: 5 pts (5%)
#### Mecánicas de juego: 47 pts (45%)
##### ✅ Arma <El arma es capaz de moverse fluídamente con las teclas ```w a s d``` en las ```4 direcciones``` pedidas mas ```diagonalmente```, al disparar con la tecla ```espacio``` se produce el sonido pedido y se produce una animación de explosión cuando se dispara a un alien\>
##### ✅ Aliens y Escenario de Juego <En la ventana principal es posible seleccionar el escenario de juego, donde cada uno tiene sus propios ponderadores y sprites\>
##### ✅ Fin de Nivel <En el fin de nivel se pueden visualizar todas las estadísticas pedidas, y se puede o no continuar dependiendo si pasó el nivel o no\>
##### ✅ Fin del juego <Al finalizar el juego se vuelve al menú de inicio y se guarda el puntaje en el archivo ```puntajes.txt```\>
#### Cheatcodes: 8 pts (8%)
##### ✅ Pausa <Al presionar la tecla ```p``` el juego se pausa, impidiendo el movimiento de los aliens, el arma y parando el timer de cuenta regresiva\>
##### ✅ O + V + N + I <Al presional simultáneamente las teclas ```O + V + N + I``` se otorgan balas infinitas por la duración del nivel, además de la posibilidad de disparar más rápido\>
##### ✅  C + I + A <Al presionar simultáneamente las teclas ```C + I + A``` se pasa automáticamente de nivel, con condición de victoria y se calcula el puntaje con las estadísticas del momento\>
#### General: 14 pts (13%)
##### ✅ Modularización <El juego se encuentra dividido en backend/frontend y cada ventana tiene su propio archivo, tanto en frontend, como en backend de ser necesario\>
##### ✅ Modelación <explicacion\>
##### ✅ Archivos  <explicacion\>
##### ✅ Parametros.py <Todas las constantes se encuentran declaradas dentro del archivo ```parametros.py```\>
#### Bonus: 10 décimas máximo
##### ✅ Risa Dog <Terminator Dog produce un sonido de risa al terminar el nivel en condición de victoria\>
##### ✅ Estrella <Aleatoriamente aparece una estrella de la muerte, que cuando es disparada, resta una cierta cantidad de tiempo a la cuenta regresiva\>
##### ❌ Disparos extra <\>
##### ✅ Bomba <Aleatoriamente aparece una bomba de hielo, que congela las aliens por una cierta cantidad de tiempo\>

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```backend/``` en ```./```.

2. ```frontend/``` en ```./```.

3. ```assets/``` en ```./frontend/```.

4. ```Sonidos/``` en ```./frontend/assets/```.

5. ```Sprites/``` en ```./frontend/assets/```.

6. ```puntajes.txt``` en ```./```.

7. ```style.css``` en ```./frontend/```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```:     ```QtCore, QtWidgets, QtGui, QtMultimedia```.

2. ```sys```:       ```exit()```.

3. ```os```:        ```path.join()```.

4. ```functools```: ```partial()```.

5. ```random```:    ```random(), uniform(), choice(), randint()```.

6. ```math```:      ```pi, cos(), sin()```.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```entidades.py```: Contiene a las clases ```Mira```, ```Alien```, ```BombaHielo```, ```EstrellaMuerte```ga , ```Tiempo``` y ```Explosion```. Estas clases son utilizadas en el archivo ```backend/logica_juego.py```.

2. ```logica_juego.py```: Contiene la clase ```Juego```, esta se encarga de toda la lógica detrás de la ventana de juego.

3. ```logica_principal.py```: Contiene la clase ```LogicaPrincipal```, se encarga de la lógica detrás de la ventana principal.

4. ```ventana_inicio.py```: Contiene la clase ```VentanaInicio```, que se encarga de la interfaz de la ventana de inicio.

5. ```ventana_ranking.py```: Contiene la clase ```VentanaRanking```, que se encarga de la interfaz de la ventana de rankings.

6. ```ventana_principal.py```: Contiene la clase ```VentanaPrincipal```, que se encarga de la interfaz de la ventana principal.

7. ```ventana_juego.py```: Contiene la clase ```VentanaJuego```, que se encarga de la interfaz de la ventana de juego.

8. ```ventana_post.py```: Contiene la clase ```VentanaPost```, que se encarga de la interfaz de la ventana de post-juego.

9. ```parametros.py```: Contiene todas las constantes numéricas y rutas de archivos.

10. ```utils.py```: Contiene la función ```encapsular_h()```.

11. ```manejo_archivos.py```: Se encarga de manejar la lectura/escritura del archivo ```puntajes.txt```.


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Si un mismo usuario ya tiene un puntaje guardado, al guardar un nuevo puntaje se agregará aparte del preexistente, permitiendo a un usuario aparecer más de una vez en el ranking.

2. Para hacer del juego un poco más entretenido, se tiene un "vector" en ```parametros.py``` para la velocidad de los aliens, pero de este vector solo se utiliza la norma, que luego se aplica a un vector con direccion diagonal aleatorio en el archivo ```backend/entidades.py``` dentro de la clase ```Alien```.

3. Al disparar a la bomba de hielo, también se pausa el timer de la cuenta regresiva, para hacer que sea realmente una ventaja en los niveles con poco tiempo.

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://gist.github.com/rogerallen/f06ba704ce3befb5459239e3fdf842c7 : De este código me inspiro para ultilizar un QTimer simulando framerate y así poder actualizar el juego varias veces por segundo. Es utilizado en el archivo ```backend/logica_juego.py``` en las líneas 34-36.

2. https://stackoverflow.com/questions/13202014/passing-a-parameter-to-qtimer-timeout-signal : De aquí saco la solucion a pasar parametros a la función del timeout de un QTimer. Se utiliza en el archivo ```backend/logica_juego.py``` en las líneas 47 y 206. Consiste en utilizar la función ```partial``` de ```functools``` para crear una función con parámetros en una variable.

3. https://doc.qt.io/qtforpython-5/ : Prácticamente todo :)



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
