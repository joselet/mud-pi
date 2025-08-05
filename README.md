Paranoia MUD Pi
===============

Un intento de representación del juego de rol "Paranoia" llevado a un sencillo motor de mud basado en python.

Este proyecto proviene de un fork de mud-pi, del autor: [Frimkron/mud-pi](https://github.com/Frimkron/mud-pi)


Acerca de Paranoia
------------------
Paranoia es un juego de rol cómico, ambientado en un futuro distópico. Diseñado por Daniel Seth Gelber, Greg Costikyan, Eric Goldberg y Ken Rolston Paranoia fue publicado por primera vez en Estados Unidos por la editorial West End Games en 1984.[1]​ Presenta influencias de obras ambientadas en la distopía, como por ejemplo 1984 (de George Orwell), Un mundo feliz (de Aldous Huxley), Brazil, (de Terry Gilliam), o La naranja mecánica (de Anthony Burgess).

En 1991 Paranoia fue traducido y publicado en lengua española por la hoy en día desaparecida editorial barcelonesa Joc Internacional.

Fuente: [wikipedia](https://es.wikipedia.org/wiki/Paranoia_(juego_de_rol))

Requerimientos:
---------------
- Para arrancar el servidor: _Python_ (2.7+ or 3.3+) <http://www.python.org/download/>
- Del lado del cliente necesitarás telnet \<ip del servidor> 1234

[esta guia](http://technet.microsoft.com/en-us/library/cc771275%28v=ws.10%29.aspx)
puede ayudarte.

Instalar la base de datos
-------------------------
Abre una terminal y navega a la carpeta _admin_ y a continuación teclea:

	python install.py

O bien en Windows simplemente doble click en `install.py`


Ejecutando el Servidor
----------------------

### Windows

Doble click en `paranoia.py` - el fichero se abrirá con python


### En Mac OSX y Linux

Desde la terminal, ir al directorio principal y teclear:

	python paranoia.py
	
Nota, si te conectas al servidor por SSH verás que el script de juego se detiene cuando cierras la sesión SSH.

Una forma sencilla de evitarlo es usando una herramienta llamada `screen`. Conecta via SSH y ejecuta `screen`. Verás que estás en un shell normal, pero ahroa puedes ejecutar el script de python y pulsar `ctl+a` seguido de `d` para dejar
_screen_ funcionando background. La proxima vez que conectes, te puedes enganchar a tu sesión de screen usando `screen -r`. Tambén puedes 
[crear un daemon script](http://jimmyg.org/blog/2010/python-daemon-init-script.html)
para ejecutar el script cada vez que se inicie el servidor

Conectar al Server para jugar
-----------------------------

	telnet <ip address> 1234
	
Donde `<ip address>` es la IP externa del servidor. 1234 es el puerto sobre el que el servidor del juego está escuchando.

Al conectar recibirás un mensaje

	Qué nombre tiene tu personaje?

Ahí empieza todo.


Para salir del cliente de telnet, puedes pulsar Ctrl+C o teclear quitar


# Información adicional de posible interés (en inglés)

What is Telnet?
---------------

Telnet is simple text-based network communication protocol that was invented in
1969 and has since been superseded by other, more secure protocols. It does 
remain popular for a few specialised uses however, MUD games being one of these
uses. A long (and boring) history of the telnet protocol can be found here:
<http://www.cs.utexas.edu/users/chris/think/ARPANET/Telnet/Telnet.shtml>


What is a MUD?
--------------

MUD is short for Multi-User Dungeon. A MUD is a text-based online role-playing
game. MUDs were popular in the early 80s and were the precursor to the 
graphical Massively-Multiplayer Online Role-Playing Games we have today, like 
World of Warcraft. <http://www.mudconnect.com> is a great site for learning 
more about MUDs.

MUD-Pi-Based Projects
---------------------

Here are some of the cool projects people have made from MUD-Pi:

* **[ESP8266 MUD](http://git.savsoul.com/barry/esp8266-Mud) by Barry Ruffner** -
  a MUD that runs entirely within an ESP8266 microchip, using MicroPython
* **[MuddySwamp](https://github.com/ufosc/MuddySwamp) by the University of**
  **Florida Open Source Club** - a UF-themed MUD
* **[Dumserver](https://github.com/wowpin/dumserver) by Bartek Radwanski** - 
  a feature-rich MUD engine


Author
------

MUD Pi was written originally by Mark Frimston, then this fork by José Manuel Heras

For feedback, please email <mfrimston@gmail.com> or add a comment on the 
project's [Github page](http://github.com/frimkron/mud-pi)
