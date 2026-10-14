from playwright.sync_api import sync_playwright


# =====================================
# ABRIR REPLICADOR
# =====================================

def abrir_replicador(page):

    try:

        print(
            "\nAbrindo tela do replicador..."
        )

        page.goto(
            "https://novacentral.fretebras.com.br/meus-fretes/cadastrar",
            wait_until="domcontentloaded",
            timeout=120000
        )

        page.wait_for_timeout(3000)

        print(
            "Tela aberta com sucesso!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao abrir tela:"
        )

        print(erro)

        return False
    
# =====================================
# PREENCHER ORIGEM
# =====================================
def preencher_origem(
    page,
    frete
):

    try:

        origem = frete["origem"]

        print(
            f"\nPreenchendo origem: "
            f"{origem}"
        )

        campo_origem = page.locator(
            'input[role="combobox"][aria-controls="stop-suggestions-pickup-1"]'
        )

        campo_origem.wait_for(
            state="visible",
            timeout=10000
        )

        campo_origem.scroll_into_view_if_needed()

        campo_origem.click()

        page.wait_for_timeout(1000)

        campo_origem.fill(
            origem
        )

        page.wait_for_timeout(2000)

        # Seleciona a sugestão exibida
        page.keyboard.press(
            "ArrowDown"
        )

        page.wait_for_timeout(500)

        page.keyboard.press(
            "Enter"
        )

        page.wait_for_timeout(1000)

        print(
            "Origem preenchida!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao preencher origem:"
        )

        print(erro)

        return False

# =====================================
# PREENCHER DESTINO
# =====================================

def preencher_destino(
    page,
    frete
):

    # =====================================
    # DESTINOS POR ESTADO
    # =====================================

    DESTINOS_POR_ESTADO = {
        "SC": "Laurentino, SC",
        "PR": "Curitiba, PR",
        "RS": "Nova Petrópolis, RS",
        "SP": "Ribeirão Preto, SP",
        "GO": "Goiânia, GO",
        "MT": "Cuiabá, MT",
        "MS": "Campo Grande, MS",
        "MG": "Uberlândia, MG",
        "BA": "Feira de Santana, BA",
        "PE": "São Bento do Una, PE",
        "ES": "Santa Maria de Jetibá, ES",
        "TO": "Palmas, TO",
        "RO": "Vilhena, RO",
        "PA": "Redenção, PA",
        "MA": "Balsas, MA",
        "PI": "Uruçuí, PI",
        "CE": "Fortaleza, CE",
        "RN": "Mossoró, RN",
        "PB": "Campina Grande, PB",
        "AL": "Arapiraca, AL",
        "SE": "Itabaiana, SE",
        "RJ": "Campos dos Goytacazes, RJ",
        "AC": "Rio Branco, AC",
        "AM": "Manaus, AM",
        "AP": "Macapá, AP",
        "RR": "Boa Vista, RR",
        "DF": "Brasília, DF"
    }

    try:

        # =====================================
        # IDENTIFICAR ESTADO DE DESTINO
        # =====================================

        estado_destino = frete["estado_destino"].strip().upper()

        destino = DESTINOS_POR_ESTADO.get(
            estado_destino
        )

        if not destino:
            raise ValueError(
                f"Não existe destino cadastrado para o estado {estado_destino}"
            )

        print(f"\nEstado de destino: {estado_destino}")
        print(f"Cidade de destino: {destino}")

        # =====================================
        # LOCALIZAR CAMPO DE DESTINO
        # =====================================

        campo_destino = page.locator(
            'input[role="combobox"][aria-controls="stop-suggestions-delivery-1"]'
        )

        campo_destino.wait_for(
            state="visible",
            timeout=10000
        )

        campo_destino.scroll_into_view_if_needed()

        campo_destino.click()

        page.wait_for_timeout(1000)

        # =====================================
        # PREENCHER DESTINO
        # =====================================

        campo_destino.fill(destino)

        page.wait_for_timeout(2000)

        # =====================================
        # SELECIONAR SUGESTÃO
        # =====================================

        page.keyboard.press("ArrowDown")

        page.wait_for_timeout(500)

        page.keyboard.press("Enter")

        page.wait_for_timeout(1000)

        print("Destino preenchido com sucesso!")

        return True

    except Exception as erro:

        print("\nErro ao preencher destino:")
        print(erro)

        return False
    
# =====================================
# CLICAR NO BOTÃO HOJE
# =====================================

def clicar_hoje(page):

    try:

        botao_hoje = page.locator(
            'button[aria-label="Hoje"]'
        )

        botao_hoje.wait_for(
            state="visible",
            timeout=10000
        )

        botao_hoje.scroll_into_view_if_needed()

        botao_hoje.click()

        page.wait_for_timeout(1000)

        print(
            "Botão Hoje clicado!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao clicar no botão Hoje:"
        )

        print(erro)

        return False

# =====================================
# PREENCHER PRODUTO
# =====================================

def preencher_produto(
    page,
):

    try:

        campo_produto = page.locator(
            'label:has-text("Qual produto será carregado?")'
        ).locator(
            ".."
        ).locator(
            "input"
        )

        campo_produto.wait_for(
            state="visible",
            timeout=10000
        )

        campo_produto.scroll_into_view_if_needed()

        campo_produto.click()

        page.wait_for_timeout(500)

        campo_produto.fill(
            "Milho"
        )

        page.wait_for_timeout(1000)

        page.keyboard.press(
            "Tab"
        )

        page.wait_for_timeout(1500)

        print(
            "Produto preenchido!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao preencher produto:"
        )

        print(erro)

        return False

# =====================================
# PREENCHER CARGA
# =====================================

