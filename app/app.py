import os
import time
import logging
from flask import Flask, render_template, jsonify, request
from redis import Redis
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__, template_folder=('.'))

# Configura el logging
logging.basicConfig(level=logging.INFO)

# ~ Conexion a Redis ~
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_conn = Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def connect_to_redis():
    # Intenta conectarte a redis
    logging.info(f"Intentando conectar a Redis en {redis_host}...")
    retries = 5
    while retries > 0:
        try:
            redis_conn.ping()
            logging.info("Conectado a Redis exitosamente =)")
            redis_conn.msetnx({'Dubstep': 0, 'Raw': 0})
            return redis_conn
        except Exception as e:
            logging.warning(f"No se pudo conectar a Redis: {e}. Reintentando en 5 segundos...")
            retries -= 1
            time.sleep(5)
    logging.error("No se pudo conetar a Redis despues de varios intentos")
    return None

redis = connect_to_redis()

# ~ Conexion a PostgreSQL ~
db_host = os.environ.get('POSTGRES_HOST', 'localhost')
db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
def connect_to_postgres():
    # Intenta conectarte a PostgreSQL 
    logging.info(f"Intentando conectar a PostgreSQL en {db_host}")
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host
            )
            logging.info("Conectado a PostgreSQL correctamente =)")
            return conn
        except OperationalError as e:
            logging.warning(f"No se pudo conectar a PostgreSQL: {e}. Reintentando en 5 segundos...")
            retries -= 1
            time.sleep(5)
    logging.error("No se pudo conectar a PostgreSQL despuees de varios intentos.")
    return None

db_conn = connect_to_postgres()

# ~ Rutas de la aplicacion ~

@app.route('/')
def index():
    # Landing page
    return render_template('index.html')

@app.route('/stats')
def stats_page():
    # Result page
    return render_template('results.html')

@app.route('/vote', methods=['POST'])
def vote():
    # Gestion del voto
    if not redis:
        return jsonify({'error': 'Servicio de Redis no disponible'}), 500
    try:
        data = request.get_json()
        vote_option = data.get('vote')

        if vote_option not in ['dubstep', 'raw']:
            return jsonify({'error': 'Voto invalido'}), 400
        
        # Incrementar el contador en Redis
        total_votes = redis.incr(vote_option)
        logging.info(f"Voto registrado para {vote_option}. Total: {total_votes}")

        return jsonify({'success': True, vote_option: total_votes})
    except Exception as e:
        logging.error(f"Error en /vote: {e}")
        return jsonify({'error': 'Error Interno del servidor'}), 500
    
@app.route('/results', methods=['GET'])
def results():
    """Devuelve los resultados actuales de la votación."""
    if not redis:
        return jsonify({'error': 'Servicio de Redis no disponible'}), 500

    try:
        # CAMBIO: Obtiene los valores de las nuevas opciones
        dubstep_votes = redis.get('dubstep')
        raw_votes = redis.get('raw')
        
        # CAMBIO: Devuelve el JSON con las nuevas opciones
        return jsonify({
            'dubstep': int(dubstep_votes) if dubstep_votes else 0,
            'raw': int(raw_votes) if raw_votes else 0
        })
    except Exception as e:
        logging.error(f"Error en /results: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)