#
#  Posgrado en Ingenieria y en Ciencias de la Computacion
#  Inteligencia Artificial
#  Proyecto sobre representacion del conocimiento
#
#  Equipo:
#       Montejano Lopez Donovan Jesus (1.a -> 1.d)
#       Murrieta Leon Juan Eduardo    (1.a -> 2.c)
#
#  Se implementan los predicados:
#       1.a class_extension
#	    1.b property_extension
#	    1.c relation_extension
#	    1.d classes_of_individual
#       1.e properties_of_individual
#       1.e class_properties
#       1.f relations_of_individual
#       1.f class_relations
#       
#       2.a add_class
#       2.a add_object
#       2.b add_class_property
#       2.c add_object_property
#
#       Opciones para leer y guardar la Base de Conocimiento
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

def save_knowledge_base(file_path,knowledge_base):
    #single_line_KB=""
    counter=0

    newKnowledgeBase = open(file_path, 'w') 
    print('[', file=newKnowledgeBase)
    for clase in knowledge_base.keys():
        print ('class(',clase,',',
                knowledge_base[clase]['parent'], ',',
                knowledge_base[clase]['props'], ',',
                knowledge_base[clase]['rel'], ',',
                knowledge_base[clase]['objects'],
                ')',file = newKnowledgeBase, end="")
        counter+=1
        if counter<len(knowledge_base):
            print(',',file = newKnowledgeBase)
    print('\n]', file=newKnowledgeBase)
    return

def select_action(KB):
    print("----- Base: "+KB+" ---------")
    print("Seleccione una acción:")
    print("1. Mostrar extensión de una clase")
    print("2. Mostrar extensión de una propiedad")
    print("3. Mostrar las clases a las que pertenece un objeto")
    print("4. Mostrar la extension de una relacion")
    print("5. Mostrar las propiedades de un objeto")
    print("6. Mostrar las propiedades de una clase")
    print("7. Mostrar las relaciones de un individuo")
    print("8. Mostrar las relaciones de una clase")
    print("9. Añadir nueva clase")
    print("10. Añadir nuevo objeto")
    print("11. Añadir nueva propiedad a una clase")
    print("12. Añadir nueva propiedad a un objeto")
    print("..................................")
    print("13. Guardar Base de Conocimiento")
    print("14. Cargar Base de Conocimiento")
    print("0. Salir")

    choice = input("Ingrese el número de la acción que desea realizar: ")
    return choice

def fixInput(inp):
    tmp = inp.replace(" ","")
    tmp = tmp.replace("(","\(")
    tmp = tmp.replace(")","\)")
    return tmp


def getObjects (class_name, knowledge_base):
    objects = re.findall (r'(\[[^\[\]]+,\[.*?\],\[.*?\]\])', knowledge_base[class_name]['objects'])
    return objects

def getObjectName(obj):
    campos = re.search(r'\[([^\[\]]+),(\[.*?\]),(\[.*?\])\]', obj )
    return  re.split('>',campos.group(1))[1]

def getObjectProps(obj):
    campos = re.search(r'\[([^\[\]]+),(\[.*?\]),(\[.*?\])\]', obj )
    return campos.group(2)

def setObjectProps(obj, properties):
    campos = re.search(r'\[([^\[\]]+),(\[.*?\]),(\[.*?\])\]', obj )
    newObj = '['+campos.group(1)+','+properties+','+campos.group(3)+']'
    return newObj

def getObjectRel(obj):
    campos = re.search(r'\[([^\[\]]+),(\[.*?\]),(\[.*?\])\]', obj )
    return  campos.group(3)

def getRelatedObject(relationName,relation):
    campos = re.findall(r'(\w+=>\w+)', relation )
    related=[]
    for rel in campos:
        negativeRelation=False
        if re.search(r'not\('+rel+'\)',relation):
            negativeRelation=True
        relations = re.findall(r'(\w+)=>(\w+)',rel)
        for r in relations:
            if r[0]==relationName:
                if negativeRelation: 
                    related.append('not('+r[1]+')') 
                else: 
                    related.append(r[1]) 
    return(related)

