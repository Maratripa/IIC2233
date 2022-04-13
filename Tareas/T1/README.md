# Tarea 1: DCCasino :school_satchel:

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Programación Orientada a Objetos: 38 pts (28%)
##### ✅  Diagrama <Se encuentra en un archivo llamado diagrama.jpeg>
##### ✅ Definición de clases, atributos, métodos y properties <explicacion\>
##### ✅ Relaciones entre clases <Todas las subclases heredan correctamente los métodos y atributos>
#### Simulaciones: 10 pts (7%)
##### ✅ Crear partida <explicacion\>
#### Acciones: 35 pts (26%)
##### ✅ Jugador <explicacion\>
##### ✅ Juego <explicacion\>
##### ✅ Bebestible <explicacion\>
##### ✅ Casino <explicacion\>
#### Consola: 41 pts (30%)
##### ✅ Menú de Inicio <explicacion\>
##### ✅ Opciones de jugador <explicacion\>
##### ✅ Menú principal <explicacion\>
##### ✅ Opciones de juegos <explicacion\>
##### ✅ Carta de bebestibles <explicacion\>
##### ✅ Ver estado del Jugador <explicacion\>
##### ✅ Robustez <explicacion\>
#### Manejo de archivos: 13 pts (9%)
##### ✅ Archivos CSV  <El manejo de csv se encuentra en manejo_csv.py, está diseñado para que funcione concualquier orden de headers.>
##### ✅ parametros.py <Todos los valores están declarados en parametros.py y no hay valores hardcodeados>
#### Bonus: 3 décimas máximo
##### ✅ Ver Show <explicacion\>


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
2. ```entidades```: Contiene a ```Jugador```, ```Juego```, ```Bebestible``` y sus respectivas clases hijas.
3. ```manejo_csv```: Hecha para trabajar con los archivos csv en un solo lugar.
4. ```parametros```: Hecha para contener todos los valores usados a lo largo del código.

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
