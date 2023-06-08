from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

from config import config

app=Flask(__name__)

conexion = MySQL(app)

@app.route('/clients', methods=['GET'])
def list():
    try:
        cursor=conexion.connection.cursor()
        sql= "SELECT id, name,adress, cellphone FROM client"
        # ejecutar la consulta
        cursor.execute(sql)
        # Convertir la repuesta en algo entendible para python
        datos=cursor.fetchall()
        clientes=[]
        for fila in datos:
            cliente={'id':fila[0], 'name':fila[1], 'adress':fila[2], 'cellphone':fila[3] }
            clientes.append(cliente)
        return jsonify({'clientes': clientes, 'mensaje':"lista de clientes"})
    except Exception as ex:    
      return jsonify({ 'mensaje':"lista de clientes"})

@app.route('/clients/<name>', methods=['GET'])  
def client(name):
    try:
        cursor=conexion.connection.cursor()
        sql= "SELECT id, name,adress, cellphone FROM client Where name = '{0}'".format(name)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
             cliente={'id':datos[0], 'name':datos[1], 'adress':datos[2], 'cellphone':datos[3] } 
             return jsonify({'cliente': cliente, 'mensaje':"Cliente encontrado"})
        else:
            return jsonify({ 'mensaje':"Cliente NO encontrado"})
              
    except Exception as ex:
        return jsonify({ 'mensaje':"error"})

@app.route('/clients', methods=['POST'])              
def new_client():
    try:
        ###Traer el objeto de la petición
        # print(request.json)
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO client (id, name, adress, cellphone) VALUES ('{0}', '{1}', '{2}', '{3}')""".format(request.json['id'], request.json['name'], request.json['adress'], request.json['cellphone' ])
        cursor.execute(sql)
        conexion.connection.commit() ###onfirma la acción de insercción
        return jsonify({ 'mensaje':"cliente registrad"})  
        
    except Exception as ex:
        return jsonify({ 'mensaje':"error"})        


@app.route('/clients/<name>', methods=['DELETE'])
def delete_client(name):
    try:
        cursor=conexion.connection.cursor()
        sql= "DELETE FROM client WHERE name = '{0}'".format(name)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({ 'mensaje':"cliente eliminado"}) 
    except Exception as ex:
        return jsonify({ 'mensaje':"error"}) 

@app.route('/clients/<name>', methods=['PUT'])    
def update_client(name):
    try:
        ###Traer el objeto de la petición
        # print(request.json)
        cursor=conexion.connection.cursor()
        sql= """UPDATE client SET id = '{0}', adress = '{1}', cellphone = '{2}' WHERE name = '{3}' """.format(request.json['id'], request.json['adress'], request.json['cellphone'], name)
        cursor.execute(sql)
        conexion.connection.commit() ###onfirma la acción de insercción
        return jsonify({ 'mensaje':"cliente actualizado"})  
        
    except Exception as ex:
        return jsonify({ 'mensaje':"error"}) 
        
  
def pagina_no_encontrada(error):
    return "<h1> La página NO existe </h1>", 404

if __name__ == '__main__':
    # Acceder al diccionario de config
    app.config.from_object(config['development'])
    # registrar el error
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()