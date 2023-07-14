import mysql.connector
import requests
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os
from datetime import datetime

def load_public_key_from_file(file_path):
    with open(file_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())
    return public_key

def load_private_key_from_file(file_path, password=None):
    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=password, backend=openssl.backend)
    return private_key

def verificaPardeChaves():
    if not (os.path.exists("chave_privada.pem") and os.path.exists("chave_publica.pem")):
        print("Gerar um novo par de chaves")
        # Gerar um novo par de chaves
        chave_privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        chave_publica = chave_privada.public_key()

        # Salvar o par de chaves em arquivos PEM
        with open("chave_privada.pem", "wb") as chave_privada_arquivo:
            chave_privada_arquivo.write(
                chave_privada.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )
            print("Chave privada gerada com sucesso")
        with open("chave_publica.pem", "wb") as chave_publica_arquivo:
            chave_publica_arquivo.write(
                chave_publica.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )
            print("Chave pública gerada com sucesso")


def criptografar(texto):
    chave_publica = load_public_key_from_file("chave_publica.pem")  # Substitua pelo caminho da chave pública

    dado_bytes = texto.encode('utf-8')
    # Criptografar a mensagem usando a chave pública
    mensagem_criptografada = chave_publica.encrypt(
        dado_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return mensagem_criptografada


def descriptografar(texto_criptografado):
    chave_privada = load_private_key_from_file("chave_privada.pem")  # Substitua pelo caminho da chave privada

    # Descriptografar a mensagem usando a chave privada
    mensagem_descriptografada = chave_privada.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return mensagem_descriptografada


def verificarDB():
    print("Verificando se o banco de dados existe")
    # Defina as informações de conexão
    config = {
        #'host': '172.19.0.2',
        'host': 'localhost',
        'user': 'root',
        'password': 'ehcQ8jpfjrGST93n',
        'charset': "utf8mb4"
    }

    # Crie a conexão
    conn = mysql.connector.connect(**config)


    # Crie um cursor para executar consultas
    cursor = conn.cursor()

    # Execute a consulta para listar os bancos de dados
    cursor.execute("SHOW DATABASES")

    # Recupere os resultados
    databases = cursor.fetchall()

    # Verifique se o banco de dados desejado está na lista
    database_name = 'mlchallenge_db'
    database_exists = any(database_name in db for db in databases)

    if database_exists == False:
        # Crie o banco de dados
        cursor.execute("CREATE DATABASE mlchallenge_db")
        conn.commit()
        
        # Use o banco de dados recém-criado
        cursor.execute("USE mlchallenge_db")
        conn.commit()

        # Crie a tabela
        cursor.execute("""CREATE TABLE mlchallenge_tb (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            id_json INT,
                            user_name VARCHAR(255),
                            credit_card_num TEXT,
                            credit_card_ccv TEXT,
                            cuenta_numero VARCHAR(20),
                            codigo_zip CHAR(10),
                            fec_alta VARCHAR(30), 
                            direccion VARCHAR(255),
                            geo_latitud VARCHAR(20),
                            geo_longitud VARCHAR(20),
                            color_favorito VARCHAR(30),
                            foto_dni VARCHAR(255),
                            ip VARCHAR(20),
                            auto VARCHAR(255),
                            auto_modelo VARCHAR(255),
                            auto_tipo VARCHAR(255),
                            auto_color VARCHAR(255),
                            cantidad_compras_realizadas INT,
                            avatar VARCHAR(255),
                            fec_birthday VARCHAR(30)
                            )""")
        conn.commit()

    # Feche o cursor
    cursor.close()
    # Feche a conexão com o banco de dados
    conn.close()

def getJson():
    # Faça uma requisição GET para a URL
    response = requests.get("https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios")

    # Verifique o status da resposta
    if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
        # Obtenha o JSON da resposta
        json_data = response.json()

        # Conecte-se ao banco de dados
        conn = mysql.connector.connect(
            #host="172.19.0.2",
            host="localhost",
            user="root",
            password="ehcQ8jpfjrGST93n",
            database="mlchallenge_db",
            charset="utf8mb4"
        )

        # Crie um cursor para executar as consultas SQL
        cursor = conn.cursor()

        # Percore json e insire os dados no banco de dados
        for item in json_data:
            # Defina os dados a serem inseridos
            dados = {
                "id_json": item["id"],
                "user_name": item["user_name"],
                "credit_card_num": str(criptografar(item["credit_card_num"])),
                "credit_card_ccv": str(criptografar(item["credit_card_ccv"])),
                "cuenta_numero": item["cuenta_numero"],
                "codigo_zip": item["codigo_zip"],
                "fec_alta": item["fec_alta"],
                "direccion": item["direccion"],
                "geo_latitud": item["geo_latitud"],
                "geo_longitud": item["geo_longitud"],
                "color_favorito": item["color_favorito"],
                "foto_dni": item["foto_dni"],
                "ip": item["ip"],
                "auto": item["auto"],
                "auto_modelo": item["auto_modelo"],
                "auto_tipo": item["auto_tipo"],
                "auto_color": item["auto_color"],
                "cantidad_compras_realizadas": item["cantidad_compras_realizadas"],
                "avatar": item["avatar"],
                "fec_birthday": item["fec_birthday"]
            }

            # Defina a consulta SQL de inserção
            sql = """
                INSERT INTO mlchallenge_tb (
                    id_json, user_name, credit_card_num, credit_card_ccv, cuenta_numero, codigo_zip, fec_alta,
                    direccion, geo_latitud, geo_longitud, color_favorito, foto_dni, ip, auto,
                    auto_modelo, auto_tipo, auto_color, cantidad_compras_realizadas, avatar, fec_birthday
                )
                VALUES (
                    %(id_json)s, %(user_name)s, %(credit_card_num)s, %(credit_card_ccv)s, %(cuenta_numero)s, %(codigo_zip)s, %(fec_alta)s,
                    %(direccion)s, %(geo_latitud)s, %(geo_longitud)s, %(color_favorito)s, %(foto_dni)s, %(ip)s, %(auto)s,
                    %(auto_modelo)s, %(auto_tipo)s, %(auto_color)s, %(cantidad_compras_realizadas)s, %(avatar)s, %(fec_birthday)s
                )
            """

            # Execute a consulta SQL com os dados fornecidos
            cursor.execute(sql, dados)

            # Faça o commit da transação
            conn.commit()

        # Feche o cursor e a conexão com o banco de dados
        cursor.close()
        conn.close()
    else:
        print("Erro ao obter o JSON da URL:", response.status_code)



#Função para verificar e criar banco de dados
verificarDB()

# Verificar se o par de chaves já existe, caso não exista, gerar um novo par de chaves
verificaPardeChaves()

#Função para pegar dados do JSON e inserir no banco de dados
getJson()