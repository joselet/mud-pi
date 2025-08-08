-- drop table if exists players;
CREATE TABLE IF NOT EXISTS players (
    name TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    nivel INTEGER DEFAULT 0,
    clon INTEGER DEFAULT 1,
    pv_max INTEGER DEFAULT 100,
    pv INTEGER DEFAULT 100,
    e_max INTEGER DEFAULT 100,
    e INTEGER DEFAULT 100,
    f INTEGER DEFAULT 10,
    r INTEGER DEFAULT 10,
    a INTEGER DEFAULT 10,
    d INTEGER DEFAULT 10,
    p INTEGER DEFAULT 10,
    c INTEGER DEFAULT 10,
    tm INTEGER DEFAULT 10,
    pm INTEGER DEFAULT 10,
    servicio TEXT,
    sociedad_secreta TEXT,
    sector TEXT,
    room TEXT DEFAULT 'inicio',
    config TEXT ,
    inventario TEXT ,
    traicion INTEGER DEFAULT 0
);

-- Insertar jugadores (para pruebas)
/*
INSERT INTO players (name,password,nivel,clon,pv_max,pv,e_max,e,f,r,a,d,p,c,tm,pm,servicio,sociedad_secreta,sector,room,config,inventario,traicion) VALUES
	 ('jose','jose',1,1,100,86,100,110,16,8,18,16,13,5,1,18,'SEG','Comunistas','ANO','inicio','{"tiradas": false, "detallado": false}','{}',1),
	 ('pepe','pepe',0,2,100,3,100,70,8,17,9,20,11,12,19,7,'SCP','Piratas Informáticos','ICO','lab/p3_pasillo_genetico','{}','{}',1),
	 ('juan','juan',0,1,100,27,100,56,7,8,8,17,9,1,10,17,'SCP','Piratas Informáticos','ANO','lab/p3_pasillo_genetico','{}','{}',3),
	 ('pinki','winki',0,6,100,25,100,68,9,11,12,14,1,7,14,11,'SID','Comunistas','EKO','inicio','{"tiradas": true, "detallado": true}','{}',0),
	 ('tinki','winki',0,1,100,42,100,63,12,10,13,11,10,20,10,7,'SDF','Iglesia Primitiva del Cristo Programador','ICO','lab/p3_pasillo_genetico','{"detallado": true}','{}',0),
	 ('cpu','inmortal',7,1,100,100,100,100,20,20,20,20,20,20,1,1,'SBD','Piratas Informáticos','ANO','lab/p3_pasillo_genetico','{}','{}',0),
	 ('ordenador','inmortal',8,1,1000,1000,100,100,200,200,20,20,20,20,20,1,'SBD','Piratas Informáticos','ANO','inicio',NULL,NULL,0);
*/
