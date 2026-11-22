
# ==================================================
# SOFTWARE FJ - SISTEMA DE CLIENTES Y RESERVAS
# UNAD - Programacion - Fase 4
# Luis Diego Ponzon Giraldo
# ==================================================

# Importamos las herramientas que vamos a utilizar.

# ABC permite crear clases abstractas y abstractmethod
# sirve para definir metodos que deben implementar las clases hijas.
from abc import ABC, abstractmethod

# Lo usamos para guardar los errores y eventos del programa.
import logging

# Nos permite trabajar con fechas y horas.
from datetime import datetime


# ==================================================
# 1. CONFIGURACION DEL REGISTRO DE EVENTOS
# ==================================================

# Configuramos el archivo donde quedaran registrados
# los errores y las operaciones importantes del sistema.

logging.basicConfig(
    filename="sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# Dejamos constancia del inicio del programa.
logging.info("Se inicio el sistema Software FJ")


# ==================================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==================================================

# Creamos una excepcion general para los errores
# relacionados con el funcionamiento del sistema.
class ErrorSistema(Exception):
    pass


# Se utiliza cuando los datos de un cliente
# no cumplen con las condiciones solicitadas.
class ErrorCliente(ErrorSistema):
    pass


# Se utiliza cuando hay problemas con un servicio,
# por ejemplo, cuando no esta disponible.
class ErrorServicio(ErrorSistema):
    pass


# Se utiliza cuando una reserva tiene datos incorrectos
# o no se puede realizar la operacion.
class ErrorReserva(ErrorSistema):
    pass


# Se utiliza cuando se intenta realizar una operacion
# que no esta permitida en el sistema.
class OperacionNoPermitida(ErrorSistema):
    pass

# ==================================================
# 3. CLASE ABSTRACTA ENTIDAD
# ==================================================

# Esta clase sera la base para los clientes y servicios.
# Cada entidad tendra un identificador unico dentro de su grupo.
class Entidad(ABC):

    # Al crear una entidad verificamos que su identificador sea valido.
    def __init__(self, identificador):

        # El identificador debe ser un numero entero mayor que cero.
        if type(identificador) is not int or identificador <= 0:
            raise ErrorSistema(
                "El identificador debe ser un numero entero positivo."
            )

        # Guardamos el identificador como atributo protegido.
        self._identificador = identificador

    # Permite consultar el identificador sin modificarlo directamente.
    @property
    def identificador(self):
        return self._identificador

    # Las clases que hereden de Entidad deben implementar este metodo.
    @abstractmethod
    def mostrar_informacion(self):
        pass


# ==================================================
# 4. CLASE CLIENTE
# ==================================================

# La clase Cliente hereda de Entidad para utilizar
# el identificador y los metodos definidos anteriormente.
class Cliente(Entidad):

    # Recibimos los datos necesarios para registrar un cliente.
    def __init__(self, identificador, nombre, documento, correo, telefono):

        # Validamos el identificador usando la clase padre.
        try:
            super().__init__(identificador)
        except ErrorSistema as error:
            raise ErrorCliente(
                f"No se pudo registrar el cliente: {error}"
            ) from error

        # Verificamos que el nombre sea un texto valido.
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ErrorCliente(
                "El nombre debe tener al menos 3 caracteres."
            )

        # No permitimos numeros ni caracteres especiales en el nombre.
        if not all(
            letra.isalpha() or letra.isspace() or letra in "-'"
            for letra in nombre
        ):
            raise ErrorCliente(
                "El nombre solo puede contener letras y espacios."
            )

        # El documento debe contener entre 6 y 12 digitos.
        if type(documento) not in (str, int):
            raise ErrorCliente("El documento debe ser numerico.")

        documento = str(documento).strip()

        if not documento.isdigit() or not 6 <= len(documento) <= 12:
            raise ErrorCliente(
                "El documento debe tener entre 6 y 12 digitos."
            )

        # Revisamos que el correo tenga una estructura basica valida.
        if not isinstance(correo, str):
            raise ErrorCliente("El correo debe ser un texto.")

        correo = correo.strip().lower()

        if (
            correo.count("@") != 1
            or " " in correo
            or not correo.split("@")[0]
            or "." not in correo.split("@")[1]
            or correo.split("@")[1].startswith(".")
            or correo.endswith(".")
        ):
            raise ErrorCliente("El correo electronico no es valido.")

        # El telefono debe tener 10 digitos.
        if type(telefono) not in (str, int):
            raise ErrorCliente("El telefono debe ser numerico.")

        telefono = str(telefono).strip()

        if not telefono.isdigit() or len(telefono) != 10:
            raise ErrorCliente(
                "El telefono debe contener 10 digitos."
            )

        # Guardamos los datos como atributos privados.
        self.__nombre = nombre.strip()
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

    # Estos metodos permiten consultar los datos del cliente.
    # No definimos setters para evitar cambios sin validacion.
    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    # Mostramos los datos principales del cliente registrado.
    def mostrar_informacion(self):
        return (
            f"ID: {self.identificador} | "
            f"Nombre: {self.__nombre} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__correo} | "
            f"Telefono: {self.__telefono}"
        )


# ==================================================
# 5. CLASE ABSTRACTA SERVICIO
# ==================================================

# Esta clase contiene los datos que comparten todos
# los servicios que ofrece la empresa Software FJ.
class Servicio(Entidad):

    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):

        # Utilizamos la clase padre para validar el identificador.
        try:
            super().__init__(identificador)
        except ErrorSistema as error:
            raise ErrorServicio(
                f"Error al crear el servicio: {error}"
            ) from error

        # Revisamos que el servicio tenga un nombre valido.
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ErrorServicio(
                "El nombre del servicio debe tener al menos 3 caracteres."
            )

        # La tarifa debe ser un valor numerico mayor que cero.
        if type(tarifa_hora) not in (int, float):
            raise ErrorServicio("La tarifa debe ser numerica.")

        if not 0 < tarifa_hora < float("inf"):
            raise ErrorServicio(
                "La tarifa debe ser un valor positivo y valido."
            )

        # Verificamos que la disponibilidad sea verdadera o falsa.
        if type(disponible) is not bool:
            raise ErrorServicio(
                "La disponibilidad debe ser True o False."
            )

        # Guardamos los datos del servicio.
        self.__nombre = nombre.strip()
        self.__tarifa_hora = tarifa_hora
        self.__disponible = disponible

    # Permitimos consultar los datos sin cambiarlos directamente.
    @property
    def nombre(self):
        return self.__nombre

    @property
    def tarifa_hora(self):
        return self.__tarifa_hora

    @property
    def disponible(self):
        return self.__disponible

    # Permite cambiar la disponibilidad de un servicio.
    def cambiar_disponibilidad(self, disponible):

        if type(disponible) is not bool:
            raise ErrorServicio(
                "La disponibilidad debe ser True o False."
            )

        self.__disponible = disponible

        logging.info(
            f"Disponibilidad actualizada: {self.__nombre} - {disponible}"
        )

    # Calculamos el total cuando se aplican descuentos o impuestos.
    # Los valores de descuento e impuesto se manejan como porcentajes.
    def _aplicar_ajustes(self, subtotal, descuento=0, impuesto=0):

        if type(subtotal) not in (int, float):
            raise ErrorServicio("El subtotal debe ser numerico.")

        if not 0 < subtotal < float("inf"):
            raise ErrorServicio("El subtotal debe ser mayor que cero.")

        if type(descuento) not in (int, float):
            raise ErrorServicio("El descuento debe ser numerico.")

        if not 0 <= descuento <= 100:
            raise ErrorServicio(
                "El descuento debe estar entre 0 y 100."
            )

        if type(impuesto) not in (int, float):
            raise ErrorServicio("El impuesto debe ser numerico.")

        if not 0 <= impuesto <= 100:
            raise ErrorServicio(
                "El impuesto debe estar entre 0 y 100."
            )

        # Primero aplicamos el descuento y despues el impuesto.
        total = subtotal * (1 - descuento / 100)
        total = total * (1 + impuesto / 100)

        return round(total, 2)

    # Cada tipo de servicio tendra su propia forma de calcular el costo.
    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    # Cada servicio debe validar los datos de su reserva.
    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    # Cada servicio mostrara una descripcion diferente.
    @abstractmethod
    def describir_servicio(self):
        pass

    # Mostramos la informacion general del servicio.
    def mostrar_informacion(self):

        estado = "Disponible" if self.__disponible else "No disponible"

        return (
            f"ID: {self.identificador} | "
            f"Servicio: {self.__nombre} | "
            f"Tarifa por hora: ${self.__tarifa_hora:,.2f} | "
            f"Estado: {estado}"
        )


