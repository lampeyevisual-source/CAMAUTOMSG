from fretebrascopy import abrir_fretebras, capturar_fretes
from replicador import (
    abrir_replicador,
    preencher_origem,
    preencher_destino,
    clicar_negociador,
    preencher_produto,
    preencher_carga,
    preencher_lote,
    preencher_caminhao,
    preencher_carroceria,
    preencher_pagamento,
    preencher_final,
    preencher_publicar
)
from mensagem import(
    contar_motoristas,
    selecionar_todos_motoristas,
    abrir_chat_envio,
    enviar_chat_compartilhar
    
)

from fretebras2 import(
analisar_cards,
    
)
import os
import random
import time
import re
import unicodedata
import subprocess
import sys

# =========================
# PASTA / ARQUIVO
# =========================

PASTA_DATA = "data"

ARQUIVO_PROCESSADOS = (
    f"{PASTA_DATA}/processados.txt"
)

os.makedirs(
    PASTA_DATA,
    exist_ok=True
)

# =========================
# TIMER
# =========================

def iniciar_timer():

    return time.time()


def finalizar_timer(
    nome_acao,
    inicio
):

    tempo = round(
        time.time() - inicio,
        2
    )

    print(
        f"[TEMPO] {nome_acao}: {tempo}s"
    )

# =========================
# CARREGA PROCESSADOS
# =========================

