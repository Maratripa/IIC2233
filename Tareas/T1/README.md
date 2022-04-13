# Tarea 1: DCCasino :school_satchel:

## Consideraciones generales :octocat:

El DCCasino simula un casino con varias opciones de jugadores. Al elegir un jugador, comienza la partida y te encuentras ante el menú principal, de ahí hay varias opciones: menú de juegos, menú de bebestibles, ver el estado del jugador y ver un show, además de volver al menú de inicio y jugar con otro jugador y de salir del juego.
Los jugadores existen aparte del casino, por lo que si juegas con un personaje, y vuelves al menú de inicio, el progreso del jugador queda guardado. De la misma manera, si un jugador queda en quiebra, ya no estará disponible para ser utilizado. Al tener el dinero suficiente para pagar la deuda, se dará la opción al usuario de pagarla y salir o de seguir jugando, en caso de que pierda dinero, se quitará la opción.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Programación Orientada a Objetos: 38 pts (28%)
##### ✅  Diagrama <Se encuentra en un archivo llamado diagrama.jpeg\>
##### ✅ Definición de clases, atributos, métodos y properties <Las clases se encuentran repartidas entre tres archivos, las sub-clases se encuentran todas en el mismo archivo que la clase padre\>
##### ✅ Relaciones entre clases <Todas las subclases heredan correctamente los métodos y atributos\>
#### Simulaciones: 10 pts (7%)
##### ✅ Crear partida <Al crear una partida se crea una lista con todos los jugadores disponibles y una instancia del DCCasino. Se puede volver y jugar con distintos personajes en una misma "partida"\>
#### Acciones: 35 pts (26%)
##### ✅ Jugador <Se encuentran implementadas las aciones de comprar_bebestible y apostar, además de las habilidades de cada personalidad\>
##### ✅ Juego <Los juegos tienen implementados todos sus respectivos métodos\>
##### ✅ Bebestible <Los bebestibles tienen implementados el método de consumir, además de las modificaciones de las sub-clases\>
##### ✅ Casino <El casino tiene implementados todos los métodos de los menúes\>
#### Consola: 41 pts (30%)
##### ✅ Menú de Inicio <El menú de inicio es la entrada al jugador, donde este puede entrar al casino eligiendo un personaje o salir de el juego\>
##### ✅ Opciones de jugador <En las opciones de jugador se muestra cada personaje con su personalidad. Se muestran solo los personajes que no están en quiebra\>
##### ✅ Menú principal <En el menú principal se muestran las opciones para ir al menú de juegos, menú de bebestibles, ver el show, y en caso de estar disponible la opción, pagar la deuda\>
##### ✅ Opciones de juegos <En el menú de juegos se enumeran todos los juegos y se pueden seleccionar solo aquellos en los que se puede apostar (cuando se tiene más dinero que la apuesta mínima)\>
##### ✅ Carta de bebestibles <En la carta de bebestibles se muestran todos los bebestibles con su tipo y precio, también se muestra el dinero disponible del jugador\>
##### ✅ Ver estado del Jugador <En el estado del jugador se imprimen todos los atributos acutales del jugador\>
##### ✅ Robustez <En cada menú están las opciones para volver al menú anterior o salir del juego (cuando se está apostando en un juego no se puede salir, pero si volver). Todos los inputs cuentan con validación de string, para que no se pueda ingrasar un valor no válido\>
#### Manejo de archivos: 13 pts (9%)
##### ✅ Archivos CSV  <El manejo de csv se encuentra en manejo_csv.py, está diseñado para que funcione concualquier orden de headers\>
##### ✅ parametros.py <Todos los valores están declarados en parametros.py y no hay valores hardcodeados\>
#### Bonus: 3 décimas máximo


##### ✅ Ver Show <Se elige un show al azar y se modifican los atributos del jugador actual\>


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```bebestibles.csv``` en ```.```
2. ```juegos.csv``` en ```.```
3. ```jugadores.csv``` en ```.```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```sys```: ```exit()```.
2. ```random```: ```random() y choice()```.
3. ```abc```: ```Clase ABC y decorador @abstractmethod```.
4. ```os```: ```path.dirname(), path.realpath() y path.join()```.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```casino```: Contiene a ```Casino```.
2. ```entidades```: Contiene a ```Juego```, ```Bebestible``` y sus respectivas sub-clases.
3. ```jugador```: Contiene a ```Jugador``` y sus respecticas sub-clases
4. ```manejo_csv```: Hecha para trabajar con los archivos csv en un solo lugar.
5. ```parametros```: Hecha para contener todos los valores usados a lo largo del código.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Para el bonus de Show, considero que no es necesario crear una clase dedicada, ya que se puede implementar el show a través de un método de la clase ```Casino```.
2. En el menú de juegos, si se apuesta $0 se cancela la apuesta y se vuelve al menú anterior, ya que no tiene sentido poder apostar $0 y tener la posibilidad de activar un evento especial o alguna habilidad de jugador.
3. Las cantidades que se suman o restan al jugador con la habilidad ludopatia deberían estar en parametros.py, ya que no se deberían hardcodear estos valores.
4. Si el jugador se queda sin energía, no podrá seguir apostando, pero podrá realizar otras acciones para poder recuperar energía.
5. Si el jugadro se queda sin dinero, se vuelve al menú de inicio, y se puede empezar de nuevo con otro jugador, pero el que se quedó sin dinero ya no estará disponible.
6. Si el jugador recolecta el dinero suficiente para terminar, tendrá la opción de seguir jugando y en el menú principal aparecerá la opción para terminar el juego.
7. Para que no hayan probabilidades de apuesta negativas, se hace uso se la funcion max(0, probabilidad) para que devuelva 0 en este caso.

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory: Código para obtener path de ejecución del archivo y está implementado en el archivo ```manejo_csv.py``` en las líneas 7, 48 y 74.


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