# ==================================================
# 6. CLASE SALA
# ==================================================

# Esta clase permite gestionar el alquiler de salas.
# Hereda los datos y funciones generales de Servicio.
class Sala(Servicio):

    def __init__(self, identificador, nombre, tarifa_hora,
                 capacidad, disponible=True):

        # Enviamos los datos generales a la clase Servicio.
        super().__init__(
            identificador, nombre, tarifa_hora, disponible
        )

        # Verificamos que la capacidad sea un numero valido.
        if type(capacidad) is not int or not 1 <= capacidad <= 100:
            raise ErrorServicio(
                "La capacidad de la sala debe estar entre 1 y 100 personas."
            )

        # Guardamos la cantidad maxima de personas.
        self.__capacidad = capacidad

    # Permite consultar la capacidad de la sala.
    @property
    def capacidad(self):
        return self.__capacidad

    # Revisamos que la sala pueda reservarse.
    def validar_parametros(self, duracion):

        # Solo aceptamos duraciones numericas.
        if type(duracion) not in (int, float):
            raise ErrorReserva(
                "La duracion de la reserva debe ser numerica."
            )

        # La sala puede reservarse entre 1 y 12 horas.
        if not 1 <= duracion <= 12:
            raise ErrorReserva(
                "La sala se puede reservar entre 1 y 12 horas."
            )

        # No permitimos reservar una sala que no este disponible.
        if not self.disponible:
            raise ErrorServicio(
                "La sala seleccionada no esta disponible."
            )

        return True

    # Calculamos el costo segun las horas solicitadas.
    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        # Antes de calcular verificamos los datos de la reserva.
        self.validar_parametros(duracion)

        # Multiplicamos la tarifa por las horas de uso.
        subtotal = self.tarifa_hora * duracion

        # Aplicamos los descuentos e impuestos si corresponde.
        total = self._aplicar_ajustes(
            subtotal, descuento, impuesto
        )

        return total

    # Mostramos las caracteristicas de la sala.
    def describir_servicio(self):

        return (
            f"Sala: {self.nombre} | "
            f"Capacidad: {self.__capacidad} personas | "
            f"Tarifa por hora: ${self.tarifa_hora:,.2f}"
        )


