%
%  Posgrado en Ingenieria y en Ciencias de la Computacion
%  Inteligencia Artificial
%  Proyecto sobre representacion del conocimiento
%
%  Equipo:
%  	Montejano Lopez Donovan Jesus
%  	Murrieta Leon Juan Eduardo
%
%  Solo se implementa el predicado 
%  	class_extension
%

class_extension(CLASE,KB,OBJCLASE):-
        objetos_desde_clase(CLASE,KB,OBJCLASE).

objetos_desde_clase(CLASE,KB,OBJETOS):-
	% obtine los objetos de esta clase
        objetos_de_clase(CLASE,KB,OBJETOSNODO),
	% obtiene todas las subclases
        subclases(CLASE,KB,TOTSUBCLASES),
	% obtiene todos los objetos de las subclases
        objetos_subclases(TOTSUBCLASES,KB,OBJETOSSUBCLASES),
        append(OBJETOSNODO,OBJETOSSUBCLASES,OBJETOS),!.

% Retorna los objetos de la clase CLASE
objetos_de_clase(CLASE,[class(CLASE,_,_,_,OBJCLASE)|_],OBJETOS):-
        id_objeto(OBJCLASE,OBJETOS).

objetos_de_clase(CLASE,[_|T],OBJETOS):- % Salta la siguiente clase
        objetos_de_clase(CLASE,T,OBJETOS).

% Extrae el nombre asignado en el id        
id_objeto([],[]). % No hay elementos
id_objeto([[id=>NOM,_,_]|_],NOMBRE):-
	append([NOM],[],NOMBRE).

% Retorna las subclases de una clase
subclases(CLASE,KB,SUBCLASES):-
        subclases_de_clase(CLASE,KB,SCLASES),
        todas_las_subclases(SCLASES,KB,SUBCLASES).

%
% Desciende al siguiente nivel de una clase y retorna sus
% subclases
%
subclases_de_clase(_,[],[]). % Fin del arbol, no mas clases

% En [H|T] H debe tener la forma del functor class, se ignoran
% los demás atributos
subclases_de_clase(CLASE,[class(SUBCLASE,CLASE,_,_,_)|T],SUBCLASES):-
        subclases_de_clase(CLASE,T,RAMAS),
        append([SUBCLASE],RAMAS,SUBCLASES).

% El functor en H no tiene a CLASE como superior
subclases_de_clase(CLASE,[_|T],SUBCLASES):-
        subclases_de_clase(CLASE,T,SUBCLASES).


% Retorna todas las subclases
todas_las_subclases([],_,[]).  % Ultimo nivel, devuelve vacio
todas_las_subclases(CLASES,KB,TODASSUBCLASES):-
        subclases_en_lista_clases(CLASES,KB,SUBCLASES),
        todas_las_subclases(SUBCLASES,KB,SUBSUBCLASES),
        append(CLASES,SUBSUBCLASES,TODASSUBCLASES).

% Recorre una lista de clases y retornas todas las subclases
% de esa lista
subclases_en_lista_clases([],_,[]). % No hay mas clases
subclases_en_lista_clases([CLASE|T],KB,SUBCLASES):-
        subclases_de_clase(CLASE,KB,SUBCLASESI),
        subclases_en_lista_clases(T,KB,SUBCLASESD),
        append(SUBCLASESI,SUBCLASESD,SUBCLASES).

% Retorna todas los objetos de la lista de clases
% y sus subclases
objetos_subclases([],_,[]). % No hay mas clases
objetos_subclases([CLASE|T],KB,TOTOBJETOS):-
        objetos_de_clase(CLASE,KB,OBJETO),
        objetos_subclases(T,KB,OBJETOS),
        append(OBJETO,OBJETOS,TOTOBJETOS).

% Manejo de archivos obtenido de:
% https://turing.iimas.unam.mx/~luis/cursos/IA2022-1/proyectos/Manejo_de_archivos.zip
%--------------------------------------------------
% Load and Save from files
%--------------------------------------------------


%KB open and save

open_kb(Route,KB):-
        open(Route,read,Stream),
        readclauses(Stream,X),
        close(Stream),
        atom_to_term(X,KB).

save_kb(Route,KB):-
        open(Route,write,Stream),
        writeq(Stream,KB),
        close(Stream).

readclauses(InStream,W) :-
        get0(InStream,Char),
        checkCharAndReadRest(Char,Chars,InStream),
        atom_chars(W,Chars).

checkCharAndReadRest(-1,[],_) :- !.  % End of Stream
checkCharAndReadRest(end_of_file,[],_) :- !.

checkCharAndReadRest(Char,[Char|Chars],InStream) :-
        get0(InStream,NextChar),
        checkCharAndReadRest(NextChar,Chars,InStream).

%compile an atom string of characters as a prolog term
atom_to_term(ATOM, TERM) :-
        atom(ATOM),
        atom_to_chars(ATOM,STR),
        atom_to_chars('.',PTO),
        append(STR,PTO,STR_PTO),
        read_from_chars(STR_PTO,TERM).

:- op(800,xfx,'=>').