def isaParentClass(class_name,knowledge_base):
        for subclase in knowledge_base.keys():
             if class_name == knowledge_base[subclase]['parent']:
                 return True
        return False

def addProperty(property_name, properties):
        campos = re.split(r',', properties.lstrip('[').rstrip(']') )
        campos.append (property_name)
        props = ','.join(campos)
        return '['+props+']'

def addRelation(property_name,property_value,properties):
        campos = re.findall(r'(\w+=>\w+)', properties )
        campos.append (property_name+'=>'+property_value)
        props = ','.join(campos)
        return '['+props+']'


# Función para obtener la extensión hacia atrás de una clase 
def class_backExtension(class_name, knowledge_base):
    extension = []

    extension.append(class_name)

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
        objects = getObjects(clase, knowledge_base)
        for obj in objects: 
            if len(obj)>2 and object_name == getObjectName(obj): 
                for c in class_backExtension(clase, knowledge_base): 
                    extension.append(c) 
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
                relaciones=getRelatedObject(relation_name,relation) 
                nombre=getObjectName(obj) 
                extension.append(nombre+':'+','.join(relaciones))
            break
    
    objects = objects_extension('top', knowledge_base) 
    for obj in objects: 
        rel=getObjectRel(obj)
        if len(rel)>2 and re.search(relation_name,rel): 
            print(rel)
            relaciones=getRelatedObject(relation_name,rel)
            nombre=getObjectName(obj)
            extension.append(nombre+':'+','.join(relaciones))

    return extension

# Función para obtener las propiedades de un objeto
def properties_of_individual(subject_name, knowledge_base):
    properties = []
    objects = objects_extension('top', knowledge_base) 
    for obj in objects: 
        nombre=getObjectName(obj)
        if nombre == subject_name:
            properties.append(re.split(',',getObjectProps(obj).lstrip('[').rstrip(']')))
            clases = classes_of_individual(nombre,knowledge_base)
            for c in clases:
                props = knowledge_base[c]['props'].lstrip('[').rstrip(']').split(',')
                for p in props: 
                    properties.append(p)
            
    return properties

# Función para obtener las propiedades de una clase
def class_properties(class_name, knowledge_base):
    properties=[]
    classback = class_backExtension(class_name, knowledge_base)
    for c in classback: 
        props = knowledge_base[c]['props'].lstrip('[').rstrip(']').split(',') 
        for p in props: 
            properties.append(p)

    return properties

# Función para obtener las relaciones de un objeto
def relations_of_individual(subject_name, knowledge_base):
    properties = []
    objects = objects_extension('top', knowledge_base) 
    for obj in objects: 
        nombre=getObjectName(obj)
        if nombre == subject_name:
            properties.append(getObjectRel(obj).lstrip('[').rstrip(']'))
            
    return properties

# Función para insertar una nueva clase y generar una nueva
# base de conocimiento
def add_class(class_name, mother_class,knowledge_base):
    new_knowledge_base={}

    for key, value in knowledge_base.items(): 
        new_knowledge_base[key] = value
        if key==mother_class:
            new_knowledge_base[class_name] = {}
            new_knowledge_base[class_name]['parent']  = mother_class
            new_knowledge_base[class_name]['props']   = []
            new_knowledge_base[class_name]['rel']     = []
            new_knowledge_base[class_name]['objects'] = []

    return new_knowledge_base

# Agregar nuevo objeto en la base de conocimiento y generar
# una nueva base
def add_object(object_name, mother_class,knowledge_base):
    new_knowledge_base={}

    objects = getObjects(mother_class,knowledge_base)
    objects.append('[id=>'+object_name+',[],[]]')
    knowledge_base[mother_class]['objects']=','.join(objects)

    for key, value in knowledge_base.items(): 
        new_knowledge_base[key] = value

    return new_knowledge_base