# ==================================================
# 7. CLASE EQUIPO
# ==================================================

# Esta clase permite realizar el alquiler de equipos.
# Utiliza los datos generales que ya tiene Servicio.
class Equipo(Servicio):

    def __init__(self, identificador, nombre, tarifa_hora,
                 tipo_equipo, cantidad=1, disponible=True):

        # Primero validamos los datos generales del servicio.
        super().__init__(
            identificador, nombre, tarifa_hora, disponible
        )

        # Verificamos que se indique el tipo de equipo.
        if not isinstance(tipo_equipo, str) or len(tipo_equipo.strip()) < 3:
            raise ErrorServicio(
                "Debe indicar un tipo de equipo valido."
            )

        # La cantidad debe ser un numero entero entre 1 y 20.
        if type(cantidad) is not int or not 1 <= cantidad <= 20:
            raise ErrorServicio(
                "La cantidad de equipos debe estar entre 1 y 20."
            )

        # Guardamos la informacion propia del equipo.
        self.__tipo_equipo = tipo_equipo.strip()
        self.__cantidad = cantidad

    # Consultamos el tipo de equipo registrado.
    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    # Consultamos la cantidad de equipos del alquiler.
    @property
    def cantidad(self):
        return self.__cantidad

    # Comprobamos que el alquiler cumpla las condiciones.
    def validar_parametros(self, duracion):

        # La duracion debe ser un numero.
        if type(duracion) not in (int, float):
            raise ErrorReserva(
                "La duracion del alquiler debe ser numerica."
            )

        # Permitimos alquileres entre 1 y 48 horas.
        if not 1 <= duracion <= 48:
            raise ErrorReserva(
                "El alquiler debe durar entre 1 y 48 horas."
            )

        # Verificamos si el equipo se encuentra disponible.
        if not self.disponible:
            raise ErrorServicio(
                "El equipo solicitado no esta disponible."
            )

        return True

    # Calculamos el valor del alquiler.
    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        # Revisamos los datos antes de realizar el calculo.
        self.validar_parametros(duracion)

        # Multiplicamos la tarifa por las horas y la cantidad.
        subtotal = self.tarifa_hora * duracion * self.__cantidad

        # Aplicamos los descuentos e impuestos correspondientes.
        total = self._aplicar_ajustes(
            subtotal, descuento, impuesto
        )

        return total

    # Mostramos los detalles del equipo que se alquila.
    def describir_servicio(self):

        return (
            f"Equipo: {self.nombre} | "
            f"Tipo: {self.__tipo_equipo} | "
            f"Cantidad: {self.__cantidad} | "
            f"Tarifa por hora y unidad: ${self.tarifa_hora:,.2f}"
        )

# ==================================================
# 8. CLASE ASESORIA
# ==================================================

# Esta clase permite contratar asesorias especializadas.
# Hereda las caracteristicas generales de Servicio.
class Asesoria(Servicio):

    def __init__(self, identificador, nombre, tarifa_hora,
                 especialidad, profesional, modalidad="virtual",
                 disponible=True):

        # Validamos los datos generales del servicio.
        super().__init__(
            identificador, nombre, tarifa_hora, disponible
        )

        # Comprobamos que se indique el area de la asesoria.
        if not isinstance(especialidad, str) or len(especialidad.strip()) < 3:
            raise ErrorServicio(
                "Debe indicar una especialidad valida."
            )

        # Verificamos que el profesional tenga un nombre valido.
        if not isinstance(profesional, str) or len(profesional.strip()) < 3:
            raise ErrorServicio(
                "El nombre del profesional debe tener al menos 3 caracteres."
            )

        # Solo manejamos asesorias virtuales o presenciales.
        if not isinstance(modalidad, str):
            raise ErrorServicio(
                "La modalidad debe ser virtual o presencial."
            )

        modalidad = modalidad.strip().lower()

        if modalidad not in ("virtual", "presencial"):
            raise ErrorServicio(
                "La modalidad debe ser virtual o presencial."
            )

        # Guardamos los datos propios de la asesoria.
        self.__especialidad = especialidad.strip()
        self.__profesional = profesional.strip()
        self.__modalidad = modalidad

    # Permite consultar la especialidad de la asesoria.
    @property
    def especialidad(self):
        return self.__especialidad

    # Permite consultar el profesional encargado.
    @property
    def profesional(self):
        return self.__profesional

    # Permite conocer si la asesoria es virtual o presencial.
    @property
    def modalidad(self):
        return self.__modalidad

    # Validamos las condiciones para realizar la asesoria.
    def validar_parametros(self, duracion):

        # La duracion debe ser un valor numerico.
        if type(duracion) not in (int, float):
            raise ErrorReserva(
                "La duracion de la asesoria debe ser numerica."
            )

        # Las asesorias pueden durar entre 1 y 8 horas.
        if not 1 <= duracion <= 8:
            raise ErrorReserva(
                "La asesoria debe durar entre 1 y 8 horas."
            )

        # No se permiten reservas si el servicio no esta disponible.
        if not self.disponible:
            raise ErrorServicio(
                "La asesoria seleccionada no esta disponible."
            )

        return True

    # Calculamos el valor de la asesoria segun su duracion.
    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        # Primero verificamos los datos de la asesoria.
        self.validar_parametros(duracion)

        # Calculamos el valor de las horas contratadas.
        subtotal = self.tarifa_hora * duracion

        # Aplicamos los descuentos e impuestos si corresponde.
        total = self._aplicar_ajustes(
            subtotal, descuento, impuesto
        )

        return total

    # Mostramos la informacion de la asesoria.
    def describir_servicio(self):

        return (
            f"Asesoria: {self.nombre} | "
            f"Especialidad: {self.__especialidad} | "
            f"Profesional: {self.__profesional} | "
            f"Modalidad: {self.__modalidad} | "
            f"Tarifa por hora: ${self.tarifa_hora:,.2f}"
        )


