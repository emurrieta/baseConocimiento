#
#  Posgrado en Ingenieria y en Ciencias de la Computacion
#  Inteligencia Artificial
#  Proyecto sobre representacion del conocimiento
#
#  Equipo:
#       Montejano Lopez Donovan Jesus
#       Murrieta Leon Juan Eduardo
#
#  Se implementan los predicados:
#       class_extension
#	property_extension
#	relation_extension
#	classes_of_individual
#

import re

def load_knowledge_base(file_path):
    knowledge_base = {}
    single_line_KB=""


    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines: 
        single_line_KB+=line.rstrip()

    single_line_KB=single_line_KB.replace(" ","")
    kb_line = re.search('^\[(.*)\]$', single_line_KB).group(1)
    kb_line=kb_line.replace(",class",", class")
    kb_line+=", "

    clases = re.findall('class\(.*?[^{class}].*?\), ',kb_line)

    for clase in clases:
            clase = clase.rstrip(', ').rstrip(', ')
            campos = re.search('\((.+),(.+),(\[.*\]),(\[.*\]),(\[(\[.*\])*\])\)',clase)

            class_name = campos.group(1)
            parent_class = campos.group(2)
            properties = campos.group(3)
            relations = campos.group(4)
            objects = campos.group(5)

            knowledge_base[class_name] = {
                'parent': parent_class,
                'props': properties,
                'rel': relations,
                'objects': objects
            }

    return knowledge_base

def select_action():
    print("Seleccione una acción:")
    print("1. Mostrar extensión de una clase")
    print("2. Mostrar extensión de una propiedad")
    print("3. Mostrar las clases a las que pertenece un objeto")
    print("4. Mostrar la extension de una relacion")
    print("0. Salir")

    choice = input("Ingrese el número de la acción que desea realizar: ")
    return choice

def getObjects (class_name, knowledge_base):
    objects = re.findall (r'(\[[^\[\]]+,\[.*?\],\[.*?\]\])', knowledge_base[class_name]['objects'])
    return objects

def getObjectName(obj):
    campos = re.search(r'\[([^\[\]]+),(\[.*?\]),(\[.*?\])\]', obj )
    return  re.split('>',campos.group(1))[1]

def getObjectProps(obj):
    campos = re.search(r'\[([^\[\]]+),(\[.*?\]),(\[.*?\])\]', obj )
    return campos.group(2)

def getObjectRel(obj):
    campos = re.search(r'\[([^\[\]]+),(\[.*?\]),(\[.*?\])\]', obj )
    return  campos.group(3)

def isaParentClass(class_name,knowledge_base):
        for subclase in knowledge_base.keys():
             if class_name == knowledge_base[subclase]['parent']:
                 return True
        return False

# Función para obtener la extensión hacia atrás de una clase 
def class_backExtension(class_name, knowledge_base):
    extension = []

    extension.append(class_name)
    print ('back Class ='+class_name)

    topclase = knowledge_base[class_name]['parent']
    if topclase != 'top':
        for c in class_backExtension(topclase, knowledge_base): 
            extension.append(c)

    return extension
    
# Función para obtener la extensión de una clase en objetos
def objects_extension(class_name, knowledge_base):
    isparent = False
    extension = []

    for subclase in knowledge_base.keys():
        if class_name == knowledge_base[subclase]['parent']:
            isparent = True
            for obj in objects_extension(subclase,knowledge_base): 
                extension.append(obj)

    if not isparent:
        objects = getObjects(class_name, knowledge_base)
        for obj in objects:
            extension.append(obj)

    return extension


# Función para obtener la extensión de una clase
def class_extension(class_name, knowledge_base):
    isparent = False
    extension = []

    for subclase in knowledge_base.keys():
        if class_name == knowledge_base[subclase]['parent']:
            isparent = True
            for name in class_extension(subclase,knowledge_base): 
                extension.append(name)

    if not isparent:
        objects = getObjects(class_name, knowledge_base)
        for obj in objects:
            extension.append(getObjectName(obj))

    return extension


