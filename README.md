# ModuloSxe
## _Objetivo_
El objetivo ha sido modificar el módulo de librerías e implementar nuevas funcionalidades, entre ellas adaptarse a un supuesto nuevo requerimiento que dicta que los libros pueden estar un máximo de 30 días en préstamo y dar la posibilidad de agregar un precio al alquiler de estos.
## _Estructura_
La estructura de las vistas generales es:
- **Books**:
    En la vista general se ve como default una vista **Kanban** donde se puede ver claramente la foto de cada libro y se organizan los libros por columnas según su estado. También se puede variar entre las vistas **Calendar** donde se posicionan los libros según su fecha de préstamo y una vista **Tree** con información más detallada. Al crear o editar un registro se nos abrirá la vista **Form**.
  
- **Books Categories**:
    Tiene una vista **Tree** que muestra la información de una categoría.
    
## _Nuevas Funcionalidades:_
   En la vista **Form** se modificó algo la estética de los botones de estado, haciendo invisibles algunos, pero manteniendo en código en los .py para posibles modificaciones futuras, además ahora cuando un libro tiene un estado el botón que lo permitía cambiar a ese mismo estado desaparece haciendo la vista más amable para el usuario. Se utilizó la herencia de módulo "mail" para añadir la funcionalidad que nos permite mandar mensajes desde dentro del módulo a clientes, por ejemplo, para notificar que el plazo para devolver su libro se está acabando o a otros usuarios, además permite planificar una actividad, agregar notas, seguir la actividad de un registro... y tener un registro de las modificaciones en los atributos de un libro, guardando la fecha y el usuario que los realizo.
   El nuevo campo calculado "Remaining days" calcula los días restantes, restando a la fecha del préstamo+30 días la fecha actual y devolviendo los días restantes, cuando un libro supera ese para se le asigna automáticamente el estado "lost".
   
## _En la segunda versión:_
Se han corregido los errores gramaticales y traducciones, se añadió una nueva funcionalidad que permite crear una orden de venta, ayudándose de "sale.order" donde se añadió un campo relacionado a "library book" , ahora al darle a un libro el estado "Avaliable" aparecerá un nuevo botón para crear la orden de venta, y se logró que dentro de la orden de venta, al confirmarla, el libro cambie de estado "Avaliable" a "Borrowed", además ahora el usuario al introducir una fecha posterior a la actual es avisado con una ventana de lo sucedido.
   
## _Futuras Mejoras:_   
  Implementar la gestión de las facturas despues de realizar una orden de venta.
  
## _Autor_
_Jacobo Fernández Barreiro_  