# ==================================================
# 9. CLASE RESERVA
# ==================================================

# Esta clase relaciona un cliente con el servicio
# que desea contratar y permite gestionar su reserva.
class Reserva(Entidad):

    def __init__(self, identificador, cliente, servicio,
                 duracion, descuento=0, impuesto=0):

        # Validamos el identificador de la reserva.
        try:
            super().__init__(identificador)
        except ErrorSistema as error:
            raise ErrorReserva(
                f"Error al crear la reserva: {error}"
            ) from error

        # Comprobamos que el cliente este registrado como objeto Cliente.
        if not isinstance(cliente, Cliente):
            raise ErrorReserva(
                "Debe seleccionar un cliente valido."
            )

        # El servicio debe pertenecer a las clases que hemos creado.
        if not isinstance(servicio, Servicio):
            raise ErrorReserva(
                "Debe seleccionar un servicio valido."
            )

        # Revisamos la duracion y disponibilidad del servicio.
        servicio.validar_parametros(duracion)

        # Guardamos los datos de la reserva.
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__descuento = descuento
        self.__impuesto = impuesto

        # Todas las reservas comienzan en estado pendiente.
        self.__estado = "pendiente"
        self.__total = None

        logging.info(
            f"Reserva {self.identificador} creada para "
            f"el cliente {cliente.identificador}"
        )

    # Permite consultar el estado actual de la reserva.
    @property
    def estado(self):
        return self.__estado

    # Permite consultar el cliente de la reserva.
    @property
    def cliente(self):
        return self.__cliente

    # Permite consultar el servicio seleccionado.
    @property
    def servicio(self):
        return self.__servicio

    # Permite consultar el valor calculado.
    @property
    def total(self):
        return self.__total

    # Confirmamos la reserva si cumple las condiciones.
    def confirmar(self):

        # Solo se pueden confirmar reservas pendientes.
        if self.__estado != "pendiente":
            raise OperacionNoPermitida(
                "Solo se pueden confirmar reservas pendientes."
            )

        # Volvemos a verificar que el servicio este disponible.
        self.__servicio.validar_parametros(self.__duracion)

        # Al confirmar, el servicio deja de estar disponible.
        self.__servicio.cambiar_disponibilidad(False)
        self.__estado = "confirmada"

        logging.info(
            f"Reserva {self.identificador} confirmada"
        )

        return True

    # Cancelamos una reserva y liberamos el servicio.
    def cancelar(self):

        # No permitimos cancelar dos veces la misma reserva.
        if self.__estado == "cancelada":
            raise OperacionNoPermitida(
                "Esta reserva ya fue cancelada."
            )

        # Si estaba confirmada, el servicio vuelve a estar disponible.
        if self.__estado == "confirmada":
            self.__servicio.cambiar_disponibilidad(True)

        self.__estado = "cancelada"

        logging.info(
            f"Reserva {self.identificador} cancelada"
        )

        return True

    # Procesamos la reserva y calculamos el valor final.
    def procesar(self):

        if self.__estado != "pendiente":
            raise OperacionNoPermitida(
                "La reserva no esta pendiente de procesamiento."
            )

        try:
            # Calculamos el costo utilizando el metodo del servicio.
            total = self.__servicio.calcular_costo(
                self.__duracion,
                self.__descuento,
                self.__impuesto
            )

            # Si el calculo es correcto, confirmamos la reserva.
            self.confirmar()

        except ErrorSistema as error:

            # Registramos el error sin perder su informacion.
            logging.error(
                f"Error al procesar reserva {self.identificador}: {error}"
            )

            # Enviamos el error para que el sistema principal lo maneje.
            raise

        except (TypeError, ValueError, OverflowError) as error:

            # Controlamos errores que puedan aparecer en los calculos.
            logging.exception(
                f"Error inesperado en reserva {self.identificador}"
            )

            raise ErrorReserva(
                "No se pudo calcular el costo de la reserva."
            ) from error

        else:
            # Si no hubo errores, guardamos el total calculado.
            self.__total = total

            logging.info(
                f"Reserva {self.identificador} procesada correctamente"
            )

            return total

        finally:
            # Este bloque se ejecuta aunque ocurra algun error.
            logging.info(
                f"Finalizo el intento de procesar reserva "
                f"{self.identificador}"
            )

    # Mostramos un resumen con los datos de la reserva.
    def mostrar_informacion(self):

        if self.__total is None:
            valor = "Pendiente de calcular"
        else:
            valor = f"${self.__total:,.2f}"

        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duracion: {self.__duracion} horas | "
            f"Estado: {self.__estado} | "
            f"Total: {valor}"
        )

    
