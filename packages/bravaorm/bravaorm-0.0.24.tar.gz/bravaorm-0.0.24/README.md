




# Brava ORM para MySQL/MariaDB

SDK fornece uma série de recursos para aumentar produtividade no desenvolvimento de aplicações com integração a banco de dados relacional MySql/MariaDB.

# Instalação

Instalação utilizando Pip

```bash
pip install bravaorm
```

Git/Clone
```
git clone https://github.com/robertons/bravaorm
cd bravaorm
pip install -r requirements.txt
python setup.py install
```


## Dados de Entrada

| entrada     | default |    tipo     | obrigatório |                  |
|-------------|---------|-------------|-------------|------------------|
| db_user     | None    | string      | sim         | Nome Usuário     |
| db_password | None    | string      | sim         | Senha Usuario    |
| db_host     | None    | string      | sim         | Host             |
| db_port     | None    | string      | sim         | Porta            |
| db_database | None    | string      | sim         | Nome DB          |
| db_ssl      | False   | boolean     | não         | Conexão Segura   |
| db_ssl_ca   | None    | string      | não         | Certificado CA   |
| db_ssl_cert | None    | string      | não         | Certificado      |
| db_ssl_key  | None    | string      | não         | Chave Certificado|
| db_charset  | utf8    | string      | não         | Charset DB       |
| log_level   | error   | string      | não         | Nível log        |

##  Saída

| método       | aplicável 		    |    resultado 					  			
|--------------|--------------------|--------------------------------------------
| first    	   |  Conexão           | objeto de um select     
| all    	   |  Conexão           | lista de objetos de um select|
| fetch   	   |  Conexão           | lista  de um select sem conversão em objeto
| delete(*obj*)| Conexão    		| exclui um objeto
| save()  	   | Conexão    		| salva operações no db
| add(*obj*)   | Objeto, Conexão    | adiciona objeto a uma lista/tabela
| ToJSON()     | Objeto, Conexão    | resultado em formato dict


## Conexão com Banco de dados

```python
import bravaorm

conn = bravaorm.Connection(db_user="root", db_password="pass", db_host="host", db_port=3306, db_database="dbmae", db_charset="utf8mb4")

```

## Gerando Modelo de Entidade

```python

import os
import bravaorm

bravaorm.Make(dir = os.path.dirname(os.path.abspath(__file__)), db_user="user", db_password="pass", db_host="host", db_port=3306, db_database="dbname")

```

> O script acima irá gerar na raiz do projeto as classes objetos baseados no Banco de Dados. As tabelas do banco dedos devem seguir os requisitos de pluralização, conforme exemplo abaixo:

```bash
.
├── ...
├── model                           # Raiz Entidade
│   ├── __init__.py          
│   ├── categoria.py               # Classe Categoria | Tabela categorias
│   ├── cliente.py                 # Classe Cliente  	| Tabela clientes
│   └── compra.py                  # Classe Compra  	| Tabela compras
│   └── produto.py                 # Classe Produto  	| Tabela produtos
└── ...
```

Tomando como exemplo a tabela produtos, a classe gerada estará assim:

```python
# -*- coding: utf-8 -*-
from bravaorm.entity import *

class Produto(Entity):

	def __init__(cls, **kw):
		cls.__metadata__ = {'pk': ['id']}

		cls.id = Int(pk=True, auto_increment=True, not_null=True, precision=10, scale=0)
		cls.id_categoria = Int(fk=True, not_null=True, precision=10, scale=0)
		cls.prod_nome = String(max=155)
		cls.prod_preco = Decimal(not_null=True, precision=19, scale=2)
		cls.prod_data_fabricacao = DateTime(format='%d/%m/%Y')
		cls.prod_data_modificacao = DateTime(format='%d/%m/%Y HH:MM:SS')

		# One-to-One
		cls.categorias = Obj(context=cls, keyname='categorias', name='Categoria', key='id', reference='id_categoria', table='categorias')

		# One-to-many
		cls.compras = ObjList(context=cls, keyname='compras',name='Compra', key='id_compra', reference='id', table='compras')

		super().__init__(**kw)
```


# Seleção de Objetos e Condições

```python
produto = conn.produtos.where("id=10").first
print(produto)
print(produto.toJSON())
```

**> <model.produto.Produto object at 0x101237c10>**

**> {'id': 10, 'id_categoria': 10, 'prod_nome': 'Exemplo', 'prod_preco':  Decimal('99.90'), 'prod_data_fabricacao': datetime(2010, 12, 10, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 03, 31, 16, 54, 22)}**

# Condição 'Ou'

A condição orwhere é dependente de condição where, e cria novos blocos a cada utilização.

