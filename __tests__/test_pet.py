# 1 - Bibliotecas
import json             # leitor e escritor de arquivos json
import pytest           # engine  framework de teste de unidade
import requests         # framework de teste de API

from utils.utils import ler_csv     # importar a função de leitura do csv

# 2 - Classe (opcionla no Python, em muitos casos)

# 2.1 - Atributos ou variantes
# consulta e resultado esperado
pet_id = 30488454           # código do animal
pet_name = "Lagertha"       # nome do animal
pet_category_id = 1         # código da categoria do animal
pet_category_name = "cat"   # título da categoria
pet_tag_id = 1              # código do rótulo
pet_tag_name = "vacinado"   # título do rótulo


# infos em comum
url = 'https://petstore.swagger.io/v2/pet'          # endereço
headers = { 'Content-Type': 'application/json' }    # formato dos dados trafegados

# 2.2 - Funções / Métodos

def test_post_pet():
    # configura
    # dados de entrada estão no arquivo json
    pet=open('./fixtures/json/pet1.json')     # abre o arquivo json
    data=json.loads(pet.read())               # let o conteúdo e carrega como json em uma variavel data
    # dados de saída / resultado esperado estão nos atributos acima das funções

    # executa
    response = requests.post(           # executa o método post com as infos a seguir
        url=url,                        # endereço
        headers=headers,                # cabeçalho / informações extras
        data=json.dumps(data),          # a mensagem = json
        timeout=5                       # tempo limite da transmissão, em segundos
    )
   
    # valida
    response_body = response.json()     # cria uma variável e carrega a resposta em formato json
    
    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['name'] == pet_tag_name

def test_get_pet():
    # configura
    # dados de entrada e saida / resultado esperado estão na seção de atributos antes das funções

    # executa
    response = requests.get(
        url=f'{url}/{pet_id}',  # chama o endereço do get / consulta passando o código do animal
        headers=headers
        # não tem corpo da mensagem / body

    )
        

    # valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['status'] == 'available'


def test_put_pet():
    # configura
    # dados de entrada estão no arquivo json
    pet=open('./fixtures/json/pet2.json')     # abre o arquivo json
    data = json.loads(pet.read())
    # dados de saída / resultado esperado vem dos atributos descritos antes das funçoes

    # executa
    response = requests.put(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=5
    )

    # valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name

    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['name'] == pet_tag_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['status'] == 'sold'


def test_delete_pet():
    # configura
    # dados de entrada virão dos atributos

    # executa
    response = requests.delete(
        url=f'{url}/{pet_id}',
        headers=headers
    )

    # valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(pet_id)



@pytest.mark.parametrize('pet_id,category_id,category_name,pet_name,tags,status',
                         ler_csv('./fixtures/csv/pets.csv'))
def test_post_pet_dinamico(pet_id,category_id,category_name,pet_name,tags,status):
    # configura

    pet = {}        # criando uma lista vazia chamada pet
    pet['id'] = int(pet_id)
    pet['category'] = {}
    pet['category']['id'] = int(category_id)
    pet['category']['name'] = category_name
    pet['name'] = pet_name
    pet['photoUrls'] = []
    pet['photoUrls'].append('')
    pet['tags'] = []

    tags = tags.split(';')
    for tag in tags:
        tag = tag.split('-')
        tag_formatada = {}
        tag_formatada['id'] = int(tag[0])
        tag_formatada['name'] = tag[1]
        pet['tags'].append(tag_formatada)

        pet['status'] = status

        pet = json.dumps(obj=pet, indent=4)
        print('\n' + pet)   # visualiza como ficou o json criado dinamicamente

        # executa
        response = requests.post(
            url=url,
            headers=headers,
            data=pet,
            timeout=5
    
        )

        # valida
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['id'] == int(pet_id)
        assert response_body['name'] == pet_name
        assert response_body['status'] == status