# ==================================================
# 10. GESTION DE CLIENTES, SERVICIOS Y RESERVAS
# ==================================================

# Esta clase se encarga de administrar los registros
# de clientes, servicios y reservas de Software FJ.
class SistemaSoftwareFJ:

    def __init__(self):

        # Usamos listas para guardar la informacion
        # mientras el programa se encuentra funcionando.
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    # Registramos un cliente despues de validar sus datos.
    def registrar_cliente(self, identificador, nombre,
                          documento, correo, telefono):

        nuevo_cliente = Cliente(
            identificador, nombre, documento, correo, telefono
        )

        # Evitamos registrar dos clientes con el mismo ID.
        for cliente in self.__clientes:
            if cliente.identificador == nuevo_cliente.identificador:
                raise ErrorCliente(
                    "Ya existe un cliente con este identificador."
                )

            # Tampoco permitimos documentos repetidos.
            if cliente.documento == nuevo_cliente.documento:
                raise ErrorCliente(
                    "Ya existe un cliente con este documento."
                )

        # Si no hay duplicados, guardamos el cliente.
        self.__clientes.append(nuevo_cliente)

        logging.info(
            f"Cliente registrado: {nuevo_cliente.nombre}"
        )

        return nuevo_cliente

    # Agregamos los servicios que ofrece la empresa.
    def registrar_servicio(self, servicio):

        # Solo aceptamos objetos que pertenezcan a Servicio.
        if not isinstance(servicio, Servicio):
            raise ErrorServicio(
                "El objeto ingresado no es un servicio valido."
            )

        # Revisamos que el identificador no este repetido.
        for registrado in self.__servicios:
            if registrado.identificador == servicio.identificador:
                raise ErrorServicio(
                    "Ya existe un servicio con este identificador."
                )

        self.__servicios.append(servicio)

        logging.info(
            f"Servicio registrado: {servicio.nombre}"
        )

        return servicio

    # Buscamos un cliente utilizando su identificador.
    def buscar_cliente(self, identificador):

        for cliente in self.__clientes:
            if cliente.identificador == identificador:
                return cliente

        raise ErrorCliente(
            "No se encontro un cliente con ese identificador."
        )

    # Buscamos un servicio dentro de los registrados.
    def buscar_servicio(self, identificador):

        for servicio in self.__servicios:
            if servicio.identificador == identificador:
                return servicio

        raise ErrorServicio(
            "No se encontro el servicio solicitado."
        )

    # Buscamos una reserva por su identificador.
    def buscar_reserva(self, identificador):

        for reserva in self.__reservas:
            if reserva.identificador == identificador:
                return reserva

        raise ErrorReserva(
            "No se encontro una reserva con ese identificador."
        )

    # Creamos una reserva relacionando cliente y servicio.
    def crear_reserva(self, identificador, id_cliente,
                      id_servicio, duracion, descuento=0,
                      impuesto=0):

        # Primero revisamos si el numero de reserva ya existe.
        for reserva in self.__reservas:
            if reserva.identificador == identificador:
                raise ErrorReserva(
                    "Ya existe una reserva con este identificador."
                )

        # Buscamos el cliente y el servicio seleccionados.
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)

        # Evitamos tener dos reservas activas del mismo servicio.
        for reserva in self.__reservas:
            if (
                reserva.servicio is servicio
                and reserva.estado in ("pendiente", "confirmada")
            ):
                raise ErrorReserva(
                    "El servicio ya tiene una reserva activa."
                )

        # Creamos la reserva usando la clase correspondiente.
        nueva_reserva = Reserva(
            identificador, cliente, servicio,
            duracion, descuento, impuesto
        )

        # Guardamos la nueva reserva en nuestra lista.
        self.__reservas.append(nueva_reserva)

        logging.info(
            f"Reserva {identificador} registrada en el sistema"
        )

        return nueva_reserva

    # Procesamos una reserva que ya fue creada.
    def procesar_reserva(self, identificador):

        reserva = self.buscar_reserva(identificador)

        # La clase Reserva se encarga de calcular y confirmar.
        return reserva.procesar()

    # Cancelamos una reserva registrada en el sistema.
    def cancelar_reserva(self, identificador):

        reserva = self.buscar_reserva(identificador)

        return reserva.cancelar()

    # Devolvemos los clientes registrados.
    def listar_clientes(self):
        return self.__clientes.copy()

    # Devolvemos los servicios disponibles en el sistema.
    def listar_servicios(self):
        return self.__servicios.copy()

    # Devolvemos las reservas que se han creado.
    def listar_reservas(self):
        return self.__reservas.copy()


# ==================================================
# 11. MANEJO CENTRALIZADO DE ERRORES
# ==================================================

