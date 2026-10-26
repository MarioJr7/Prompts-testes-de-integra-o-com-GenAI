"""Testes de integração do CRUD de usuários (casos derivados de cenarios-integracao.md)."""
import json, os
from datetime import date, timedelta
import pytest, requests

BASE = os.getenv("BASE_URL", "http://localhost:8000")
URL = f"{BASE}/usuarios"
CAMINHO = os.path.join(os.path.dirname(__file__), "..", "casos-de-teste", "dados-teste.json")
DADOS = json.load(open(CAMINHO, encoding="utf-8"))
VALIDO = DADOS["validos"][0]["payload"]


def novo(payload=None):
    return requests.post(URL, json=payload or VALIDO)


@pytest.fixture(autouse=True)
def limpar():
    yield
    for u in requests.get(URL).json():
        requests.delete(f"{URL}/{u['id']}")


def test_it01_it02_cria_e_persiste():                      # IT-01, IT-02
    r = novo(); assert r.status_code == 201
    uid = r.json()["id"]
    g = requests.get(f"{URL}/{uid}"); assert g.status_code == 200
    assert g.json()["endereco"] == VALIDO["endereco"] and g.json()["nome"] == VALIDO["nome"]


def test_it03_fluxo_completo():                            # IT-03
    uid = novo().json()["id"]
    alterado = {**VALIDO, "endereco": {**VALIDO["endereco"], "numero": "999"}}
    assert requests.put(f"{URL}/{uid}", json=alterado).status_code == 200
    assert requests.get(f"{URL}/{uid}").json()["endereco"]["numero"] == "999"
    assert requests.delete(f"{URL}/{uid}").status_code == 204
    assert requests.get(f"{URL}/{uid}").status_code == 404


def test_it04_cpf_duplicado():                             # IT-04
    novo(); assert novo().status_code == 409


def test_it05_cpf_mascara_equivale():                      # IT-05
    novo(); assert novo({**VALIDO, "cpf": "529.982.247-25"}).status_code == 409


@pytest.mark.parametrize("caso", DADOS["invalidos"], ids=lambda c: c["descricao"])
def test_it06_a_it12_validacoes(caso):                     # IT-06..IT-12
    assert novo(caso["payload"]).status_code == caso["status_esperado"]


@pytest.mark.parametrize("caso", DADOS["validos"], ids=lambda c: c["descricao"])
def test_dados_validos(caso):
    assert novo(caso["payload"]).status_code == 201


def test_it13_json_malformado():                           # IT-13
    r = requests.post(URL, data="{nome:", headers={"Content-Type": "application/json"})
    assert r.status_code == 400


def test_it09_it10_borda_idade():                          # IT-09, IT-10
    h = date.today()
    d18 = h.replace(year=h.year - 18)                      # (29/fev: ajustar se necessário)
    assert novo({**VALIDO, "dataNascimento": d18.isoformat()}).status_code == 201
    menor = (d18 + timedelta(days=1)).isoformat()          # 17 anos e 364 dias
    assert novo({**VALIDO, "cpf": "11144477735", "dataNascimento": menor}).status_code == 422


def test_it14_it16_inexistente():                          # IT-14, IT-16
    assert requests.get(f"{URL}/inexistente").status_code == 404
    assert requests.put(f"{URL}/inexistente", json=VALIDO).status_code == 404


def test_it15_atualizar_para_cpf_existente():              # IT-15
    novo(); outro = DADOS["validos"][1]["payload"]
    b = novo(outro).json()["id"]
    assert requests.put(f"{URL}/{b}", json={**outro, "cpf": VALIDO["cpf"]}).status_code == 409


def test_it17_excluir_duas_vezes():                        # IT-17
    uid = novo().json()["id"]
    assert requests.delete(f"{URL}/{uid}").status_code == 204
    assert requests.delete(f"{URL}/{uid}").status_code == 404


def test_it18_listagem_consistente():                      # IT-18
    a = novo().json()["id"]; b = novo(DADOS["validos"][1]["payload"]).json()["id"]
    ids = [u["id"] for u in requests.get(URL).json()]
    assert a in ids and b in ids
    requests.delete(f"{URL}/{a}")
    assert a not in [u["id"] for u in requests.get(URL).json()]


def test_it19_sql_injection_no_nome():                     # IT-19
    assert novo({**VALIDO, "nome": "'; DROP TABLE usuarios;--"}).status_code in (201, 422)
    assert requests.get(URL).status_code == 200            # tabela segue íntegra


def test_it20_utf8_integro():                              # IT-20
    p = DADOS["validos"][1]["payload"]
    uid = novo(p).json()["id"]
    assert requests.get(f"{URL}/{uid}").json()["nome"] == p["nome"]