```python
produtos = conn.produtos.where("id=10").orwhere("id=12").orwhere("id=14").all
print(produtos.toJSON())
```
**> [{'id': 10, 'id_categoria': 10,  'prod_nome': 'Exemplo', 'prod_preco':  Decimal('99.90'), 'prod_data_fabricacao': datetime(2010, 12, 10, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 03, 31, 16, 54, 22)}, {'id': 12, 'prod_nome': 'Outro Exemplo ', 'prod_preco':  Decimal('88,20'), 'prod_data_fabricacao': datetime(2011, 10, 8, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 02, 12, 10, 24, 20)}, {'id': 14, 'prod_nome': 'Novo Exemplo', 'prod_preco':  Decimal('129,90'), 'prod_data_fabricacao': datetime(2009, 11, 7, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 01, 10, 14, 34, 15)}]**

# Seleção de Campos
```python
produto = conn.produtos.where("id=10").select("id, prod_nome").first
print(produto.toJSON())
```
**> {'id': 10, 'prod_nome': 'Exemplo'}**

# Alias de Funções ou Campos
```python
produto = conn.produtos.alias('prod_nome','nome').where("id=10").first
print(produto['nome'])
print(produto.prod_nome)
```
**> Exemplo**
**> Exemplo**

*Alias são campos não editáveis*

# Ordenamento


```python
# ORDERBY
produto = conn.produtos.orderby("prod_nome").all
produto = conn.produtos.orderby("prod_nome DESC").all

```
# Agrupamento

```python
# GROUPBY
produto = conn.produtos.groupby("id_categoria").all
```

# Limite

```python
# LIMIT
produto = conn.produtos.orderby("prod_nome").limit(0,10).all

```

# União de Objetos

O métodos "join" e "inner" são recomendados para uso de objetos com relacionamento "um para um",  ou em casos onde o resultado da tabela secundária irá retornar apenas **um resultado.** A utilização desses métodos em casos de seleção "um para vários" o resultado será baseado na tabela secundária, podendo ocorrer a repetição do objeto principal. Neste neste caso é recomendável a utilização do método "include" onde o resultado da lista será com objetos únicos incluindo os vários resultados da tabela secundária.

**Exemplos:**

## Join

O método join, é equivalente ao "LEFT JOIN" e retorna o objeto principal incluindo a seleção secundária, de duas tabelas.

```python
produto = conn.produtos.join("categegorias").all

```

**> {'id': 10, 'id_categoria': 10, 'prod_nome': 'Exemplo', 'prod_preco':  Decimal('99.90'), 'prod_data_fabricacao': datetime(2010, 12, 10, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 03, 31, 16, 54, 22), 'categorias': {'id':1, 'cat_nome':'Categoria Teste'}}**


## Inner

O método inner, é equivalente ao "INNER JOIN" e retorna o objeto principal baseado na interceção da tabela secundária.

```python
produto = conn.produtos.inner("categorias").where("categorias.id=1").all

```

**> [{'id': 10, 'id_categoria': 10, 'prod_nome': 'Exemplo', 'prod_preco':  Decimal('99.90'), 'prod_data_fabricacao': datetime(2010, 12, 10, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 03, 31, 16, 54, 22), 'categorias': {'id':1, 'cat_nome':'Categoria Teste'}}, {'id': 12, 'prod_nome': 'Outro Exemplo ', 'prod_preco':  Decimal('88,20'), 'prod_data_fabricacao': datetime(2011, 10, 8, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 02, 12, 10, 24, 20), 'categorias': {'id':1, 'cat_nome':'Categoria Teste'}}, {'id': 14, 'prod_nome': 'Novo Exemplo', 'prod_preco':  Decimal('129,90'), 'prod_data_fabricacao': datetime(2009, 11, 7, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 01, 10, 14, 34, 15), 'categorias': {'id':1, 'cat_nome':'Categoria Teste'}}]**

## Include

O método include, faz seleção de um ou vários objetos relacionados ao objeto principal, recomendado para relacionamento um para vários.

*este método requer atenção em relação a performance para grandes seleções*

```python
produto = conn.produtos.include("compras").where("id=10, compras.compra_paga=1").all

```

**> [{'id': 10, 'id_categoria': 10, 'prod_nome': 'Exemplo', 'prod_preco':  Decimal('99.90'), 'prod_data_fabricacao': datetime(2010, 12, 10, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 03, 31, 16, 54, 22), 'compras': [{'id':1, 'compra_data':datetime(2010, 12, 10, 0, 0, 0), 'id_cliente':12}, {'id':23, 'compra_data':datetime(2017, 11, 13, 0, 0, 0), 'id_cliente':54}, {'id':34, 'compra_data':datetime(2018, 1 11, 0, 0, 0), 'id_cliente':20}, {'id':110, 'compra_data':datetime(2019, 7, 22, 0, 0, 0), 'id_cliente':16}]}]**

#  Fetch

O método fetch  permite o obter a resposta direta do DB em formato dict a partir de um select, sem a conversão dos dados em classe/objeto. Este método oferece ganho significativo de performance.

```python
# GROUPBY
produtos = conn.produtos.fetch

```