def carregar_processados():

    try:

        with open(
            ARQUIVO_PROCESSADOS,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return set(

                linha.strip()

                for linha in arquivo.readlines()

            )

    except:

        return set()

# =========================
# SALVA PROCESSADO
# =========================
def salvar_processado(frete_id):

    with open(
        ARQUIVO_PROCESSADOS,
        "a",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(f"{frete_id}\n")
        arquivo.flush()
        os.fsync(arquivo.fileno())

# =========================
# USUÁRIO
# =========================

def abrir_login(page):

    campo_usuario = page.locator(
        "#username"
    )

    campo_usuario.wait_for(
        state="visible",
        timeout=4000
    )

    campo_usuario.click()

    campo_usuario.fill(
        "contact.camgroup@gmail.com"
    )

    print(
        "Usuário preenchido."
    )

    # =========================
    # SENHA
    # =========================

    campo_senha = page.locator(
        "#password"
    )

    campo_senha.wait_for(
        state="visible",
        timeout=4000
    )

    campo_senha.click()

    campo_senha.fill(
        "Lhm@4856"
    )

    print(
        "Senha preenchida."
    )

    # =========================
    # SENHA
    # =========================

    campo_entrar = page.locator(
        "#kc-content-wrapper > div > section > div > div > form > button > span.fuel-button__content"
    )

    campo_entrar.wait_for(
        state="visible",
        timeout=4000
    )

    campo_entrar.click()

    print(
        "Acesso Iniciado."
    )

    page.wait_for_timeout(40000)

# =========================
# CIDADES
# =========================

entrada_cidades = input(
    "\nDigite as cidades que deseja anunciar, separadas por ';'\n"
    "Exemplo: Diamantino MT; Uberlândia MG; Rondonópolis MT\n\n"
    "Cidades: "
).strip()

cidades = []

for cidade in entrada_cidades.split(";"):
    cidade = cidade.strip()

    if not cidade:
        continue

    partes = cidade.rsplit(" ", 1)

    if len(partes) != 2:
        print(f"Formato inválido: {cidade}")
        print("Use: Cidade UF")
        continue

    nome_cidade = partes[0].strip().lower()
    estado = partes[1].strip().lower()

    nome_cidade_url = nome_cidade.replace(" ", "-")

    cidades.append({
        "cidade": nome_cidade,
        "estado": estado,
        "cidade_url": nome_cidade_url
    })
print("\nCidades selecionadas:")

for item in cidades:
    print(f"- {item['cidade'].title()} / {item['estado'].upper()}")


# =====================================
# CAPTURAR FRETE
# =====================================

def capturar_fretes(
    page,
    indice_card,
    nome_cidade,
    processados, processados_sequencia
):

    print("\nClassificando fretes...")


    while True:

        # =====================================
        # CAPTURA DOS CARDS
        # =====================================

        print("\nCapturando cards...")

        cards = page.locator("section").all()

        print(f"\nFretes encontrados: {len(cards)}")

        # =====================================
        # VERIFICA LIMITE
        # =====================================

        if indice_card >= len(cards):

            return None, indice_card, "FIM_CARDS",processados_sequencia

        try:

            card = cards[indice_card]

            cidades = card.locator(
                "h2"
            ).all_text_contents()

            print("\n====================")

            if len(cidades) >= 2:

                origem = cidades[0].strip()

                destino = cidades[1].strip()

                print(
                    "Origem:",
                    origem
                )

                print(
                    "Destino:",
                    destino
                )

                # =====================================
                # CRIA ID
                # =====================================

                frete_id = origem

                # =====================================
                # VERIFICA DUPLICADO
                # =====================================

                if frete_id in processados:

                    print(
                        f"\nOrigem já processada: "
                        f"{frete_id}"
                    )

                    processados_sequencia += 1

                    print(
                        f"Fretes já processados em sequência: "
                        f"{processados_sequencia}/30"
                    )

                    # =====================================
                    # 30 DUPLICADOS
                    # =====================================

                    if processados_sequencia >= 30:

                        print(
                            "\n30 fretes já processados "
                            "em sequência."
                        )

                        return (
                            None,
                            indice_card,
                            "30_DUPLICADOS",
                            processados_sequencia
                        )

                    # =====================================
                    # VAI PARA O PRÓXIMO CARD
                    # =====================================

                    indice_card += 1

                    continue

                # =====================================
                # FRETE NOVO
                # =====================================

                print(
                    "\nFrete novo encontrado!"
                )

                processados_sequencia = 0

                frete = {

                    "origem": origem,

                    "destino": destino

                }

                return (
                    frete,
                    indice_card,
                    "VALIDO",
                    processados_sequencia
                )

            page.wait_for_timeout(4000)

        except Exception as e:

            print(
                "\nErro ao capturar frete:"
            )

            print(e)

            indice_card += 1
        
# =========================
# MAIN
# =========================

def main():


    indice_cidade = 0
    nome_cidade = cidades[indice_cidade]["cidade"]
    estado = cidades[indice_cidade]["estado"]
    nome_cidade_url = cidades[indice_cidade]["cidade_url"]

    # =========================
    # ABRE FRETEBRAS
    # =========================

    inicio_sistema = iniciar_timer()

    playwright, context, page = abrir_fretebras(
    )

    finalizar_timer(
        "Abrir Fretebras",
        inicio_sistema
    )

    # Variável global do ciclo
    pagina_atual = 1
    total_paginas = 1
    indice_card = 0
    processados_sequencia = 0
    tentativas_cidade = 0
    fretes_processados = 0

    # =========================
    # LOOP PRINCIPAL
    # =========================

    while True:

        ciclo_inicio = iniciar_timer()

        try:

            print("\n===================================")
            print("NOVO CICLO")
            print("===================================\n")

            # =========================
            # ATUALIZA FRETES
            # =========================

            etapa_inicio = iniciar_timer()

            # =========================
            # DEFINE URL
            # =========================
            if pagina_atual == 1:

                # =========================
                # DEFINE URL - PRIMEIRA PÁGINA
                # =========================

                url = (
                    f"https://www.fretebras.com.br/fretes/"
                    f"carga-de-{nome_cidade_url}-{estado}/"
                    f"raio-cem-km"
                )

            else:

                # =========================
                # DEFINE URL - PÁGINAS SEGUINTES
                # =========================

                url = (
                    f"https://www.fretebras.com.br/fretes/"
                    f"carga-de-{nome_cidade_url}-{estado}/"
                    f"raio-cem-km/{pagina_atual}"
                )

            print(f"URL: {url}")
            print(f"Página atual: {pagina_atual}")
            
            # =========================
            # ACESSA PÁGINA
            # =========================

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            try:

                elemento = page.locator("p").filter(
                    has_text="páginas"
                ).first

                print(
                    "Quantidade encontrada:",
                    elemento.count()
                )

                texto_paginas = elemento.inner_text()

                match = re.search(
                    r"de\s+(\d+)\s+páginas",
                    texto_paginas
                )
                if match:

                    total_paginas = int(
                        match.group(1)
                    )

                    print(
                        f"Total de páginas: {total_paginas}"
                    )

            except Exception as e:

                print(
                    f"Erro ao capturar total de páginas: {e}"
                )
                
            finalizar_timer(
                "Atualizar fretes",
                etapa_inicio
            )
            # =========================
            # PROCESSADOS
            # =========================

            processados = carregar_processados()

            print(

                f"\nProcessados carregados: "
                f"{len(processados)}"

            )
            # =========================
            # TOTAL DE FRETES
            # =========================

            cards = page.locator(
                "section"
            ).all()

            total_cards = len(cards)

            print(
                f"\nTotal de cards na página: "
                f"{total_cards}"
            )
            
            # =========================
            # CONFERE CIDADE NA PÁGINA
            # =========================

            cidade_esperada = unicodedata.normalize(
                "NFD",
                nome_cidade.strip().lower()
            ).encode("ascii", "ignore").decode("utf-8")

            print(
                f"\nCidade pesquisada: "
                f"{cidade_esperada.title()}"
            )

            try:

                # Procura o campo da cidade
                campo_cidade = page.locator(
                    'input[placeholder="Escolha a cidade"]'
                ).first

                # Aguarda o campo ficar disponível
                campo_cidade.wait_for(
                    state="visible",
                    timeout=10000
                )

                # Pega o valor atual da página
                cidade_pagina = (
                    campo_cidade.input_value()
                    or ""
                ).strip().lower()

                # Remove acentos
                cidade_pagina = unicodedata.normalize(
                    "NFD",
                    cidade_pagina
                ).encode("ascii", "ignore").decode("utf-8")

                print(
                    f"Cidade na página: "
                    f"{cidade_pagina.title()}"
                )

            except Exception as erro:

                tentativas_cidade += 1

                print(
                    "\n❌ NÃO FOI POSSÍVEL CONFIRMAR A CIDADE."
                )

                print(
                    "O campo 'Escolha a cidade' não foi "
                    "encontrado na página."
                )

                print(
                    f"Tentativa: {tentativas_cidade}/10"
                )

                # =========================
                # ATINGIU 10 TENTATIVAS
                # =========================

                if tentativas_cidade >= 10:

                    print(
                        "\n🚨 10 TENTATIVAS SEM SUCESSO."
                    )

                    print(
                        f"Pulando a cidade: "
                        f"{nome_cidade.title()}"
                    )

                    # Zera o contador
                    tentativas_cidade = 0

                    # Avança para próxima cidade
                    indice_cidade += 1

                    # Reinicia controles
                    pagina_atual = 1
                    indice_card = 0

                    continue

                # =========================
                # AINDA TEM TENTATIVAS
                # =========================

                pagina_atual = 1
                indice_card = 0

                continue


            # =========================
            # COMPARA AS CIDADES
            # =========================

            if cidade_pagina != cidade_esperada:

                print(
                    "\n⚠️ CIDADE INCORRETA!"
                )

                print(
                    f"Esperada: {cidade_esperada.title()}"
                )

                print(
                    f"Encontrada: {cidade_pagina.title()}"
                )

                print(
                    "\nReiniciando o fluxo..."
                )

                pagina_atual = 1
                indice_card = 0

                continue


            # =========================
            # CIDADE CONFIRMADA
            # =========================

            print(
                "\n✅ CIDADE CONFIRMADA!"
            )

            print(
                f"Cidade: {cidade_pagina.title()}"
            )

            # Zera tentativas porque deu certo
            tentativas_cidade = 0

            # =========================
            # CAPTURA FRETE
            # =========================

            etapa_inicio = iniciar_timer()

            frete, indice_card, resultado,processados_sequencia = capturar_fretes(
                page,
                indice_card,
                nome_cidade,
                processados,
                processados_sequencia
            )

            finalizar_timer(
                "Capturar fretes",
                etapa_inicio
            )
             # =========================
            # 30 DUPLICADOS
            # =========================

            if resultado == "30_DUPLICADOS":

                print(
                    "\n30 fretes já processados em sequência."
                )

                print(
                    f"\nFinalizando cidade: "
                    f"{nome_cidade.title()} - {estado.upper()}"
                )

                indice_cidade += 1

                # =========================
                # PRÓXIMA CIDADE
                # =========================

                if indice_cidade < len(cidades):

                    nome_cidade = cidades[indice_cidade]["cidade"]
                    nome_cidade_url = cidades[indice_cidade]["cidade_url"]
                    estado = cidades[indice_cidade]["estado"]

                    pagina_atual = 1
                    indice_card = 0

                    print(
                        "\n==================================="
                    )

                    print(
                        f"PRÓXIMA CIDADE: "
                        f"{nome_cidade.title()} - {estado.upper()}"
                    )

                    print(
                        "==================================="
                    )

                    continue

                # =========================
                # RECOMEÇA DA PRIMEIRA CIDADE
                # =========================

                else:

                    print(
                        "\nTodas as cidades foram processadas."
                    )

                    indice_cidade = 0

                    nome_cidade = cidades[indice_cidade]["cidade"]
                    nome_cidade_url = cidades[indice_cidade]["cidade_url"]
                    estado = cidades[indice_cidade]["estado"]

                    pagina_atual = 1
                    indice_card = 0

                    continue

            # =========================
            # FIM DOS CARDS
            # =========================

            if resultado == "FIM_CARDS":

                print(
                    "\nTodos os cards da página foram analisados."
                )

                indice_card = 0

                # =========================
                # PRÓXIMA PÁGINA
                # =========================

                if pagina_atual < total_paginas:

                    pagina_atual += 1

                    print(
                        f"\nIndo para a página {pagina_atual}"
                    )

                    continue

                # =========================
                # TERMINOU A CIDADE
                # =========================

                print(
                    f"\nFinalizadas todas as páginas de "
                    f"{nome_cidade.title()} - {estado.upper()}"
                )

                indice_cidade += 1

            # =========================
            # FRETE NOVO
            # =========================

            if resultado == "VALIDO":

                # =========================
                # CRIA ID
                # =========================

                frete_id = frete["origem"]


                # =========================
                # VERIFICA ESTADO DA ORIGEM
                # =========================

                origem = frete["origem"].strip().upper()
                estado_atual = estado.strip().upper()

                # Origem vem no formato: "Brasília, DF"
                if "," in origem:
                    uf_origem = origem.split(",")[-1].strip()
                else:
                    uf_origem = ""

                if uf_origem != estado_atual:

                    print("\nOrigem fora do estado pesquisado:")
                    print(f"Frete: {origem}")
                    print(f"UF da origem: {uf_origem}")
                    print(f"Estado pesquisado: {estado_atual}")

                    indice_card += 1

                    continue

                # =========================
                # IGNORA ORIGEM GOIÂNIA
                # =========================

                try:

                    origem = (
                        frete["origem"]
                        .strip()
                        .lower()
                        .replace("â", "a")
                        .replace("á", "a")
                    )


                    if "goiania" in origem:

                        print(
                            "\nIgnorando frete de Goiânia:"
                        )

                        print(
                            frete["origem"]
                        )

                        indice_card += 1

                        continue


                    # =========================
                    # IGNORA SANTA MARIA DE JETIBÁ
                    # =========================

                    if "santa maria de jetiba" in origem:

                        print(
                            "\nIgnorando frete de Santa Maria de Jetibá:"
                        )

                        print(
                            frete["origem"]
                        )

                        indice_card += 1

                        continue


                except Exception as e:

                    print(
                        f"\nErro ao verificar origem: {e}"
                    )

                    indice_card += 1

                    continue


                # =========================
                # FRETE VÁLIDO
                # =========================

                print(
                    f"\nFrete válido: "
                    f"{frete['origem']} -> {frete['destino']}"
                )

            # =========================
            # NOVO FRETE ENCONTRADO
            # =========================

            print("\nNOVO FRETE ENCONTRADO")
            print("========================")

            print(f"Origem : {frete['origem']}")
            print(f"Destino: {frete['destino']}")
            
    
            # =========================
            # SALVA PROCESSADO
            # =========================

            print("\nSalvando frete...")

            try:

                print(f"ID do frete: {frete_id}")

                salvar_processado(frete_id)

                processados.add(frete_id)

                fretes_processados += 1

                print("Frete salvo com sucesso.")

                # =========================
                # PAUSA A CADA 10 FRETES
                # =========================

                if fretes_processados >= 5:

                    print("\nForam processados 10 fretes.")
                    print("Aguardando 5 minutos para continuar...")

                    time.sleep(300)  # 5 minutos

                    fretes_processados = 0

                    print("Retomando processamento...")

            except Exception as e:

                print(f"ERRO AO SALVAR: {e}")

            print(f"\nTOTAL PROCESSADOS: {fretes_processados}")

        
            # =========================
            # ABRIR LOGIN
            # =========================

            page.goto(
                "https://novacentral.fretebras.com.br/meus-fretes",
                wait_until="domcontentloaded",
                timeout=120000
            )

            print("\nReplicador carregado!")

            page.wait_for_timeout(4000)

            inicio_login = iniciar_timer()

            campo_usuario = page.locator("#username")

            if campo_usuario.count() > 0:

                print("Tela de login encontrada.")

                abrir_login(
                    page
                )

            else:

                print("Usuário já está logado.")

            finalizar_timer(
                "Abrir Login",
                inicio_login
            )

            time.sleep(15)


            # =========================
            # ABRIR REPLICADOR
            # =========================

            inicio_replicador = iniciar_timer()

            resultado = abrir_replicador(
                page
            )
            if not resultado:
                continue

            finalizar_timer(
                "Abrir Replicador",
                inicio_replicador
            )   

            # =========================
            # PREENCHER ORIGEM
            # =========================

            inicio_origem = iniciar_timer()

            resultado = preencher_origem(
                page,
                frete
            )
            if not resultado:
                continue
            finalizar_timer(
                "Preencher Origem",
                inicio_origem
            )
            page.wait_for_timeout(4000)

            # =========================
            # PREENCHER DESTINO
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_destino(
                page,
                frete
            )
            if not resultado:
                continue
            finalizar_timer(
                "Preencher Destino",
                inicio_destino
            )
            page.wait_for_timeout(4000)

            # =========================
            # PREENCHER
            # =========================

            inicio_negociador = iniciar_timer()

            resultado = clicar_negociador(
                page
            )
            if not resultado:
                continue
            finalizar_timer(
                "Preencher Negociador",
                inicio_negociador
            )
            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_produto(
                page
            )
          
            if not resultado:
                continue
            finalizar_timer(
                "Preencher Produto",
                inicio_destino
            )
            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_carga(
                page
            )

            if not resultado:
                continue

            finalizar_timer(
                "Preencher Carga",
                inicio_destino
            )
            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_lote(
                page
            )

            if not resultado:
                continue

            finalizar_timer(
                "Preencher Lote",
                inicio_destino
            )   
            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_caminhao(
                page
            )

            if not resultado:
                continue
    
            finalizar_timer(
                "Preencher Caminhão",
                inicio_destino
            )

            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            resultado = preencher_carroceria(page)

            if not resultado:

                continue

            finalizar_timer(
                "Preencher Carroceria",
                inicio_destino
            )

            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            preencher_pagamento(
                page        
            )

            finalizar_timer(
                "Preencher Pagamento",
                inicio_destino
            )

            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            preencher_final(
                page        
            )

            finalizar_timer(
                "Preencher Final",
                inicio_destino
            )

            # =========================
            # PREENCHER 
            # =========================

            inicio_destino = iniciar_timer()

            preencher_publicar(
                page        
            )

            finalizar_timer(
                "Preencher Publicar",
                inicio_destino
            )

            page.wait_for_timeout(3000)
            # =========================
            # ABRIR MOTORISTAS SUGERIDOS
            # =========================

            inicio_motoristas = iniciar_timer()

            try:

                page.goto(
                    "https://novacentral.fretebras.com.br/meus-fretes",
                    wait_until="domcontentloaded",
                    timeout=120000
                )
                page.wait_for_timeout(30000)

                origem = frete["origem"]

                print(
                    f"\nProcurando frete publicado: {origem}"
                )

                frete_encontrado = False

                for tentativa in range(10):

                    try:

                        page.wait_for_timeout(6000)

                        # Procura todos os elementos que possuem exatamente o texto da origem
                        origens = page.get_by_text(origem, exact=True)

                        total = origens.count()

                        print(f"Foram encontradas {total} ocorrências da origem.")

                        for i in range(total):

                            origem_elemento = origens.nth(i)

                            try:

                                # Sobe até o primeiro ancestral que possui o botão
                                card = origem_elemento.locator(
                                    "xpath=ancestor::*[.//button[@data-testid='suggested-trucker-list-item-beta']][1]"
                                )

                                botao = card.locator(
                                    '[data-testid="suggested-trucker-list-item-beta"]'
                                )

                                if botao.count() == 0:
                                    continue

                                print(f"Frete localizado: {origem}")

                                botao.click(force=True)

                                page.wait_for_timeout(3000)

                                print("Motoristas sugeridos aberto!")

                                frete_encontrado = True

                                break

                            except Exception:
                                continue

                        if frete_encontrado:
                            break

                    except Exception as erro:

                        print(f"Erro na tentativa {tentativa+1}: {erro}")

                    print(f"Tentativa {tentativa+1}/10")

                    page.reload(wait_until="domcontentloaded")
            except Exception as erro:

                print("\nErro ao abrir motoristas sugeridos:")
                print(erro)

            finalizar_timer(
                "Abrir Motoristas Sugeridos",
                inicio_motoristas
            )
            # =========================
            # CONTAR MOTORISTAS
            # =========================

            inicio_motoristas = iniciar_timer()

            quantidade_motoristas = contar_motoristas(
                page
            )

            finalizar_timer(
                "Contar Motoristas",
                inicio_motoristas
            )
            
            # =========================
            # SELECIONAR MOTORISTAS
            # =========================

            inicio_selecionar_motoristas = iniciar_timer()

            selecionar_todos_motoristas(
                page
            )

            finalizar_timer(
                "Selecionar Motoristas",
                inicio_selecionar_motoristas
            )

            # =========================
            # ABRIR CHAT
            # =========================

            abrir_chats= iniciar_timer()

            abrir_chat_envio(
                page
            )

            finalizar_timer(
                "Chat Aberto",
                abrir_chats
            )

            # =========================
            # ABRIR CHAT
            # =========================

            chat_enviar= iniciar_timer()

            enviar_chat_compartilhar(
                page
            )

            finalizar_timer(
                "Chat Enviado",
                chat_enviar
            )
           
            # =========================
            # ANALISAR LEADS NO CHAT
            # =========================

            analisar_cards(
                page, quantidade_motoristas
            )


            # =======================
            # AGUARDAR ANTES DO PRÓXIMO PROCESSO
            # =========================

            tempo_espera = random.randint(60, 120)

            print(f"\nAguardando {tempo_espera} segundos para iniciar um novo processo...")

            time.sleep(tempo_espera)

        except Exception as erro_geral:

            print("\nERRO GERAL:")

            print(erro_geral)

            page

            time.sleep(10)

        print("\nTodos os cards da página foram analisados.")

        indice_card = 0

        if pagina_atual < total_paginas:

            pagina_atual += 1

            print(f"\nIndo para a página {pagina_atual}")

        else:

            print(
                f"\nFinalizadas todas as páginas de "
                f"{nome_cidade.title()} - {estado.upper()}"
            )

            indice_cidade += 1

            if indice_cidade < len(cidades):

                nome_cidade = cidades[indice_cidade]["cidade"]
                estado = cidades[indice_cidade]["estado"]

                pagina_atual = 1

                print(
                    f"\nIniciando próxima cidade: "
                    f"{nome_cidade.title()} - {estado.upper()}"
                )

            else:

                print("\nTodas as cidades foram processadas.")

                indice_cidade = 0

                nome_cidade = cidades[indice_cidade]["cidade"]
                estado = cidades[indice_cidade]["estado"]

                pagina_atual = 1

                print(
                    f"\nReiniciando ciclo pela cidade: "
                    f"{nome_cidade.title()} - {estado.upper()}"
                )

        continue
if __name__ == "__main__":
    main()