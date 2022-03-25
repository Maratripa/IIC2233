# Tarea X: Nombre de la tarea :school_satchel:


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<DCCorreos es un programa que simula una empresa de correos, donde existen los usuarios que pueden crear y mandar encomiendas, revisar las encomiendas creadas, realizar reclamos y ver las encomiendas que tienen como destinatario al usuario. También se permite el registro de nuevos usuarios con un usuario y contraseña. Además, el administrador puede iniciar sesión para revisar y actualizar todas las encomiendas, además de revisar todos los reclamos creados.>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️
#### Menú de Inicio (18pts) (18%)
##### ✅ Requisitos <explicacion\>
##### ✅ Iniciar sesión <Implementado.\>
##### ✅ Ingresar como administrador <Implementado.\>
##### ✅ Registrar usuario <Implementado.\>
##### ✅ Salir <Implementado usando sys.exit().\>
#### Flujo del programa (31pts) (31%) 
##### ✅ Menú de Usuario <Implementado completamente.\>
##### ✅ Menú de Administrador <Implementado completamente.\>
#### Entidades 15pts (15%)
##### ✅ Usuarios <Esta entidad está implementada en su totalidad.\>
##### ✅ Encomiendas <Esta entidad está implementada en su totalidad.\>
##### ✅ Reclamos <Esta entidad está implementada en su totalidad.\>
#### Archivos: 15 pts (15%)
##### ✅ Manejo de Archivos <Todos los archivos se abren con encoding "utf'8" y no se usa el modo 'w' a menos que sea necesario o contraproductivo no usarlo. Se usan paths relativos para todos los archivos.\>
#### General: 21 pts (21%)
##### ✅ Menús <Todos los menús están implementados.\>
##### ✅ Parámetros <El archivo parámetros no fue modificado.\>
##### ✅ Módulos <Se utiliza un archivo para cada entidad, ningún archivo supera las 400 líneas.\>
##### ✅ PEP8 <Todos los archivos .py cumplen con la norma PEP8.\>
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```csv/``` en ```T0/```
2. ```entidades/``` en ```T0/```
3. ```encomiendas.csv``` en ```T0/csv/```
4. ```reclamos.csv``` en ```T0/csv/```
5. ```usuarios.csv``` en ```T0/csv/```
6. ```__init__.py``` en ```T0/entidades/```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```datetime```: ```now().strftime() / datetime```.
2. ```sys```: ```exit()```.
3. ```os```: ```join() / path```.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```usuario```: Contiene a la clase ```UsuarioRegistrado```, que se encarga del menú y las funciones de un usuario registrado.
2. ```encomienda```: Contiene a la clase ```Encomienda```, que se encarga de crear las encomiendas con sus respectivos atributos.
3. ```reclamo```: Contiene a la clase ```Reclamo```, que se encarga de crear los reclamos con sus respectivos atributos.
4. ```administrador```: Contiene a la clase ```Admin```, que se encarga del menú y las funciones del administrador.
2. ```archivos```: Hecha para mantener el uso de **open()** en un solo módulo.
3. ```funciones```: Contiene funciones para el estilo del output y manejo de inputs.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Las encomiendas que el usuario crea en sesión, dejan de estar disponibles en su menú después de cerrar sesión, incluso si ingresa de nuevo en una misma ejecución del código. Esto con el fin de evitar tener una lista, diccionario o archivo grande para contener las encomiendas creadas, solo para borrarlo una vez termine la ejecución del código.

2. Al momento de mostrar las encomiendas, se puede cortar el largo de las entradas, con el fin de hacer que queden bien en el formato de tabla. Se justifica porque de todas maneras hay suficientes carácteres en cada una de las entradas para que se entienda el contenido.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory>: De esta respuesta es que manejo el uso de módulos en subdirectorios, usando un archivo __init__.py.


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