**> [{'id': 10, 'prod_nome': 'Exemplo', 'prod_preco':  Decimal('99.90'), 'prod_data_fabricacao': datetime(2010, 12, 10, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 03, 31, 16, 54, 22)}, {'id': 12, 'prod_nome': 'Outro Exemplo ', 'prod_preco':  Decimal('88,20'), 'prod_data_fabricacao': datetime(2011, 10, 8, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 02, 12, 10, 24, 20)}, {'id': 14, 'prod_nome': 'Novo Exemplo', 'prod_preco':  Decimal('129,90'), 'prod_data_fabricacao': datetime(2009, 11, 7, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 01, 10, 14, 34, 15)}]**

## Método toJSON()

O metodo toJSON() retorna o objeto ou lista de resultado em formato dict.

```python
	print(produto)
	print(produto.toJSON())
```
**> <model.produto.Produto object at 0x107737c10>**

**> {'id': 10, 'prod_nome': 'Exemplo', 'prod_preco':  Decimal('99.90'), 'prod_data_fabricacao': datetime(2010, 12, 10, 0, 0, 0), 'prod_data_modificacao': 'datetime(2021, 03, 31, 16, 54, 22)}**


# Criação de Objetos
## Simples
```python
from model import *

produto = Produto()
produto.prod_nome = 'Exemplo'
produto.prod_preco = Decimal('99.90')
produto.prod_data_fabricacao = datetime(2010, 12, 10, 0, 0, 0)
produto.prod_data_modificacao = '31/03/2021 16:54:22' # Conversão para datetime seguindo formato '%d/%m/%Y HH:MM:SS'

conn.add(produto)
conn.save()

```

**OU**

```python
from model import *

produto = Produto(prod_nome='Exemplo', prod_preco=Decimal('99.90'), prod_data_fabricacao = datetime(2010, 12, 10, 0, 0, 0), prod_data_modificacao = '31/03/2021 16:54:22')

conn.add(produto)
conn.save()
```

**OU**

```python
from model import *

produto = Produto(**{prod_nome:'Exemplo', prod_preco:Decimal('99.90'), prod_data_fabricacao:datetime(2010, 12, 10, 0, 0, 0), prod_data_modificacao :'31/03/2021 16:54:22'})

conn.add(produto)
conn.save()
```

## Com Relacionamentos

No exemplo abaixo, criamos um produto na tabela *produtos* com 3 fotos na tabela *produtos_fotos*

```python
from model import *

produto = Produto()
produto.prod_nome = 'Exemplo'
produto.prod_preco = Decimal('99.90')
produto.prod_data_fabricacao = datetime(2010, 12, 10, 0, 0, 0)
produto.prod_data_modificacao = '31/03/2021 16:54:22' # Conversão para datetime seguindo formato '%d/%m/%Y HH:MM:SS'

foto = ProdutoFoto()
foto.foto_descricao = 'Vista Frontal'
foto.foto_arquivo =  'fronta.jpg'
produto.produtos_fotos.add(foto)

foto = ProdutoFoto(**{foto_descricao:'Vista Lateral', foto_arquivo:'lateral.jpg'})
produto.produtos_fotos.add(foto)

produto.produtos_fotos.add(ProdutoFoto(foto_descricao='Vista Lateral', foto_arquivo='lateral.jpg'))

conn.add(produto)
conn.save()

```

# Atualizando Objeto

```python
produto = conn.produtos.where("id=10").first
produto.prod_preco = Decimal(89.90)
conn.add(produto).save()
```
**ou vários**

```python
produtos = db.produtos.where("prod_preco>=100").all
for produto in produtos:
	produto.prod_preco = produto.prod_preco * 0.9
	conn.add(produto)
db.save()
```

**ou relativos**

```python
categoria = db.categorias.include("produtos").where("id=1, produtos.pro_preco>=100").all
for produto in categoria.produtos:
	produto.prod_preco = produto.prod_preco * 0.9
	conn.add(produto)
db.save()
```

# Exclusão de Objetos

O método requer um objeto de entrada, ou uma condição where definida:

```python
conn.delete(produto).save()
```
ou condicional

```python
conn.produtos.where("prod_preco=100").delete()
```

# Contador

```python
quantidade_produtos = conn.produtos.where("prod_preco=100").count

print(quantidade_produtos)
```

**> 113 **

# Execute Query

É possível executar queries mais complexas e com condicionais específicas, nesse caso é possível escrever a query diretamente na conexão e informar qual o tipo de objeto será retornado a partir dela.

A definição do objeto é opcional.



```python
produtos = conn.execute("SELECT * FROM produtos WHERE preco > 100", "Produto")
```

A consulta acima irá retornar uma lista de  objetos *Produto*


```python
produtos = conn.execute("SELECT * FROM produtos WHERE preco > 100")
```

A consulta acima irá retornar uma lista com dictionary  com dados de produtos



## License

MIT

Copyright (c) 2019-2021 Roberto Neves. All rights reserved. info (at) robertonsilva@gmail.com