def preencher_carga(
    page
):

    try:

        campo_carga = page.locator(
            'label:has-text("Tipo da carga")'
        ).locator(
            ".."
        ).locator(
            "input"
        )

        campo_carga.wait_for(
            state="visible",
            timeout=10000
        )

        campo_carga.scroll_into_view_if_needed()

        campo_carga.click()

        page.wait_for_timeout(1000)

        page.get_by_text(
            "Granel sólido",
            exact=True
        ).click()

        page.wait_for_timeout(1000)

        print(
            "Carga preenchida!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao preencher carga:"
        )

        print(erro)

        return False

# =====================================
# SELECIONAR CARGA COMPLETA
# =====================================

def selecionar_carga_completa(
    page
):

    try:

        botao_carga_completa = page.get_by_text(
            "Carga completa",
            exact=True
        )

        botao_carga_completa.wait_for(
            state="visible",
            timeout=10000
        )

        botao_carga_completa.scroll_into_view_if_needed()

        botao_carga_completa.click()

        page.wait_for_timeout(1000)

        print(
            "Carga completa selecionada!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao selecionar carga completa:"
        )

        print(erro)

        return False

# =====================================
# SELECIONAR CAPACIDADE DO VEÍCULO
# =====================================

def selecionar_capacidade_veiculo(
    page
):

    try:

        botao_capacidade = page.get_by_text(
            "Conforme capacidade do veículo",
            exact=True
        )

        botao_capacidade.wait_for(
            state="visible",
            timeout=10000
        )

        botao_capacidade.scroll_into_view_if_needed()

        botao_capacidade.click()

        page.wait_for_timeout(1000)

        print(
            "Capacidade do veículo selecionada!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao selecionar capacidade do veículo:"
        )

        print(erro)

        return False
    
# =====================================
# SELECIONAR TODOS OS PESADOS
# =====================================

def preencher_caminhao(
    page
):

    try:

        botao_pesados = page.get_by_text(
            "Selecionar todos pesados",
            exact=True
        )

        botao_pesados.wait_for(
            state="visible",
            timeout=10000
        )

        botao_pesados.scroll_into_view_if_needed()

        botao_pesados.click()

        page.wait_for_timeout(2000)

        print(
            "Todos os pesados selecionados!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao selecionar todos os pesados:"
        )

        print(erro)

        return False
              

# =====================================
# PREENCHER CARROCERIA
# =====================================

def preencher_carroceria(
    page
):

    try:

        # Seleciona Caçamba
        botao_cacamba = page.locator(
            'button[aria-label="Caçamba"]'
        )

        botao_cacamba.wait_for(
            state="visible",
            timeout=10000
        )

        botao_cacamba.click()

        page.wait_for_timeout(1000)

        # Seleciona Graneleiro
        botao_graneleiro = page.locator(
            'button[aria-label="Graneleiro"]'
        )

        botao_graneleiro.wait_for(
            state="visible",
            timeout=10000
        )

        botao_graneleiro.click()

        page.wait_for_timeout(1000)

        print(
            "Carrocerias selecionadas!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao preencher carroceria:"
        )

        print(erro)

        return False

# =====================================
# PREENCHER PAGAMENTO
# =====================================

def preencher_pagamento(
    page
):

    try:

        botao_pagamento = page.get_by_text(
            "A combinar",
            exact=True
        )

        botao_pagamento.wait_for(
            state="visible",
            timeout=10000
        )

        botao_pagamento.scroll_into_view_if_needed()

        botao_pagamento.click()

        page.wait_for_timeout(2000)

        print(
            "Pagamento selecionado!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao preencher pagamento:"
        )

        print(erro)

        return False
def selecionar_percentual(page):

    try:

        # Abre a lista de percentual
        campo_percentual = page.locator(
            'input[role="combobox"][aria-haspopup="listbox"][readonly]'
        ).filter(
            has_not=page.locator('[aria-label]')
        ).last

        campo_percentual.wait_for(
            state="visible",
            timeout=10000
        )

        campo_percentual.scroll_into_view_if_needed()
        campo_percentual.click()

        page.wait_for_timeout(1000)

        # Seleciona 70%
        opcao_70 = page.get_by_text(
            "70%",
            exact=True
        )

        opcao_70.wait_for(
            state="visible",
            timeout=10000
        )

        opcao_70.click()

        page.wait_for_timeout(1000)

        # Seleciona PIX
        page.get_by_text(
            "Pix",
            exact=True
        ).click()

        page.wait_for_timeout(1000)

        print("Percentual 70% e PIX selecionados!")

        return True

    except Exception as erro:

        print("\nErro ao selecionar percentual:")
        print(erro)

        return False
# =====================================
# PREENCHER FINAL
# =====================================

def preencher_final(
    page
):

    try:

        campo_final = page.locator(
            '[role="button"][aria-label="Frete Simples, Exposição padrão"]'
        )

        campo_final.wait_for(
            state="visible",
            timeout=10000
        )

        campo_final.scroll_into_view_if_needed()

        campo_final.click()

        page.wait_for_timeout(2000)

        print(
            "Frete Simples selecionado!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao preencher final:"
        )

        print(erro)

        return False

# =====================================
# PUBLICAR FRETE
# =====================================

def preencher_publicar(
    page
):

    try:

        botao_publicar = page.locator(
            'button[aria-label="Publicar Frete"]'
        )

        botao_publicar.wait_for(
            state="visible",
            timeout=10000
        )

        botao_publicar.scroll_into_view_if_needed()

        botao_publicar.click()

        page.wait_for_timeout(10000)

        print(
            "Frete publicado!"
        )

        return True

    except Exception as erro:

        print(
            "\nErro ao publicar:"
        )

        print(erro)

        return False