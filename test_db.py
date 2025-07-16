from sqlalchemy import create_engine, text

try:

    engine = create_engine("mysql+pymysql://root:@localhost/diagnostico_db")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexão com SQLAlchemy bem-sucedida:", result.fetchone())
except Exception as e:
    print("Erro na conexão com SQLAlchemy:", str(e))

try:
    import mysql.connector
    cnx = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='diagnostico_db'
    )
    print("Conexão direta com mysql-connector-python bem-sucedida")
    cnx.close()
except Exception as err:
    print("Erro na conexão direta com mysql-connector-python:", str(err))