# Función para insertar una propiedad a una clase y generar una nueva
# base de conocimiento
def add_class_property(class_name, property_name, knowledge_base):
    new_knowledge_base={}

    for key, value in knowledge_base.items(): 
        new_knowledge_base[key] = value
        if key==class_name:
            properties = new_knowledge_base[class_name]['props']
            properties = addProperty(property_name, properties)
            new_knowledge_base[class_name]['props'] = properties

    return new_knowledge_base

# Función para insertar una propiedad a un objeto y generar una nueva
# base de conocimiento
def add_object_property(object_name, mother_class, property_name, knowledge_base):
    new_knowledge_base={}

    new_knowledge_base = knowledge_base

    objects = getObjects(mother_class,knowledge_base)
    for obj in range(len(objects)): 
        if object_name == getObjectName(objects[obj]):
            properties = getObjectProps (objects[obj]) 
            properties = addProperty(property_name, properties)
            objects[obj] = setObjectProps(objects[obj],properties)
            new_knowledge_base[mother_class]['objects'] = '['+','.join(objects)+']'

    return new_knowledge_base


def main():

    # en WINDOWS requiere el PATH al archivo
    #file_path = 'C:\\Users\\Donovan\\Downloads\\BD (3).txt'
    # en LINUX basta con el nombre del archivo en el mismo directorio
    file_path = 'BD.txt'
    base_conocimientos = load_knowledge_base(file_path)

    while True:
        action = select_action(file_path)

        if action == '1':
            clase = fixInput(input('Mostrar extensión de >'))
            extension = class_extension(clase, base_conocimientos)
            print("\n----------------------------------------------------")
            print("Extensión de la clase "+clase+": ", extension)
            print("----------------------------------------------------")
        elif action == '2':
            property_name = fixInput(input('Mostrar extensión de la propiedad >'))
            extension = class_extension(clase, base_conocimientos)
            extension = property_extension(property_name, base_conocimientos)
            print("\n----------------------------------------------------")
            print("Extensión de la propiedad "+property_name+": ", extension)
            print("----------------------------------------------------")
        elif action == '3':
            object_name = fixInput(input('Mostrar las clases a las que pertenece el objeto >'))
            extension = classes_of_individual(object_name, base_conocimientos)
            print("\n----------------------------------------------------")
            print("Extensión de la clases de "+object_name+": ", extension)
            print("----------------------------------------------------")
        elif action == '4':
            relation = fixInput(input('Mostrar los objetos que tienen la relacion >'))
            extension = relation_extension(relation, base_conocimientos)
            print("\n----------------------------------------------------")
            print("Extensión de la relacion "+relation+": ", extension[1:])
            print("----------------------------------------------------")
        elif action == '5':
            object_name = fixInput(input('Mostrar las propiedades del objeto >'))
            extension = properties_of_individual(object_name, base_conocimientos)
            print("\n----------------------------------------------------")
            print("Propiedades del objeto "+object_name+": ", extension)
            print("----------------------------------------------------")
        elif action == '6':
            object_name = fixInput(input('Mostrar las propiedades de la clase >'))
            extension = class_properties(object_name, base_conocimientos)
            print("\n----------------------------------------------------")
            print("Propiedades del objeto "+object_name+": ", extension)
            print("----------------------------------------------------")
        elif action == '7':
            object_name = fixInput(input('Mostrar las relaciones de un individuo >'))
            extension = relations_of_individual(object_name, base_conocimientos)
            print("\n----------------------------------------------------")
            print("Propiedades del objeto "+object_name+": ", extension)
            print("----------------------------------------------------")
        elif action == '8':
            class_name = fixInput(input('Mostrar las relaciones de una clase >'))
            extension = class_properties(class_name, base_conocimientos)
            print("\n----------------------------------------------------")
            print("Propiedades del objeto "+class_name+": ", extension)
            print("----------------------------------------------------")
        elif action == '9':
            class_name = fixInput(input('Nombre de la clase >'))
            mom_class  = fixInput(input('Nombre de la clase madre >'))
            try: 
                if base_conocimientos[mom_class]: 
                    new_kb_name = fixInput(input('Nombre la nueva base de conocimiento >')) 
                    base_conocimientos = add_class(class_name, mom_class, base_conocimientos) 
                    save_knowledge_base(new_kb_name, base_conocimientos) 
                    print("\n----------------------------------------------------") 
                    print("Definicion nueva clase '"+class_name+"': ", base_conocimientos[class_name]) 
                    print("----------------------------------------------------")
            except KeyError: 
                print("\n----------------------------------------------------") 
                print("Error: clase '"+mom_class+"' desconocida")
                print("\n")
        elif action == '10':
            object_name = fixInput(input('Nombre del objeto >'))
            mom_class  = fixInput(input('Nombre de la clase madre >'))
            try: 
                if base_conocimientos[mom_class]: 
                    new_kb_name = fixInput(input('Nombre la nueva base de conocimiento >')) 
                    base_conocimientos=add_object(object_name, mom_class, base_conocimientos)
                    save_knowledge_base(new_kb_name, base_conocimientos) 
                    print("\n----------------------------------------------------") 
                    print("Lista de objetos '"+mom_class+"': ", base_conocimientos[mom_class]['objects']) 
                    print("----------------------------------------------------")
            except KeyError: 
                print("\n----------------------------------------------------") 
                print("Error: clase '"+mom_class+"' desconocida")
                print("\n")
        elif action == '11':
            class_name = fixInput(input('Nombre de la clase >'))
            property_name  = fixInput(input('Nombre de la propiedad >'))
            try: 
                if base_conocimientos[class_name]: 
                    new_kb_name = fixInput(input('Nombre la nueva base de conocimiento >')) 
                    base_conocimientos = add_class_property(class_name, property_name, base_conocimientos)
                    save_knowledge_base(new_kb_name, base_conocimientos) 
                    print("\n----------------------------------------------------") 
                    print("Propiedades de la clase '"+class_name+"': ", base_conocimientos[class_name]['props'])
                    print("----------------------------------------------------")
            except KeyError: 
                print("\n----------------------------------------------------") 
                print("Error: clase '"+class_name+"' desconocida")
                print("\n")
        elif action == '12':
            object_name = fixInput(input('Nombre del objeto >'))
            class_name = fixInput(input('Nombre de la clase del objeto >'))
            property_name  = fixInput(input('Nombre de la propiedad >'))
            try: 
                if base_conocimientos[class_name]: 
                    new_kb_name = fixInput(input('Nombre la nueva base de conocimiento >')) 
                    base_conocimientos = add_object_property(object_name, class_name, property_name, base_conocimientos)
                    save_knowledge_base(new_kb_name, base_conocimientos) 
                    extension = properties_of_individual(object_name, base_conocimientos)
                    print("\n----------------------------------------------------") 
                    print("Propiedades del objeto '"+object_name+"': ",extension) 
                    print("----------------------------------------------------")
            except KeyError: 
                print("\n----------------------------------------------------") 
                print("Error: clase '"+class_name+"' desconocida")
                print("\n")
        elif action == '13': 
            new_kb_name = fixInput(input('Nombre de la base de conocimiento ['+file_path+']>')) 
            if new_kb_name=="":
                new_kb_name=file_path
            save_knowledge_base(new_kb_name, base_conocimientos) 
        elif action == '14': 
            new_kb_name = fixInput(input('Nombre de la base de conocimiento ['+file_path+']>')) 
            if new_kb_name=="":
                new_kb_name=file_path 
            try : 
                base_conocimientos = load_knowledge_base(new_kb_name)
            except FileNotFoundError:
                print("\n----------------------------------------------------") 
                print("Error: Archivo no localizado: "+new_kb_name)
                print("\n")
                continue
            file_path=new_kb_name
        elif action == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, seleccione una acción válida.")

if __name__ == "__main__":
    main()


