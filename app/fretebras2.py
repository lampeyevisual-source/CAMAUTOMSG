
import csv
import os
import random
from datetime import datetime


# Caminho do arquivo de contatos
CAMINHO_CSV = "app/msg/contatosfrete.csv"

mensagens = []



# =====================================
# FUNÇÃO PARA CONSULTAR CSV
# =====================================

def buscar_contato_csv(id_motorista):

    try:

        with open(
            CAMINHO_CSV,
            "r",
            encoding="utf-8"
        ) as arquivo:


            leitor = csv.DictReader(arquivo)


            for linha in leitor:

                if linha["id"] == id_motorista:

                    return linha


        return None


    except Exception as erro:

        print("Erro CSV:", erro)

        return None
# =====================================
# ABRIR CHAT
# =====================================

def abrir_chat(card):

    try:

        print("\nAbrindo chat...")

        card.scroll_into_view_if_needed()

        card.wait_for(
            state="visible",
            timeout=5000
        )

        card.click()

        print("Chat aberto!")

        return True

    except Exception as erro:

        print("\nErro ao abrir chat:")
        print(erro)

        return False
    
def carregar_mensagens(nome_arquivo):

    global mensagens

    pasta = os.path.join(
        os.path.dirname(__file__),
        "msg",
        "mensagens"
    )

    arquivo = os.path.join(
        pasta,
        nome_arquivo
    )

    with open(
        arquivo,
        "r",
        encoding="utf-8"
    ) as f:

        conteudo = f.read()

    mensagens = [
        mensagem.strip()
        for mensagem in conteudo.split("###")
        if mensagem.strip()
    ]

    print(
        f"{len(mensagens)} mensagens carregadas."
    )

def pegar_mensagem():

    global mensagens

    if not mensagens:
        return None

    return random.choice(mensagens)

# =====================================
# ESCREVER MENSAGEM
# =====================================
def escrever_mensagem(page):

    try:

        mensagem = pegar_mensagem()

        if not mensagem:
            print("Nenhuma mensagem disponível.")
            return False

        print("\nLocalizando caixa de mensagem...")

        caixa = page.locator(
            "textarea[data-testid='message-input']"
        )

        if caixa.count() == 0:

            print("Chat sem caixa de mensagem. Pulando...")

            return False

        caixa.first.wait_for(
            state="visible",
            timeout=3000
        )

        caixa.first.click()

        page.wait_for_timeout(500)

        caixa.first.fill(mensagem)

        page.wait_for_timeout(500)

        caixa.first.press("Enter")

        print("\nMensagem enviada!")

        return True

    except Exception as erro:

        print(
            "\nNão foi possível enviar a mensagem. "
            "Pulando para o próximo chat."
        )

        print(erro)

        return False


# =====================================
# VERIFICAR SE PODE ENVIAR
# =====================================

def verificar_envio(contato):

    # Contato novo → pode enviar
    if contato is None:

        print("Contato novo. Pode enviar.")

        return True


    # Contato já possui envio registrado → não enviar
    print(
        f"Contato já recebeu mensagem em "
        f"{contato['data_envio']}. Não enviar novamente."
    )

    return False


# =====================================
# ATUALIZAR CSV
# =====================================

def atualizar_csv(id_motorista, nome="", ddd=""):

    linhas = []

    encontrado = False


    with open(
        CAMINHO_CSV,
        "r",
        encoding="utf-8"
    ) as arquivo:


        leitor = csv.DictReader(arquivo)


        for linha in leitor:


            if linha["id"] == id_motorista:


                encontrado = True


                linha["data_envio"] = datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                )


                linha["quantidade_envios"] = str(
                    int(linha["quantidade_envios"] or 0) + 1
                )


            linhas.append(linha)



    # Se for novo contato
    if encontrado == False:


        linhas.append({

            "id": id_motorista,

            "nome": nome,

            "ddd": ddd,

            "data_envio": datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            ),

            "quantidade_envios": "1"

        })



    with open(
        CAMINHO_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:


        campos = [
            "id",
            "nome",
            "ddd",
            "data_envio",
            "quantidade_envios"
        ]


        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )


        escritor.writeheader()

        escritor.writerows(linhas)


    print("CSV atualizado:", id_motorista)

