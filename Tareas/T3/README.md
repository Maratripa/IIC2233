# Tarea 3: DCCasillas :school_satchel:
## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

#### Networking: 23 pts (18%)
##### ✅ Protocolo <Se utiliza protocolo TCP/IP para la conexión servidor-cliente\>
##### ✅ Correcto uso de sockets <Se crean los sockets de manera correcta y se utilizan threads para trabajar concurrentemente\>
##### ✅ Conexión <La conexión se mantiene estable a lo largo de todo el juego\>
##### ❌✅🟠 Manejo de clientes <Se pueden conectar múltiples clientes, por lo menos más de la cantidad máxima de jugadores\>
#### Arquitectura Cliente - Servidor: 31 pts (25%)
##### ✅ Roles <El cliente está separado del servidor y cada las tareas se reparten acorde al enunciado\>
##### ✅ Consistencia <Todos los clientes se actualizan como se espera y se utiliza un lock para el envío de información\>
##### ❌✅🟠 Logs <explicacion\>
#### Manejo de Bytes: 26 pts (21%)
##### ✅ Codificación <El mensaje se codifica según el enunciado, utilizando big endian y little endian correspondientemente\>
##### ✅ Decodificación <El mensaje se decodifica según el enunciado, obteniendo cada uno de los parametros con su respectivo byteorder\>
##### ✅ Encriptación <La encriptación funciona según el enunciado, separando el mensaje en dos partes y ordenandolos según sus valores del medio\>
##### ✅ Desencriptación <Se logra recuperar el mensaje original solo a traves del mensaje encriptado\>
##### ✅ Integración <Se utiliza el protocolo de envío para toda comunicación entre servidor y cliente\>
#### Interfaz: 23 pts (18%)
##### ✅ Ventana inicio <Se muestran todos los elementos y se verifica si el usuario cumple con todos los requisitos\>
##### ✅ Sala de Espera <Se muestran todos los elementos, se inicia la partida al llegar a la cantidad máxima de usuarios, y el admin puede iniciar la partida antes en caso de cumplir con la cantidad mínima de usuarios\>
##### ✅ Sala de juego <Se muestran todos los elementos, la información se actualiza para todos los jugadores, se ve quien es el jugador de turno, y solo ese jugador puede tirar el dado, el rango del dado es entre 1 y 3, el jugador se mueve correctamente por las casillas blancas hasta llegar a la recta de su color y se redirige a la ventana final cuando uno de los jugadores logra avanzar sus dos fichas al la casilla de victoria\>
##### 🟠 Ventana final <Se muestran todos los elementos, se indica el ganador de la partida y hay un botón que redirige a la ventana de inicio, pero no se puede volver a jugar\>
#### Reglas de DCCasillas: 18 pts (14%)
##### ✅ Inicio del juego <Se asignan los turnos por orden de llegada a la sala de espera y los colores son aleatorios\>
##### ✅ Ronda <El jugador de turno tiene la opcion de tirar el dado, las fichas se mueven correctamente, la segunda ficha se mueve unicamente cuando la primera ya llegó a la casilla de victoria, la acción de comer una ficha esta implementada correctamente y se calcula correctamente la cantidad de casillas avanzadas\>
##### ✅ Termino del juego <Se asigna correctamente el ganador según quién logra llevar sus dos fichas a la casilla de victoria\>
#### General: 4 pts (3%)
##### ✅ Parámetros (JSON) <Todos los parametros se encuentran en un archivo json\>
#### Bonus: 5 décimas máximo
##### ❌✅🟠 Cheatcode <explicacion\>
##### ❌✅🟠 Turnos con tiempo <explicacion\>
##### ❌✅🟠 Rebote <explicacion\>

## Ejecución servidor :computer:
El módulo principal de la tarea a ejecutar es  ```servidor/main.py``` desde el directorio ```servidor/```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```servidor/``` en ```./```
2. ```parametros.json``` en ```./servidor/```

## Ejecución cliente :computer:
El módulo principal de la tarea a ejecutar es  ```cliente/main.py``` desde el directorio ```cliente/```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```cliente/``` en ```./```
2. ```backend/``` en ```./cliente/```
3. ```frontend/``` en ```./cliente/```
4. ```Sprites/``` en ```.cliente/frontend/```
5. ```parametros.json``` en ```./cliente/```
6. ```style.css``` en ```./cliente/frontend/```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé para el cliente fue la siguiente:

1. ```json```: ```dumps(), loads(), load()```
2. ```socket```: ```socket```
3. ```threading```: ```Thread```
4. ```PyQt5```: ```QtCore, QtWidgets, QtGui```
5. ```sys```: ```argv, exit()```
6. ```os```: ```path```

La lista de librerías externas que utilicé para el servidor fue la siguiente:

1. ```json```: ```dumps(), loads(), load()```
2. ```socket```: ```socket```
3. ```threading```: ```Thread, Lock```
4. ```sys```: ```exit()```
5. ```os```: ```path```
6. ```random```: ```shuffle(), randint()```

### Librerías propias
Por otro lado, los módulos que fueron creados para el cliente fueron los siguientes:

1. ```./cliente/utils.py```: contiene funciones logicas utilizadas por el cliente
2. ```./cliente/backend/cliente.py```: Contiene a ```Cliente```, clase encargada de manejar la conexión con el servidor
3. ```./cliente/backend/interfaz.py```: Contiene a ```Interfaz```, clase encargada de conectar el cliente con la interfaz gráfica
4. ```./cliente/frontend/ventana_inicio.py```: Contiene a ```VentanaInicio```
5. ```./cliente/frontend/ventana_espera.py```: Contiene a ```VentanaEspera```
6. ```./cliente/frontend/ventana_juego.py```: Contiene a ```VentanaJuego```
7. ```./cliente/frontend/ventana_final.py```: Contiene a ```VentanaFinal```

Por otro lado, los módulos que fueron creados para el servidor fueron los siguientes:

1. ```./servidor/servidor.py```: Contiene a ```Servidor```, clase encargada de manejar las conexiones con los clientes
2. ```./servidor/logica.py```: Contiene a ```Logica```, clase encargada de la lógica detrás del servidor
3. ```./servidor/utils.py```: contiene funciones logicas utilizadas por el servidor

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <Descripción/consideración 1 y justificación del por qué es válido/a> 
2. <Descripción/consideración 2 y justificación del por qué es válido/a>
3. ...

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<link de código>: este hace \<lo que hace> y está implementado en el archivo <nombre.py> en las líneas <número de líneas> y hace <explicación breve de que hace>

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
