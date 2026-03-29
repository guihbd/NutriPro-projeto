import requests

def buscar_produtos_off(termo_busca, limite=5):
    """
    Busca produtos na Open Food Facts Brasil.
    Retorna uma lista de dicionários formatados para o NutriPro.
    """
    
    # Endpoint de busca da OFF
    url = "https://br.openfoodfacts.org/cgi/search.pl"
    
    # Configuração dos parâmetros de busca
    params = {
        "search_terms": termo_busca,
        "search_simple": 1,
        "action": "process",
        "json": 1,            # Queremos a resposta em JSON
        "page_size": limite,  # Quantidade de resultados
        # 'fields' filtra apenas o que nos interessa (economiza banda e processamento)
        "fields": "product_name,brands,code,nutriments,image_front_small_url,nutriscore_grade"
    }

    # IDENTIFICAÇÃO OBRIGATÓRIA (Troque pelo seu e-mail/nome)
    headers = {
        'User-Agent': 'NutriPro - Web App - Estudante Engenharia FSA - guihbd@example.com'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status() # Levanta erro se a API cair
        data = response.json()
        
        produtos_formatados = []
        
        for p in data.get('products', []):
            nutri = p.get('nutriments', {})
            
            # Criamos um dicionário limpo para o seu MySQL/Front-end
            item = {
                "nome": p.get('product_name', 'Produto sem nome'),
                "marca": p.get('brands', 'Marca desconhecida'),
                "kcal_100g": nutri.get('energy-kcal_100g', 0),
                "proteina_100g": nutri.get('proteins_100g', 0),
                "carbo_100g": nutri.get('carbohydrates_100g', 0),
                "gordura_100g": nutri.get('fat_100g', 0),
                "sodio_100g": nutri.get('sodium_100g', 0),
                "nota": p.get('nutriscore_grade', 'N/A').upper(),
                "img": p.get('image_front_small_url', '')
            }
            produtos_formatados.append(item)
            
        return produtos_formatados

    except Exception as e:
        print(f"Erro na conexão: {e}")
        return []

# --- TESTE DO SCRIPT ---
if __name__ == "__main__":
    termo = input("Digite um produto para buscar (ex: Iogurte Grego): ")
    resultados = buscar_produtos_off(termo)
    
    for i, res in enumerate(resultados, 1):
        print(f"\n[{i}] {res['nome']} ({res['marca']})")
        print(f"    Kcal: {res['kcal_100g']} | Prot: {res['proteina_100g']}g | Nota: {res['nota']}")