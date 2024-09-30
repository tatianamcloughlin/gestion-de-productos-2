import os
import platform

from gestion_de_productos import(
    gestionProductos,
    productosParaAdultos,
    productosParaInfantes,
    Producto)



def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') # Para Linux/Unix/MacOs

def mostrar_menu():
    print("+ + + + + + + + + + +  + + + + + + + + + + ++ + + ")
    print(" + + + + + + + + + + +  + + + + + + + + + + ++ +  ")
    print("========== Menú de Gestión de Productos ==========")
    print("+ + + + + + + + + + +  + + + + + + + + + + ++ + + ")
    print(" + + + + + + + + + + +  + + + + + + + + + + ++ +  ")
    print("                                                  ")    
    print('1. Agregar Producto de  Infantes')
    print('2. Agregar Producto de Adultos')
    print('3. Buscar Producto por Codigo')
    print('4. Actualizar precio de Producto')
    print('5. Actualizar stock de Producto')
    print('6. Eliminarar Producto por codigo')
    print('7. Mostrar Todos los Productos')
    print("                                                  ")
    print('==================================================')


def agregar_producto(gestion, tipo_producto):
    while True:
        try:
            nombre = input('Ingrese nombre del producto: ')
            precio = input('Ingrese precio del producto: ')
            cantidad_en_stock = input('Ingrese cantidad del producto en stock: ')
            codigo_de_productos =input('Ingrese codigo del producto: ')
        

            if tipo_producto == '1':
                rango_etario = input(' 0: bebes \n 1: Kits \n 2: Juniors \n Ingrese la opcion correspondiente al rango etario del producto: ')
                producto = productosParaInfantes( nombre, precio, cantidad_en_stock, codigo_de_productos, rango_etario)
            elif tipo_producto == '2':
                genero = input(' 1: Masculino \n 2: Femenino \n 3: Unisex \n Ingrese la opcion correspondiente al genero del producto: ')
                producto = productosParaAdultos(nombre, precio, cantidad_en_stock, codigo_de_productos , genero)
            else:
                print('Opción inválida')
                return

            producto_creado =gestion.crear_producto(producto)
            if producto_creado:
                print(f'producto {producto.nombre} creado correctamente')

                continuar =input('1:Ingresar otro producto \n2:Volver al menu \n:')
                if continuar == '2':
                    break
            else:
                continuar =input('1:Ingresar otro producto \n2:Volver al menu \n:')
                if continuar == '2':
                    break


        except ValueError as e:
            print(f'Error: {e}')

        except Exception as e:
            print(f'Error inesperado: {e}')


def buscar_producto_por_codigo(gestion,):
    while True:        
        try:
            codigo_de_productos=(input('Ingrese el codigo del producto a buscar: '))
            productos = gestion.leer_producto(codigo_de_productos)
            if productos:
                print(productos)
                continuar =input('1:Ingresar otro codigo \n2:Volver al menu \n:')
                if continuar == '2':
                    break
            else:
                print(f'No existe un producto de codigo {codigo_de_productos} ')
                continuar =input('1:Ingresar otro codigo \n2:Volver al menu \n:')
                if continuar == '2':
                    break

        except ValueError: 
            print ('valor no valido, ingrese nuevamente: ')


def actualizar_precio_producto(gestion):
    while True:
        try:
            codigo= input('Ingrese el codigo del producto para actualizar precio: ')
            precio_nuevo =float(input('Ingrese el precio nuevo: '))
            producto_actualizado = gestion.actualizar_precio(codigo, precio_nuevo)
            if producto_actualizado:
                print (f'precio actualizado correctamente \n{producto_actualizado}')
                continuar =input('1:Ingresar otro codigo \n2:Volver al menu \n:')
                if continuar == '2':
                    break
            else:                
                continuar =input('1:Ingresar otro codigo \n2:Volver al menu \n:')
                if continuar == '2':
                    break

        except ValueError: 
            print ('valor no valido, ingrese nuevamente: ')

    

def actualizar_stock_producto(gestion):
    while True:
        try:
            codigo= input('Ingrese el codigo del producto para actualizar stock: ')
            nuevo_stock =int(input('Ingrese el nuevo stock: '))
            producto_actualizado = gestion.actualizar_stock(codigo, nuevo_stock)
            if producto_actualizado:
                print (f'stock actualizado correctamente \n{producto_actualizado}\n\n')
                continuar =input('1:Ingresar otro codigo \n2:Volver al menu \n:')
                if continuar == '2':
                    break
            else:                
                continuar =input('1:Ingresar otro codigo \n2:Volver al menu \n:')
                if continuar == '2':
                    break

        except ValueError: 
            print ('valor no valido, ingrese nuevamente: ')
 

def eliminar_producto_por_codigo(gestion):
    while True:
        try:
            codigo = input('Ingrese el codigo del producto a eliminar: ')
            gestion.eliminar_producto(codigo)
            continuar =input('1:Ingresar otro codigo \n2:Volver al menu \n:')
            if continuar == '2':
                break

        except  ValueError:
            print ('valor no valido, ingrese nuevamente: ')

def mostrar_todos_los_productos(gestion):
    print('________________LISTA DE PRODUCTOS_______________')
    try:
        productos= gestion.leer_todos_los_productos()
        for producto in productos:
            if isinstance(producto,productosParaInfantes):
                print(f'nombre:{producto.nombre}\nprecio:{producto.precio}\nstock:{producto.cantidad_en_stock}\nrango etario: {producto.rango_etario}\n_____________\n')
            elif isinstance(producto,productosParaAdultos):
                print(f'nombre:{producto.nombre}\nprecio:{producto.precio}\nstock:{producto.cantidad_en_stock}\ngenero: {producto.genero}\n_____________\n')
        input('presione enter para continuar')
    except Exception as e:
            print(f'Error al leer los productos: {e}')



if __name__ == "__main__":
    gestion = gestionProductos()

    while True:
        
        mostrar_menu()
       
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_producto(gestion, opcion) 
        
        elif opcion == '3' :
            buscar_producto_por_codigo(gestion)

        elif opcion == '4' :
            actualizar_precio_producto(gestion)

        elif opcion == '5' :
            actualizar_stock_producto(gestion)

        elif opcion == '6' :
            eliminar_producto_por_codigo(gestion)

        elif opcion == '7' :
            mostrar_todos_los_productos(gestion)

        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')
        
        limpiar_pantalla() 
        
       