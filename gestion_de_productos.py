
# Desafío 1: Sistema de Gestión de Productos
# Objetivo: Desarrollar un sistema para manejar productos en un inventario.

# Requisitos:

# Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
# Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
# Implementar operaciones CRUD para gestionar productos del inventario.
# Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
# Persistir los datos en archivo JSON.

import mysql.connector
from mysql.connector import Error
from decouple import config
import json

class Producto :
    def __init__(self, nombre, precio, cantidad_en_stock, codigo_de_productos):
        self.__nombre = nombre
        self.__precio = self.validar_precio(precio)
        self.__cantidad_en_stock = self.validar_cantidad_en_stock(cantidad_en_stock)
        self.__codigo_de_productos = self.validar_codigo_de_productos(codigo_de_productos)

    @property
    def nombre(self):
         return self.__nombre.capitalize()

    @property
    def precio(self):
         return self.__precio

    @property
    def cantidad_en_stock(self):
         return self.__cantidad_en_stock

    @property
    def codigo_de_productos(self):
         return self.__codigo_de_productos

    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)

    @cantidad_en_stock.setter
    def cantidad_en_stock(self,nuevo_stock):
        self.__cantidad_en_stock= self.validar_cantidad_en_stock(nuevo_stock)
    
    @codigo_de_productos.setter
    def codigo_de_productos(self,codigo_de_productos):
        self.__codigo_de_productos= self.validar_codigo_de_productos(codigo_de_productos)


    def validar_precio(self,precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0 :
                raise Error("El precio o debe ser numéro positivo.")
            return precio_num
        except ValueError: 
            raise ValueError("el precio debe ser un numero .")
        
 
    def validar_codigo_de_productos(self,codigo_de_productos):
        try:
            codigo_de_productos_num = int(codigo_de_productos)
            if len(str(codigo_de_productos)) != 8 :
                raise Error("el codigo ingresado debe tener 8 numeros")
            if codigo_de_productos_num <= 0:
                raise Error("El codigo del producto debe ser un numéro positivo.") 
                
            return codigo_de_productos_num
        except ValueError:
            raise ValueError ("El codigo del producto debe ser un numero.")


    def validar_cantidad_en_stock(self,cantidad_en_stock):
        try:
            cantidad = int(cantidad_en_stock)
            if cantidad <=0:
               raise Error ("cantidad en stock ingresada no valida ") 
            return cantidad 
        except ValueError: 
            raise ValueError ("la cantidad en stock debe ser un numero .") 
 
    
    def to_dict(self):
        return { 
            "nombre": self.nombre,
            "cantidad_en_stock": self.cantidad_en_stock,
            "precio": self.precio,
            "codigo_de_productos": self.codigo_de_productos
        }

    def __str__(self):
        return f"Nombre:{self.nombre} \nPrecio: ${self.precio} \nStock disponible:{self.cantidad_en_stock} "

class productosParaInfantes(Producto):
    def __init__(self, nombre, precio, cantidad_en_stock, codigo_de_productos, rango_etario):
        super().__init__(nombre, precio, cantidad_en_stock, codigo_de_productos)
        self.__rango_etario = self.validar_rango_etario(rango_etario)
   

    @property
    def rango_etario(self):     
        if self.__rango_etario == "0":
            return "Bebes"
        elif self.__rango_etario == "1":
            return "Kids"
        elif self.__rango_etario == "2":
            return "Juniors"
        elif self.__rango_etario == "Bebes":
            return "Bebes"
        elif self.__rango_etario == "Kids":
            return "Kids"
        elif self.__rango_etario == "Juniors":
            return "Juniors"
        
    def validar_rango_etario(self, rango_etario):
        try:
            if rango_etario not in ["0", "1", "2", "Bebes", "Kids", "Juniors"]:
                raise Error("La opción ingresada no corresponde a ningún rango etario existente")
            return rango_etario
        except ValueError:
            raise ValueError("El valor ingresado es incorrecto o no corresponde a ningún rango etario existente")
       

    def to_dict(self):
        data = super().to_dict()
        data["rango_etario"] = self.rango_etario
        return data

    def __str__(self):
        return f"{super().__str__()} \nRango_etario: {self.rango_etario}"  


class productosParaAdultos(Producto):
    def __init__(self, nombre, precio, cantidad_en_stock, codigo_de_productos , genero):
        super().__init__(nombre, precio, cantidad_en_stock, codigo_de_productos)
        self.__genero = self.validar_genero(genero)


    @property
    def genero(self):
        if self.__genero == "1":
            return "Masculino"
        elif self.__genero == "2":
            return "Femenino"
        elif self.__genero == "3":
            return "Unisex"
        elif self.__genero == "Masculino":
            return "Masculino"
        elif self.__genero == "Femenino":
            return "Femenino"
        elif self.__genero == "Unisex":
            return "Unisex"

    
    def validar_genero(self, genero):
        try:
            if genero not in ["1", "2", "3","Masculino","Femenino","Unisex" ]:
                raise Error("La opción ingresada no corresponde a ningún género existente")
            return genero
        except ValueError:
            raise ValueError("La opción ingresada no corresponde a ningún género existente")
       

        
    def to_dict(self):
        data = super().to_dict()
        data["genero"] = self.genero
        return data

    def __str__(self):
        return f"{super().__str__()} \nGenero: {self.genero}" 
    
class gestionProductos:
    def __init__(self):
        self.host = config('db_host')
        self.database=config('db_name')
        self.user=config('db_user')
        self.password=config('db_password')
        self.port=config('db_port')

    def validar_codigo_de_productos(self,codigo_de_productos):
        try:
            codigo_de_productos_num = int(codigo_de_productos)
            if len(str(codigo_de_productos)) != 8 :
                raise Error("el codigo ingresado debe tener 8 numeros")
            return codigo_de_productos_num
        except ValueError:
            raise ValueError ("El codigo del producto debe ser un numero.")

 

    def connect(self):
        try:
            connection= mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port= self.port
            )
            if connection.is_connected():
                return connection

        except Error as e:
            print (f'error al conectar a la base de datos :{e}')
            return None

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def verificar_existencia(self,codigo_de_productos):
        try:
            connection = self.connect()
            codigo = self.validar_codigo_de_productos(codigo_de_productos)
            if connection :
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM productos WHERE codigo_de_productos = %s', (codigo,))
                    return cursor.fetchone()
        except Exception as error:
            print(f'Error : {error}')

    def crear_producto(self, producto):
        try:
            connection= self.connect()
            cursor=connection.cursor()
            if self.verificar_existencia(producto.codigo_de_productos):
                    print(f'ya existe un producto con codigo : {producto.codigo_de_productos}')
                    return    
            query ='''
                INSERT INTO productos (nombre, precio, cantidad_en_stock, codigo_de_productos)
                VALUES (%s,%s,%s,%s)
                ''' 
            values= (producto.nombre, producto.precio, producto.cantidad_en_stock, producto.codigo_de_productos)
                    
            if isinstance(producto,productosParaInfantes ):                                              
                cursor.execute(query, values) 
                query_2 = '''
                    INSERT INTO productosparainfantes (codigo_de_productos, rango_etario)
                    VALUES (%s,%s)
                    '''
                connection.cursor().execute(query_2, (producto.codigo_de_productos, producto.rango_etario))
                    
            elif isinstance(producto,productosParaAdultos ):
                cursor.execute(query, values)
                query_3 = '''
                    INSERT INTO productosparaadultos (codigo_de_productos, genero)
                     VALUES (%s,%s)
                     '''
                cursor.execute(query_3, (producto.codigo_de_productos, producto.genero))
                    
            connection.commit()
            return producto
           
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')
            

        finally:
            if connection.is_connected():
                connection.close()


    def leer_producto(self, codigo_de_productos):
        try:
            connection= self.connect()
            cursor=connection.cursor()
            producto_data = self.verificar_existencia(codigo_de_productos)
            if producto_data:
                cursor.execute('SELECT genero FROM productosParaAdultos WHERE codigo_de_productos = %s',(codigo_de_productos,))
                genero = cursor.fetchone()
 
                if genero:
                    producto_data ['genero']= genero[0]
                    producto = productosParaAdultos(**producto_data)   
                else:
                    cursor.execute('SELECT rango_etario FROM productosParaInfantes WHERE codigo_de_productos = %s',(codigo_de_productos,))
                    rango_etario = cursor.fetchone()

                    if rango_etario:
                        producto_data ['rango_etario']= rango_etario[0]
                        producto = productosParaInfantes(**producto_data)
                    else:
                        producto = Producto(**producto_data)
                
            else:
                producto= None                  

        except Error as e:
            print(f'Error al leer producto: {e}')

        else :
            return producto
        
        finally:
            if connection.is_connected():
                connection.close()
        
    def actualizar_precio(self, codigo_de_productos, nuevo_precio):
        try:
            connection= self.connect()
            cursor = connection.cursor()
            producto_data = self.verificar_existencia(codigo_de_productos)
            if producto_data :   
                if nuevo_precio > 0 :
                    cursor.execute('UPDATE productos SET precio =%s WHERE codigo_de_productos = %s',(nuevo_precio,codigo_de_productos))                  
                    connection.commit()
                    producto_actualizado = self.leer_producto(codigo_de_productos)
                    return producto_actualizado                                      
                else :
                     print (f'el nuevo precio ingresado no es valido')
            else:
                print(f'No existe un producto de codigo {codigo_de_productos} ')
        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

        finally:
            if connection.is_connected():
                connection.close()
                     
    def actualizar_stock(self, codigo_de_productos, nuevo_stock):
        try:
            connection= self.connect()
            cursor = connection.cursor()
            producto_data = self.verificar_existencia(codigo_de_productos)
            if producto_data :   
                if nuevo_stock > 0 :
                    cursor.execute('UPDATE productos SET cantidad_en_stock =%s WHERE codigo_de_productos = %s',(nuevo_stock,codigo_de_productos))                  
                    connection.commit()
                    producto_actualizado = self.leer_producto(codigo_de_productos)
                    return producto_actualizado                                      
                else :
                     print (f'el nuevo stock ingresado no es valido')
            else:
                print(f'No existe un producto de codigo {codigo_de_productos} ')
        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

        finally:
            if connection.is_connected():
                connection.close()

    def eliminar_producto(self, codigo_de_productos):
        try:
            connection= self.connect()
            cursor = connection.cursor()
            producto_data = self.verificar_existencia(codigo_de_productos)
            if producto_data :   
                cursor.execute('DELETE FROM productosparainfantes WHERE codigo_de_productos =%s ',(codigo_de_productos,)) 
                cursor.execute('DELETE FROM productosparaadultos WHERE codigo_de_productos =%s ',(codigo_de_productos,))
                cursor.execute('DELETE FROM productos WHERE codigo_de_productos =%s ',(codigo_de_productos,))                 
                connection.commit()
                print(f'producto eliminado correctamente')
                                     
            else:
                print(f'No existe un producto de codigo {codigo_de_productos} ')
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')

        finally:
            if connection.is_connected():
                connection.close()
    
    def leer_todos_los_productos (self):
        try:
            connection= self.connect()
 
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM productos')
                    productos_data= cursor.fetchall()

                    productos =[]
                    
                    
                    for producto_data in productos_data:
                        codigo= producto_data['codigo_de_productos']
                                                                 
                        cursor.execute('SELECT genero FROM productosparaadultos WHERE codigo_de_productos = %s',(codigo,))
                        genero = cursor.fetchone()

                        if genero:
                            producto_data['genero']=genero['genero']
                            producto= productosParaAdultos(**producto_data)
                            
                        else:
                            cursor.execute('SELECT rango_etario FROM productosparainfantes WHERE codigo_de_productos = %s',(codigo,))
                            rango_etario = cursor.fetchone()
                            producto_data['rango_etario']=rango_etario['rango_etario']
                            producto= productosParaInfantes(**producto_data)
                            
                        
                        productos.append(producto)
                    

        except Exception as e:
            print(f'Error al leer los productos: {e}')

        else:
            return productos

        finally:
            if connection.is_connected():
                connection.close()




                    





                
