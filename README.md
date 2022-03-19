# ModuloSxe
## _Objetivo_
El objetivo ha sido modificar el módulo de librerías e implementar nuevas finalidades, entre ellas adaptarse a un supuesto nuevo requerimiento que dicta que los libros pueden estar un máximo de 30 días en préstamo.
## _Estructura_
La estructura de las vistas generales es:
- **Books**:
    En la vista general se ve como default una vista **Kanban** donde se puede ver claramente la foto de cada libro y se organizan los libros por columnas según su estado. También se puede variar entre las vistas **Calendar** donde se posicionan los libros según su fecha de préstamo y una vista **Tree** con información más detallada. Al crear o editar un registro se nos abrirá la vista **Form**.
  
- **Books Categories**:
    Tiene una vista **Tree** que muestra la información de una categoría.
    
## _Nuevas Funcionalidades:_
   En la vista **Form** se modificó algo la estética de los botones de estado, haciendo invisibles algunos, pero manteniendo en código en los .py para posibles modificaciones futuras, además ahora cuando un libro tiene un estado el botón que lo permitía cambiar a ese mismo estado desaparece haciendo la vista más amable para el usuario. Se utilizó la herencia de módulo "mail" para añadir la funcionalidad que nos permite mandar mensajes desde dentro del módulo a clientes, por ejemplo, para notificar que el plazo para devolver su libro se está acabando o a otros usuarios, además permite planificar una actividad, agregar notas, seguir la actividad de un registro... y tener un registro de los cambios modificados en los atributos de un libro con su fecha y el usuario que los realizo.
   El nuevo campo calculado "Remaining days" calcula los días restantes, restando a la fecha del préstamo+30 días la fecha actual y devolviendo los días restantes, cuando un libro supera ese para se le asigna automáticamente el estado "lost". 
   
## _Futuras Mejoras:_   
  Se pretende controlar mejor posibles casos que cubran errores del usuario, como no permitir que la fecha de inicio del prestamo sea posterior a la actual, además de otras mejoras visuales que hagan la interfaz más atractiva.
  
## _Autor_
_Jacobo Fernández Barreiro_  