# Esta funcion nos permite ejecutar operaciones del sistema
# y controlar los errores sin cerrar el programa.
def ejecutar_operacion(descripcion, operacion, *args, **kwargs):

    try:
        # Ejecutamos la funcion con los datos recibidos.
        resultado = operacion(*args, **kwargs)

    except ErrorSistema as error:

        # Capturamos los errores que definimos en nuestras clases.
        print(f"\nError: {error}")

        # Guardamos el mensaje y los detalles del error.
        logging.exception(
            f"Error al realizar la operacion: {descripcion}"
        )

        return False, None

    except (ValueError, TypeError, OverflowError) as error:

        # Controlamos errores de datos y calculos.
        print(f"\nError en los datos ingresados: {error}")

        logging.exception(
            f"Error de datos en la operacion: {descripcion}"
        )

        return False, None

    except Exception as error:

        # Registramos otros errores que no se hayan previsto.
        print(f"\nOcurrio un error inesperado: {error}")

        logging.exception(
            f"Error inesperado en: {descripcion}"
        )

        return False, None

    else:
        # Si todo sale bien, registramos la operacion.
        logging.info(
            f"Operacion realizada correctamente: {descripcion}"
        )

        print(f"\nOperacion exitosa: {descripcion}")

        return True, resultado

    
# ==================================================
# 12. SIMULACION DE OPERACIONES
# ==================================================

# En esta seccion probamos diferentes situaciones
# para comprobar que el sistema funciona correctamente.
def simular_operaciones():

    print("\n" + "=" * 55)
    print("SOFTWARE FJ - PRUEBAS DEL SISTEMA")
    print("=" * 55)

    # Creamos una instancia nueva para realizar las pruebas.
    sistema = SistemaSoftwareFJ()

    total_pruebas = 0
    pruebas_correctas = 0

    logging.info("Inicio de las pruebas del sistema")

    # Esta funcion nos ayuda a revisar el resultado de cada prueba.
    # Algunas operaciones deben fallar porque estamos probando errores.
    def probar(descripcion, debe_funcionar, funcion,
               *args, total_esperado=None, **kwargs):

        nonlocal total_pruebas, pruebas_correctas

        total_pruebas += 1

        print(f"\nPRUEBA {total_pruebas}: {descripcion}")

        # Ejecutamos la operacion usando el control de errores.
        exito, resultado = ejecutar_operacion(
            descripcion, funcion, *args, **kwargs
        )

        # Comprobamos si el resultado fue el esperado.
        correcta = exito == debe_funcionar

        # Cuando hay un costo esperado, tambien lo verificamos.
        if total_esperado is not None and exito:
            if resultado != total_esperado:
                correcta = False

            print(f"Total obtenido: ${resultado:,.2f}")
            print(f"Total esperado: ${total_esperado:,.2f}")

        if correcta:
            pruebas_correctas += 1
            print("Resultado de la prueba: CORRECTO")
        else:
            print("Resultado de la prueba: REVISAR")

            logging.error(
                f"La prueba {total_pruebas} no dio "
                f"el resultado esperado: {descripcion}"
            )

    # Creamos los servicios y los registramos en el sistema.
    # Asi podemos controlar errores tanto al crear como al guardar.
    def crear_servicio(tipo_servicio, *args, **kwargs):

        servicio = tipo_servicio(*args, **kwargs)

        return sistema.registrar_servicio(servicio)

    # --------------------------------------------------
    # PRUEBAS DE CLIENTES
    # --------------------------------------------------

    probar(
        "Registrar un cliente valido",
        True,
        sistema.registrar_cliente,
        1, "Carlos Perez", "1234567890",
        "carlos@gmail.com", "3001234567"
    )

    probar(
        "Rechazar un cliente con nombre muy corto",
        False,
        sistema.registrar_cliente,
        2, "Jo", "9876543210",
        "jo@gmail.com", "3009876543"
    )

    probar(
        "Registrar un segundo cliente",
        True,
        sistema.registrar_cliente,
        2, "Ana Martinez", "9876543210",
        "ana@gmail.com", "3012345678"
    )

    probar(
        "Rechazar un documento repetido",
        False,
        sistema.registrar_cliente,
        3, "Pedro Gomez", "1234567890",
        "pedro@gmail.com", "3023456789"
    )

    # --------------------------------------------------
    # PRUEBAS DE SERVICIOS
    # --------------------------------------------------

    probar(
        "Rechazar una sala con capacidad incorrecta",
        False,
        crear_servicio,
        Sala, 104, "Sala pequena", 50000, 0
    )

    probar(
        "Registrar una sala correctamente",
        True,
        crear_servicio,
        Sala, 101, "Sala principal", 50000, 10
    )

    probar(
        "Registrar equipos para alquiler",
        True,
        crear_servicio,
        Equipo, 102, "Computadores", 20000,
        "Portatil", 2
    )

    probar(
        "Registrar una asesoria especializada",
        True,
        crear_servicio,
        Asesoria, 103, "Seguridad digital", 80000,
        "Ciberseguridad", "Ana Torres", "virtual"
    )

    probar(
        "Rechazar un objeto que no es un servicio",
        False,
        sistema.registrar_servicio,
        "Servicio incorrecto"
    )

    # --------------------------------------------------
    # PRUEBAS DE RESERVAS
    # --------------------------------------------------

    probar(
        "Rechazar una reserva de cliente inexistente",
        False,
        sistema.crear_reserva,
        1001, 99, 101, 3
    )

    probar(
        "Rechazar una reserva con duracion incorrecta",
        False,
        sistema.crear_reserva,
        1001, 1, 101, 20
    )

    probar(
        "Crear una reserva de sala",
        True,
        sistema.crear_reserva,
        1001, 1, 101, 3
    )

    probar(
        "Procesar la reserva de sala",
        True,
        sistema.procesar_reserva,
        1001,
        total_esperado=150000
    )

    probar(
        "Rechazar otra reserva del servicio ocupado",
        False,
        sistema.crear_reserva,
        1002, 2, 101, 2
    )

    probar(
        "Cancelar una reserva confirmada",
        True,
        sistema.cancelar_reserva,
        1001
    )

    # --------------------------------------------------
    # PRUEBAS DE DESCUENTOS E IMPUESTOS
    # --------------------------------------------------

    probar(
        "Crear reserva con descuento incorrecto",
        True,
        sistema.crear_reserva,
        1003, 1, 101, 2, 120, 0
    )

    # La reserva se crea, pero debe fallar al calcular
    # porque el descuento supera el 100 por ciento.
    probar(
        "Rechazar calculo con descuento del 120%",
        False,
        sistema.procesar_reserva,
        1003
    )

    probar(
        "Cancelar reserva con calculo incorrecto",
        True,
        sistema.cancelar_reserva,
        1003
    )

    probar(
        "Crear reserva con descuento e impuesto",
        True,
        sistema.crear_reserva,
        1004, 1, 101, 2, 10, 19
    )

    probar(
        "Procesar reserva con descuento e impuesto",
        True,
        sistema.procesar_reserva,
        1004,
        total_esperado=107100
    )

    # --------------------------------------------------
    # PRUEBAS DE EQUIPOS Y ASESORIAS
    # --------------------------------------------------

    probar(
        "Crear reserva para alquiler de equipos",
        True,
        sistema.crear_reserva,
        1005, 2, 102, 4
    )

    probar(
        "Procesar alquiler de dos equipos",
        True,
        sistema.procesar_reserva,
        1005,
        total_esperado=160000
    )

    probar(
        "Crear reserva de asesoria",
        True,
        sistema.crear_reserva,
        1006, 2, 103, 3
    )

    probar(
        "Procesar reserva de asesoria",
        True,
        sistema.procesar_reserva,
        1006,
        total_esperado=240000
    )

    probar(
        "Cancelar reserva de asesoria",
        True,
        sistema.cancelar_reserva,
        1006
    )

    probar(
        "Rechazar cancelacion repetida",
        False,
        sistema.cancelar_reserva,
        1006
    )

    # --------------------------------------------------
    # RESUMEN DE LAS PRUEBAS
    # --------------------------------------------------

    print("\n" + "=" * 55)
    print("RESUMEN DE LAS PRUEBAS")
    print("=" * 55)

    print(f"Pruebas realizadas: {total_pruebas}")
    print(f"Pruebas correctas: {pruebas_correctas}")
    print(f"Pruebas por revisar: {total_pruebas - pruebas_correctas}")

    # Guardamos el resultado general de la simulacion.
    logging.info(
        f"Fin de pruebas. Total: {total_pruebas}, "
        f"Correctas: {pruebas_correctas}"
    )

    if pruebas_correctas == total_pruebas:
        print("\nTodas las pruebas dieron el resultado esperado.")
    else:
        print("\nSe encontraron pruebas que necesitan revision.")

    return pruebas_correctas == total_pruebas