# Función para obtener la extensión de una propiedad
def property_extension(property_name, knowledge_base):
    hasProperty='unknown'
    isparent = False
    extension = {}

    for clase in knowledge_base.keys():
        if re.search(property_name,knowledge_base[clase]['props']):
            if re.search('not\('+property_name+'\)',knowledge_base[clase]['props']):
                hasProperty='no' 
                for obj in objects_extension(clase,knowledge_base): 
                    sujeto = getObjectName(obj) 
                    props = getObjectProps(obj) 
                    if re.search('not\('+property_name+'\)',props): 
                        hasProperty='no' 
                    if re.search(property_name,props): 
                        hasProperty='yes' 
                    extension[sujeto]=hasProperty
            else:
                hasProperty='yes' 
                for obj in objects_extension(clase,knowledge_base): 
                    sujeto = getObjectName(obj) 
                    props = getObjectProps(obj) 
                    if re.search('not\('+property_name+'\)',props): 
                        hasProperty='no' 
                    if re.search(property_name,props): 
                        hasProperty='yes' 
                    extension[sujeto]=hasProperty

    return extension


# Función para obtener la extensión de una propiedad
def classes_of_individual(object_name, knowledge_base):
    extension = []

    for clase in knowledge_base.keys():
        obj = knowledge_base[clase]['objects']
        if len(obj)>2 and object_name == getObjectName(obj): 
            print ('clase del objeto: ',clase)
            for c in class_backExtension(clase, knowledge_base):
                extension.append(c)
            break

    return extension

# Función para obtener la extensión de una propiedad
def relation_extension(relation_name, knowledge_base):
    extension = []

    for clase in knowledge_base.keys():
        relation = knowledge_base[clase]['rel']
        print ('relacion '+relation)
        if len(relation)>2 and re.search(relation_name,relation): 
            objects = getObjects(clase, knowledge_base) 
            for obj in objects: 
                extension.append(obj)
            break

    return extension

# Función para obtener la extensión de una relacion
def relation_extension(relation_name, knowledge_base):
    extension = []

    extension.append(relation_name)

    for clase in knowledge_base.keys():
        relation = knowledge_base[clase]['rel']

        if len(relation)>2 and re.search(relation_name,relation): 
            objects = getObjects(clase, knowledge_base) 
            for obj in objects: 
                nombre=getObjectName(obj)
                extension.append(nombre)
            break
    
    objects = objects_extension('top', knowledge_base) 
    for obj in objects: 
        rel=getObjectRel(obj)
        if len(rel)>2 and re.search(relation_name,rel): 
            nombre=getObjectName(obj)
            extension.append(nombre)

    return extension


def main():

    # en WINDOWS requiere el PATH al archivo
    #file_path = 'C:\\Users\\Donovan\\Downloads\\BD (3).txt'
    # en LINUX basta con el nombre del archivo en el mismo directorio
    file_path = 'BD.txt'
    base_conocimientos = load_knowledge_base(file_path)

    while True:
        action = select_action()

        if action == '1':
            clase = input('Mostrar extensión de >')
            extension = class_extension(clase, base_conocimientos)
            print("Extensión de la clase "+clase+": ", extension)
            print("\n")
        elif action == '2':
            property_name = input('Mostrar extensión de la propiedad >')
            extension = property_extension(property_name, base_conocimientos)
            print("Extensión de la propiedad "+property_name+": ", extension)
            print("\n")
        elif action == '3':
            object_name = input('Mostrar las clases a las que pertenece el objeto >')
            extension = classes_of_individual(object_name, base_conocimientos)
            print("Extensión de la clases de "+object_name+": ", extension)
            print("\n")
        elif action == '4':
            relation = input('Mostrar los objetos que tienen la relacion >') 
            extension = relation_extension(relation, base_conocimientos)
            print("Extensión de la relacion "+relation+": ", extension[1:])
            print("\n")
        elif action == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, seleccione una acción válida.")

if __name__ == "__main__":
    main()


