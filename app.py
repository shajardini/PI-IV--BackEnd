import mysql.connector
from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import requests
from sklearn.preprocessing import LabelEncoder

#piIv

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'books',
    'user': 'root',
    'password': 'salomao775'
}

def conectar():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    return conn, cursor

def criar_tabela_livros():
    conn, cur = conectar()

    # Criação da tabela "livros" se ela ainda não existir
    cur.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT,
            serie TEXT,
            tema TEXT,
            faixa_etaria INT,
            quantidade INT,
            avaliacao INT,
            img_url TEXT,
            curtidas INT DEFAULT 0
        )
    ''')

    conn.commit()
    cur.close()
    conn.close()

# Buscar todos os livros
# Buscar todos os livros
@app.route('/livros', methods=['GET'])
def obter_livros():
    conn, cur = conectar()

    cur.execute('SELECT * FROM livros ORDER BY curtidas DESC')
    livros = []
    for row in cur.fetchall():
        id, titulo, autor, serie, tema, faixa_etaria, quantidade, avaliacao, img_url, curtidas = row
        livro_dict = {
            'id': id,
            'titulo': titulo,
            'autor': autor if autor else 'Não definido',
            'serie': serie if serie else 'Não definida',
            'tema': tema if tema else 'Não definido',
            'faixa_etaria': faixa_etaria,
            'quantidade': quantidade,
            'avaliacao': avaliacao,
            'img_url': img_url,
            'curtidas': curtidas
        }
        livros.append(livro_dict)
       

    cur.close()
    conn.close()

    return jsonify(livros)



@app.route('/livros/series', methods=['GET'])
def listar_series():
    conn, cur = conectar()

    cur.execute("SELECT DISTINCT serie FROM livros ORDER BY curtidas DESC;")
    series = [serie[0] for serie in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(series)


@app.route('/livros/series/<string:serie>', methods=['GET'])
def obter_livros_por_serie(serie):
    conn, cur = conectar()

    cur.execute("SELECT id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas FROM livros WHERE serie = %s;", (serie,))
    livros = []
    for row in cur.fetchall():
        id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas = row
        livro_dict = {
            'id': id,
            'titulo': livro,
            'autor': autor,
            'serie': serie,
            'tema': tema,
            'faixa_etaria': faixa_etaria,
            'quantidade': quantidade,
            'avaliacao': avaliacao,
            'img_url': img_url,
            'curtidas': curtidas
        }
        livros.append(livro_dict)

    cur.close()
    conn.close()

    return jsonify(livros)

@app.route('/livros/faixa_etaria/<int:faixa_etaria>', methods=['GET'])
def obter_livros_por_faixa_etaria(faixa_etaria):
    conn, cur = conectar()

    cur.execute("SELECT id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas FROM livros WHERE faixa_etaria = %s;", (faixa_etaria,))
    livros = []
    for row in cur.fetchall():
        id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas = row
        livro_dict = {
            'id': id,
            'titulo': livro,
            'autor': autor,
            'serie': serie,
            'tema': tema,
            'faixa_etaria': faixa_etaria,
            'quantidade': quantidade,
            'avaliacao': avaliacao,
            'img_url': img_url,
            'curtidas': curtidas
        }
        livros.append(livro_dict)

    cur.close()
    conn.close()

    return jsonify(livros)


@app.route('/livros/autor', methods=['GET'])
def obter_autores():
    conn, cur = conectar()

    cur.execute("SELECT DISTINCT autor FROM livros ORDER BY curtidas DESC;")
    autores = [autor[0] for autor in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(autores)


@app.route('/livros/autor/<string:autor>', methods=['GET'])
def obter_livros_por_autor(autor):
    conn, cur = conectar()

    cur.execute("SELECT id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas FROM livros WHERE autor = %s;", (autor,))
    livros = []
    for row in cur.fetchall():
        id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas = row
        livro_dict = {
            'id': id,
            'livro': livro,
            'autor': autor,
            'serie': serie,
            'tema': tema,
            'faixa_etaria': faixa_etaria,
            'quantidade': quantidade,
            'avaliacao': avaliacao,
            'img_url': img_url,
            'curtidas': curtidas
        }
        livros.append(livro_dict)

    cur.close()
    conn.close()

    return jsonify(livros)

@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):
    conn, cur = conectar()

    cur.execute("SELECT id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas FROM livros WHERE id = %s;", (id,))
    livro = cur.fetchone()

    cur.close()
    conn.close()

    if livro:
        livro_dict = {
            'id': livro[0],
            'titulo': livro[1],
            'autor': livro[2],
            'serie': livro[3],
            'tema': livro[4],
            'faixa_etaria': livro[5],
            'quantidade': livro[6],
            'avaliacao': livro[7],
            'img_url': livro[8],
            'curtidas': livro[9]
        }
        return jsonify(livro_dict)
    else:
        return jsonify({'message': 'Livro não encontrado.'}), 404


@app.route('/livros/temas', methods=['GET'])
def listar_temas():
    conn, cur = conectar()

    cur.execute("SELECT DISTINCT tema FROM livros ORDER BY curtidas DESC;")
    temas = [tema[0] for tema in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(temas)

@app.route('/livros/temas/<string:tema>', methods=['GET'])
def obter_livros_por_tema(tema):
    conn, cur = conectar()

    cur.execute("SELECT id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas FROM livros WHERE tema = %s;", (tema,))
    livros = []
    for id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas in cur.fetchall():
        livro_dict = {
            'id': id,
            'titulo': livro,
            'autor': autor,
            'serie': serie,
            'tema': tema,
            'faixa_etaria': faixa_etaria,
            'quantidade': quantidade,
            'avaliacao': avaliacao,
            'img_url': img_url,
            'curtidas': curtidas
        }
        livros.append(livro_dict)

    cur.close()
    conn.close()

    return jsonify(livros)

@app.route('/livros/faixa_etaria', methods=['GET'])
def listar_faixas_etarias():
    conn, cur = conectar()

    cur.execute("SELECT DISTINCT faixa_etaria FROM livros ORDER BY faixa_etaria;")
    faixas_etarias = [faixa[0] for faixa in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(faixas_etarias)


@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_por_id(id):
    conn, cur = conectar()

    livro_alterado = request.get_json()
    cur.execute("""
        UPDATE livros
        SET livro = %s, autor = %s, serie = %s, tema = %s, faixa_etaria = %s, quantidade = %s, avaliacao = %s, img_url = %s
        WHERE id = %s;
    """, (
        livro_alterado.get('livro'),
        livro_alterado.get('autor'),
        livro_alterado.get('serie'),
        livro_alterado.get('tema'),
        livro_alterado.get('faixa_etaria'),
        livro_alterado.get('quantidade'),
        livro_alterado.get('avaliacao'),
        livro_alterado.get('img_url'),
        id
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Livro atualizado com sucesso.'})


@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro_por_id(id):
    conn, cur = conectar()

    cur.execute("DELETE FROM livros WHERE id = %s;", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({'message': 'Livro excluído com sucesso.'})

@app.route('/livros/curtir/<int:id>', methods=['PUT'])
def atualizar_curtidas_livro(id):
    conn, cur = conectar()

    cur.execute("UPDATE livros SET curtidas = curtidas + 1 WHERE id = %s;", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({'message': 'Curtida atualizada com sucesso.'})


@app.route('/livros/descurtir/<int:id>', methods=['PUT'])
def diminuir_curtidas_livro(id):
    conn, cur = conectar()

    cur.execute("UPDATE livros SET curtidas = curtidas - 1 WHERE id = %s;", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({'message': 'Curtida diminuída com sucesso.'})

@app.route('/livros/mais_curtidas', methods=['GET'])
def obter_livros_mais_curtidas():
    conn, cur = conectar()

    cur.execute("SELECT id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas FROM livros ORDER BY curtidas DESC LIMIT 10;")
    livros = []
    for id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas in cur.fetchall():
        livro_dict = {
            'id': id,
            'titulo': livro,
            'autor': autor,
            'serie': serie,
            'tema': tema,
            'faixa_etaria': faixa_etaria,
            'quantidade': quantidade,
            'avaliacao': avaliacao,
            'img_url': img_url,
            'curtidas': curtidas
        }
        livros.append(livro_dict)

    cur.close()
    conn.close()

    return jsonify(livros)

@app.route('/livros/mais_curtidos', methods=['GET'])
def obter_livros_mais_curtidos_por_tema():
    tema = request.args.get('tema')

    conn, cur = conectar()

    cur.execute("""
        SELECT id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas
        FROM books.livros
        WHERE tema = %s
        ORDER BY curtidas DESC
        LIMIT 10;
    """, (tema,))

    livros = []
    for id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas in cur.fetchall():
        livro_dict = {
            'id': id,
            'titulo': livro,
            'autor': autor,
            'serie': serie,
            'tema': tema,
            'faixa_etaria': faixa_etaria,
            'quantidade': quantidade,
            'avaliacao': avaliacao,
            'img_url': img_url,
            'curtidas': curtidas
        }
        livros.append(livro_dict)

    cur.close()
    conn.close()

    return jsonify(livros)

def criar_dataframe():
    conn, cur = conectar()

    cur.execute("SELECT * FROM livros")
    livros = cur.fetchall()

    # Colunas do DataFrame
    colunas = ['id', 'titulo', 'autor', 'serie', 'tema', 'faixa_etaria', 'quantidade', 'avaliacao', 'img_url', 'curtidas']

    # Criar DataFrame a partir dos dados do banco de dados
    df = pd.DataFrame(livros, columns=colunas)

    cur.close()
    conn.close()

    return df

@app.route('/recomendacoes', methods=['GET'])
def recomendar_livros_api():
    conn, cur = conectar()

    # Obter as classificações médias dos livros
    cur.execute("SELECT livro, AVG(curtidas) AS media_curtidas FROM livros GROUP BY livro;")
    classificacoes = cur.fetchall()

    # Verificar se existem classificações
    if len(classificacoes) == 0:
        return "Não existem classificações."

    # Criar o DataFrame com as classificações médias
    df = pd.DataFrame(classificacoes, columns=['livro', 'media_curtidas'])

    # Ordenar os livros por média de curtidas
    df = df.sort_values(by='media_curtidas', ascending=False)

    # Obter os livros recomendados (top 5)
    livros_recomendados = df.head(5)

    # Obter informações completas dos livros recomendados
    livro_ids = tuple(livros_recomendados['livro'])
    cur.execute("SELECT id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas FROM livros WHERE livro IN (%s);" % ','.join(['%s']*len(livro_ids)), livro_ids)
    livros_recomendados_info = []
    for row in cur.fetchall():
        id, livro, autor, serie, tema, faixa_etaria, quantidade, img_url, avaliacao, curtidas = row
        livro_dict = {
            'id': id,
            'titulo': livro,
            'autor': autor,
            'serie': serie,
            'tema': tema,
            'faixa_etaria': faixa_etaria,
            'quantidade': quantidade,
            'avaliacao': avaliacao,
            'img_url': img_url,
            'curtidas': curtidas
        }
        livros_recomendados_info.append(livro_dict)

    cur.close()
    conn.close()

    return jsonify(livros_recomendados_info)

@app.route('/autores-curtidos', methods=['GET'])
def autores_curtidos_api():
    df = criar_dataframe()

    # Análise dos autores mais curtidos
    autores_curtidas = df.groupby('autor')['curtidas'].sum().reset_index()
    autores_curtidas = autores_curtidas.sort_values('curtidas', ascending=False)
    autores_top_10 = autores_curtidas.head(10)

    # Obter informações dos livros dos autores top 10
    livros_autores_top_10 = df[df['autor'].isin(autores_top_10['autor'])]

    # Converter para o formato JSON
    livros_autores_top_10_json = livros_autores_top_10.to_dict(orient='records')

    return jsonify(livros_autores_top_10_json)

# Buscar os livros mais curtidos por faixa etária
@app.route('/livros/curtidas_por_faixa_etaria', methods=['GET'])
def obter_livros_curtidos_por_faixa_etaria():
    df = criar_dataframe()
    faixas_etarias = df['faixa_etaria'].unique().tolist()

    livros_curtidos_por_faixa_etaria = {}
    for faixa_etaria in faixas_etarias:
        livros_filtrados = df[df['faixa_etaria'] == faixa_etaria]
        livros_filtrados = livros_filtrados.sort_values(by='curtidas', ascending=False)
        livros_filtrados = livros_filtrados.head(5)

        livros_curtidos_por_faixa_etaria[faixa_etaria] = livros_filtrados.to_dict('records')

    return jsonify(livros_curtidos_por_faixa_etaria)

if __name__ == '__main__':
    df = criar_dataframe()
    app.run()