# ==================================================
# 13. MENU PRINCIPAL DEL SISTEMA
# ==================================================

# Estas funciones facilitan el ingreso de numeros
# y permiten detectar cuando se escribe un dato incorrecto.
def leer_entero(mensaje):
    return int(input(mensaje).strip())


def leer_numero(mensaje):
    return float(input(mensaje).strip().replace(",", "."))


# Creamos y registramos un servicio segun su tipo.
def agregar_servicio(sistema, tipo_servicio, *datos):

    servicio = tipo_servicio(*datos)

    return sistema.registrar_servicio(servicio)


# Mostramos los registros de una lista.
def mostrar_registros(registros, titulo):

    print(f"\n--- {titulo} ---")

    if not registros:
        print("No hay registros para mostrar.")
        return

    for registro in registros:
        print(registro.mostrar_informacion())


# Esta funcion contiene las opciones del programa.
def menu_principal():

    # Creamos el sistema que utilizara el usuario.
    sistema = SistemaSoftwareFJ()

    logging.info("Se abrio el menu principal")

    while True:

        print("\n" + "=" * 50)
        print("     SOFTWARE FJ - SISTEMA DE RESERVAS")
        print("=" * 50)

        print("1. Registrar cliente")
        print("2. Registrar servicio")
        print("3. Consultar clientes")
        print("4. Consultar servicios")
        print("5. Crear reserva")
        print("6. Procesar reserva")
        print("7. Cancelar reserva")
        print("8. Consultar reservas")
        print("9. Ejecutar pruebas del sistema")
        print("0. Salir")
        print("-" * 50)

        try:
            opcion = input("Seleccione una opcion: ").strip()

            # Registro de clientes.
            if opcion == "1":

                print("\nREGISTRO DE CLIENTE")

                identificador = leer_entero("ID del cliente: ")
                nombre = input("Nombre completo: ")
                documento = input("Documento: ")
                correo = input("Correo electronico: ")
                telefono = input("Telefono: ")

                ejecutar_operacion(
                    "Registrar cliente",
                    sistema.registrar_cliente,
                    identificador, nombre, documento,
                    correo, telefono
                )

            # Registro de servicios.
            elif opcion == "2":

                print("\nTIPOS DE SERVICIO")
                print("1. Sala")
                print("2. Equipo")
                print("3. Asesoria")

                tipo = input("Seleccione el tipo: ").strip()

                if tipo not in ("1", "2", "3"):
                    print("El tipo de servicio no es valido.")
                    continue

                identificador = leer_entero("ID del servicio: ")
                nombre = input("Nombre del servicio: ")
                tarifa = leer_numero("Tarifa por hora: ")

                if tipo == "1":

                    capacidad = leer_entero(
                        "Capacidad de la sala: "
                    )

                    ejecutar_operacion(
                        "Registrar sala",
                        agregar_servicio,
                        sistema, Sala,
                        identificador, nombre,
                        tarifa, capacidad
                    )

                elif tipo == "2":

                    tipo_equipo = input("Tipo de equipo: ")
                    cantidad = leer_entero(
                        "Cantidad de equipos: "
                    )

                    ejecutar_operacion(
                        "Registrar equipo",
                        agregar_servicio,
                        sistema, Equipo,
                        identificador, nombre,
                        tarifa, tipo_equipo, cantidad
                    )

                elif tipo == "3":

                    especialidad = input("Especialidad: ")
                    profesional = input("Profesional encargado: ")
                    modalidad = input(
                        "Modalidad (virtual/presencial): "
                    )

                    ejecutar_operacion(
                        "Registrar asesoria",
                        agregar_servicio,
                        sistema, Asesoria,
                        identificador, nombre,
                        tarifa, especialidad,
                        profesional, modalidad
                    )

            # Consulta de clientes.
            elif opcion == "3":

                mostrar_registros(
                    sistema.listar_clientes(),
                    "CLIENTES REGISTRADOS"
                )

            # Consulta de servicios.
            elif opcion == "4":

                mostrar_registros(
                    sistema.listar_servicios(),
                    "SERVICIOS REGISTRADOS"
                )

            # Creacion de reservas.
            elif opcion == "5":

                print("\nCREAR RESERVA")

                identificador = leer_entero("ID de la reserva: ")
                id_cliente = leer_entero("ID del cliente: ")
                id_servicio = leer_entero("ID del servicio: ")
                duracion = leer_numero("Duracion en horas: ")

                descuento = leer_numero(
                    "Descuento en porcentaje (0 si no aplica): "
                )

                impuesto = leer_numero(
                    "Impuesto en porcentaje (0 si no aplica): "
                )

                ejecutar_operacion(
                    "Crear reserva",
                    sistema.crear_reserva,
                    identificador, id_cliente,
                    id_servicio, duracion,
                    descuento, impuesto
                )

            # Procesamiento y confirmacion de reservas.
            elif opcion == "6":

                identificador = leer_entero(
                    "ID de la reserva a procesar: "
                )

                exito, total = ejecutar_operacion(
                    "Procesar reserva",
                    sistema.procesar_reserva,
                    identificador
                )

                if exito:
                    print(f"Valor total: ${total:,.2f}")
                    print("La reserva quedo confirmada.")

            # Cancelacion de reservas.
            elif opcion == "7":

                identificador = leer_entero(
                    "ID de la reserva a cancelar: "
                )

                ejecutar_operacion(
                    "Cancelar reserva",
                    sistema.cancelar_reserva,
                    identificador
                )

            # Consulta de reservas.
            elif opcion == "8":

                mostrar_registros(
                    sistema.listar_reservas(),
                    "RESERVAS REGISTRADAS"
                )

            # Ejecutamos las pruebas que ya programamos.
            elif opcion == "9":

                print("\nINICIANDO PRUEBAS DEL SISTEMA")

                # Las pruebas usan otro sistema para no
                # modificar los registros del menu.
                simular_operaciones()

            # Cerramos el programa.
            elif opcion == "0":

                print("\nGracias por utilizar Software FJ.")
                logging.info("El usuario cerro el programa")
                break

            else:
                print("\nOpcion incorrecta. Intente nuevamente.")

        except (ValueError, OverflowError) as error:

            # Controlamos errores al ingresar datos numericos.
            print("\nDebe ingresar un numero valido.")

            logging.error(
                f"Error al ingresar datos en el menu: {error}"
            )

        except (KeyboardInterrupt, EOFError):

            # Permitimos salir si se interrumpe la terminal.
            print("\nSe interrumpio la ejecucion del programa.")
            logging.info("El programa fue interrumpido")
            break

        except Exception as error:

            # Registramos cualquier otro problema que aparezca.
            print(f"\nOcurrio un error: {error}")

            logging.exception(
                "Error inesperado en el menu principal"
            )


# Iniciamos el programa cuando ejecutamos este archivo.
if __name__ == "__main__":
    menu_principal()