def analisar_cards(page, quantidade_motoristas):

    print("\nAbrindo página do Chat...")

    page.goto(
        "https://novacentral.fretebras.com.br/chat",
        wait_until="domcontentloaded",
        timeout=120000
    )

    page.wait_for_timeout(8000)

    print("\nIniciando análise dos cards...")

    carregar_mensagens("liga.txt")

    cards = page.locator(
        "button[data-testid='channel-preview-id']"
    )

    quantidade = cards.count()

    print(
        f"Cards encontrados no Chat: {quantidade}"
    )

    quantidade_analisar = quantidade_motoristas + 20

    print(
        f"Motoristas desejados: {quantidade_motoristas}"
    )

    print(
        f"Margem de segurança: +10"
    )

    print(
        f"Total de chats para analisar: {quantidade_analisar}"
    )

    if quantidade == 0:
        print("Nenhum lead para processar.")
        return

    # Processa a quantidade desejada + 10 de margem
    limite = min(
        quantidade_analisar,
        quantidade
    )

    print(
        f"Processando os primeiros {limite} chats..."
    )

    for i in range(limite):

        try:

            # Recria o locator porque a lista pode mudar
            cards = page.locator(
                "button[data-testid='channel-preview-id']"
            )

            quantidade_atual = cards.count()

            if i >= quantidade_atual:
                break

            card = cards.nth(i)

            # ==============================
            # NOME
            # ==============================

            nome = (
                card
                .locator("p")
                .first
                .inner_text()
            )

            # ==============================
            # TEXTO DO CARD
            # ==============================

            texto = card.inner_text()

            # ==============================
            # DDD
            # ==============================

            ddd = ""

            if "DDD:" in texto:

                ddd = (
                    texto
                    .split("DDD:")[1]
                    .split("\n")[0]
                    .strip()
                )

            # ==============================
            # IMAGEM DO MOTORISTA
            # ==============================

            imagem = card.locator(
                "img"
            ).get_attribute("src")

            if not imagem:

                print(
                    f"{nome} - sem imagem. Pulando..."
                )

                continue

            # ==============================
            # VERIFICAR SE É MOTORISTA
            # ==============================

            if "/truckers/" not in imagem:

                print(
                    f"{nome} - chat diferente. Pulando..."
                )

                continue

            # ==============================
            # ID DO MOTORISTA
            # ==============================

            id_motorista = (
                imagem
                .split("/truckers/")[1]
                .split("/")[0]
            )

            print(
                f"\nProcessando: {nome}"
            )

            print(
                f"ID: {id_motorista}"
            )

            print(
                f"DDD: {ddd}"
            )

            # ==============================
            # CONSULTAR CSV
            # ==============================

            contato = buscar_contato_csv(
                id_motorista
            )

            # ==============================
            # BLOQUEAR SE JÁ ENVIOU
            # ==============================

            if contato is not None:

                print(
                    f"Contato já recebeu mensagem em "
                    f"{contato['data_envio']}."
                )

                print(
                    "NÃO ENVIAR. Pulando este motorista..."
                )

                continue

            # ==============================
            # ABRIR CHAT
            # ==============================

            if not abrir_chat(card):

                print(
                    "Não foi possível abrir o chat."
                )

                continue

            page.wait_for_timeout(1500)

            # ==============================
            # ENVIAR MENSAGEM
            # ==============================

            if escrever_mensagem(page):

                atualizar_csv(
                    id_motorista,
                    nome,
                    ddd
                )

                print(
                    "Envio concluído."
                )

            else:

                print(
                    "Mensagem não enviada."
                )

        except Exception as erro:

            print(
                "\n==================================="
            )

            print(
                f"ERRO NO CARD {i + 1}"
            )

            print(erro)

            print(
                "==================================="
            )

            continue

    print(
        f"\nAnálise dos cards concluída. "
        f"{limite} chats processados."
    )

    return