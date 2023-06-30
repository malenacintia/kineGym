import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

# Configurar la conexión a la base de datos SQLite
DATABASE = 'Cronograma.db'

def get_db_connection():
    print("Obteniendo conexión...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla 'cursos' si no existe
def create_table():
    print("Creando tabla cursos...") # Para probar que se ejecuta la función
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            codigo INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cupo INTEGER NOT NULL,
            horario TEXT NOT NULL,
            precio REAL NOT NULL
        ) ''')
    conn.commit()
    cursor.close()
    conn.close()


# Verificar si la base de datos existe, si no, crearla y crear la tabla
def create_database():
    print("Creando la BD...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()


# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()



class Curso:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, codigo, descripcion, cupo, horario ,precio):
        self.codigo = codigo           # Código 
        self.descripcion = descripcion # Descripción
        self.cupo = cupo
        self.horario = horario       # Cantidad disponible (stock)
        self.precio = precio           # Precio 


    # Este método permite modificar un curso.
    def modificar(self, nueva_descripcion, nuevo_cupo, nuevo_horario, nuevo_precio):
        self.descripcion = nueva_descripcion  # Modifica la descripción
        self.cupo = nuevo_cupo
        self.horario = nuevo_horario        # Modifica la cupo
        self.precio = nuevo_precio            # Modifica el precio

class Cronograma:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    # Este método permite crear objetos de la clase "curso" y agregarlos al Cronograma.
    def agregar_curso(self, codigo, descripcion, cupo, horario, precio):
        curso_existente = self.consultar_curso(codigo)
        if curso_existente:
            return jsonify({'message': 'Ya existe un curso con ese código.'}), 400
        nuevo_curso = Curso(codigo, descripcion, cupo, horario, precio)
        sql = f'INSERT INTO cursos VALUES ({codigo}, "{descripcion}", {cupo}, {horario}, {precio});'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Curso agregado correctamente.'}), 200

    # Este método permite consultar datos de cursos que están en el Cronograma
    # Devuelve el curso correspondiente al código proporcionado o False si no existe.
    def consultar_curso(self, codigo):
        sql = f'SELECT * FROM cursos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            codigo, descripcion, cupo, horario, precio = row
            return Curso(codigo, descripcion, cupo, horario, precio)
        return None

    # Este método permite modificar datos de cursos que están en el Cronograma
    # Utiliza el método consultar_curso del Cronograma y modificar del curso.
    def modificar_curso(self, codigo, nueva_descripcion, nuevo_cupo, nuevo_horario, nuevo_precio):
        curso = self.consultar_curso(codigo)
        if curso:
            curso.modificar(nueva_descripcion, nuevo_cupo, nuevo_horario, nuevo_precio)
            sql = f'UPDATE cursos SET descripcion = "{nueva_descripcion}", cupo = {nuevo_cupo}, horario = {nuevo_horario}, precio = {nuevo_precio} WHERE codigo = {codigo};' 
            self.cursor.execute(sql)
            self.conexion.commit()
            return jsonify({'message': 'Curso modificado correctamente.'}), 200
        return jsonify({'message': 'Curso no encontrado.'}), 404

    # Este método imprime en la terminal una lista con los datos de los cursos que figuran en el Cronograma.
    def listar_cursos(self):
        self.cursor.execute("SELECT * FROM cursos")
        rows = self.cursor.fetchall()
        cursos = []
        for row in rows:
            codigo, descripcion, cupo, horario, precio = row
            curso = {'codigo': codigo, 'descripcion': descripcion, 'cupo': cupo, 'horario': horario, 'precio': precio}
            cursos.append(curso)
        return jsonify(cursos), 200

    # Este método elimina el curso indicado por codigo de la lista mantenida en el Cronograma.
    def eliminar_curso(self, codigo):
        sql = f'DELETE FROM cursos WHERE codigo = {codigo};' 
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Curso eliminado correctamente.'}), 200
        return jsonify({'message': 'Curso no encontrado.'}), 404


class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.conexion = get_db_connection()  # Conexión a la BD
        self.cursor = self.conexion.cursor()
        self.items = []  # Lista de items en el carrito (variable de clase)

    # Este método permite agregar cursos del Cronograma al carrito.
    '''def agregar(self, codigo, cupo, Cronograma): 
        curso = Cronograma.consultar_curso(codigo)
        if curso is False:
            print("El curso no existe.")
            return False
        if curso.cupo < cupo:
            print(f'No hay vacantes en {curso.descripcion} a la hora solicitada, intente otro día u horario.')
            print(f'El servicio tiene {curso.cupo} lugares libres')
            return False

        #SUMA BIEN UN CUPO A LAS CLASES
        #NO IMPRIME LA CONFIRMACION...
        for item in self.items:
            if item.codigo == codigo:
                item.cupo += cupo
                sql = f'UPDATE cursos SET cupo = cupo - {cupo}  WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True
            print(f'Ha reservado un lugar en {item.descripcion} a las {item.horario} exitosamente.')
            print(f'El servicio tiene ahora {item.cupo} lugares libres')
            
                
        nuevo_item = Curso(codigo, curso.descripcion, cupo, curso.horario, curso.precio)
        self.items.append(nuevo_item)
        sql = f'UPDATE cursos SET cupo = cupo - {cupo}  WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True
        '''
    def agregar(self, codigo, cupo, Cronograma):
        curso = Cronograma.consultar_curso(codigo)
        if curso is None:
            return jsonify({'message': 'El curso no existe.'}), 404
        if curso.cupo < cupo:
            #prints agregados extra(respuesta1 respuesta2 y jsonify)
            respuesta1 = ('No hay vacantes en', (curso.descripcion), 'a la hora solicitada, intente otro día u horario.')
            respuesta2 = ('El servicio tiene', (curso.cupo), 'lugares libres')
            return jsonify({'message': 'Cantidad en stock insuficiente.', 'message': (respuesta1), 'message': (respuesta2)}), 400

        for item in self.items:
            if item.codigo == codigo:
                item.cupo += cupo
                sql = f'UPDATE cursos SET cupo = cupo - {cupo}  WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return jsonify({'message': 'Curso agregado al carrito correctamente.'}), 200

        nuevo_item = Curso(codigo, curso.descripcion, cupo, curso.horario, curso.precio)
        self.items.append(nuevo_item)
        sql = f'UPDATE cursos SET cupo = cupo - {cupo}  WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        #prints agregados en variables y en jsonify
        reserva_ok = ('Ha reservado un lugar en', (item.descripcion), 'a las', (item.horario), 'exitosamente.')
        return jsonify({'message': 'Curso agregado al carrito correctamente.', 'message': (reserva_ok)}), 200

    # Este método quita unidades de un elemento del carrito, o lo elimina.
    def quitar(self, codigo, cupo, Cronograma):
        for item in self.items:
            if item.codigo == codigo:
                if cupo > item.cupo:
                    return jsonify({'message': 'Cantidad a quitar mayor a la cupo en el carrito.'}), 400
                item.cupo -= cupo
                if item.cupo == 0:
                    self.items.remove(item)
                sql = f'UPDATE cursos SET cupo = cupo + {cupo} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return jsonify({'message': 'Curso quitado del carrito correctamente.'}), 200
        return jsonify({'message': 'El curso no se encuentra en el carrito.'}), 404

            
    def mostrar(self):
        cursos_carrito = []
        for item in self.items:
            curso = {'codigo': item.codigo, 'descripcion': item.descripcion, 'cupo': item.cupo, 'horario': item.horario, 'precio': item.precio}
            cursos_carrito.append(curso)
        return jsonify(cursos_carrito), 200


app = Flask(__name__)
CORS(app)

# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()

# Crear una instancia de la clase Cronograma
cronograma = Cronograma()

carrito = Carrito()

# Ruta para obtener los datos de un curso según su código
@app.route('/cursos/<int:codigo>', methods=['GET'])
def obtener_curso(codigo):
    curso = cronograma.consultar_curso(codigo)
    if curso:
        return jsonify({
            'codigo': curso.codigo,
            'descripcion': curso.descripcion,
            'cupo': curso.cupo,
            'horario': curso.horario,
            'precio': curso.precio
        }), 200
    return jsonify({'message': 'curso no encontrado.'}), 404

# Ruta para obtener el index
@app.route('/')
def index():
    return 'API de Cronograma'

# Ruta para obtener la lista de cursos del Cronograma
@app.route('/cursos', methods=['GET'])
def obtener_cursos():
    return cronograma.listar_cursos()

# Ruta para agregar un curso al Cronograma
@app.route('/cursos', methods=['POST'])
def agregar_curso():
    codigo = request.json.get('codigo')
    descripcion = request.json.get('descripcion')
    cupo = request.json.get('cupo')
    horario = request.json.get('horario')
    precio = request.json.get('precio')
    return cronograma.agregar_curso(codigo, descripcion, cupo, horario, precio)

# Ruta para modificar un curso del Cronograma
@app.route('/cursos/<int:codigo>', methods=['PUT'])
def modificar_curso(codigo):
    nueva_descripcion = request.json.get('descripcion')
    nuevo_cupo = request.json.get('cupo')
    nuevo_horario = request.json.get('horario')
    nuevo_precio = request.json.get('precio')
    return cronograma.modificar_curso(codigo, nueva_descripcion, nuevo_cupo, nuevo_horario, nuevo_precio)

# Ruta para eliminar un curso del Cronograma
@app.route('/cursos/<int:codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    return cronograma.eliminar_curso(codigo)

# Ruta para agregar un curso al carrito
@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    codigo = request.json.get('codigo')
    cupo = request.json.get('cupo')
    cronograma = Cronograma()
    return carrito.agregar(codigo, cupo, cronograma)

# Ruta para quitar un curso del carrito
@app.route('/carrito', methods=['DELETE'])
def quitar_carrito():
    codigo = request.json.get('codigo')
    cupo = request.json.get('cupo')
    cronograma = Cronograma()
    return carrito.quitar(codigo, cupo, cronograma)

# Ruta para obtener el contenido del carrito
@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    return carrito.mostrar()


if __name__ == '__main__':
    app.run()


'''
# Agregar cursos al Cronograma
cronograma.agregar_curso(1, "Pilates lunes", 10, "08:00 hs", 19.99)
cronograma.agregar_curso(2, "Preparación al parto lunes", 5, "11:00 hs", 9.99)
cronograma.agregar_curso(3, "Pilates lunes", 10, "16:00 hs", 19.99)
cronograma.agregar_curso(4, "Preparación al parto lunes", 5, "16:00 hs", 9.99)
cronograma.agregar_curso(5, "Pilates lunes", 10, "19:30 hs", 19.99)
cronograma.agregar_curso(6, "Pilates martes", 10, "12:00 hs", 19.99)
cronograma.agregar_curso(7, "Hipopresivos martes", 10, "17:00 hs", 9.99)
cronograma.agregar_curso(8, "Kinesiología miércoles", 1, "11:00 hs", 29.99)
cronograma.agregar_curso(9, "Kinesiología miércoles", 1, "12:00 hs", 29.99)
cronograma.agregar_curso(10, "Pilates miércoles", 10, "15:00 hs", 19.99)
cronograma.agregar_curso(11, "Kinesiología miércoles", 1, "18:00 hs", 29.99)
cronograma.agregar_curso(12, "Kinesiología miércoles", 1, "19:00 hs", 29.99)
cronograma.agregar_curso(13, "Pilates jueves", 10, "12:00 hs", 19.99)
cronograma.agregar_curso(14, "Hipopresivos jueves", 10, "17:00 hs", 9.99)
cronograma.agregar_curso(15, "Pilates jueves", 10, "19:00 hs", 19.99)
cronograma.agregar_curso(16, "Pilates viernes", 10, "8:00 hs", 19.99)
cronograma.agregar_curso(17, "Preparación al parto viernes", 5, "11:00 hs", 9.99)
cronograma.agregar_curso(18, "Hipopresivos viernes", 10, "18:00 hs", 9.99)
cronograma.agregar_curso(19, "Kinesiología sábado", 1, "10:00 hs", 29.99)
cronograma.agregar_curso(20, "Kinesiología sábado", 1, "11:00 hs", 29.99)
cronograma.agregar_curso(21, "Kinesiología sábado", 1, "12:00 hs", 29.99)
cronograma.agregar_curso(22, "Pilates sábado", 10, "10:00 hs", 19.99)

cronograma.listar_cursos()

#cronograma.modificar_curso(1, "Pilates lunes", 10, "08:00 hs", 19.99)
#cronograma.modificar_curso(2, "Preparación al parto lunes", 5, "11:00 hs", 9.99)

#carrito.agregar(13, 1, cronograma)

# Quitar 1 unidad del curso con código 1 al carrito y 1 unidad del curso con código 2 al carrito
carrito.quitar(1, 1, cronograma)
carrito.quitar(2, 1, cronograma)
# Mostrar el contenido del carrito y del Cronograma
carrito.mostrar()
cronograma.listar_cursos()
'''








