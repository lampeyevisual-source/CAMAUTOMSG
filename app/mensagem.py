from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from notificacoes import avisar

# =========================
# CONTAR MOTORISTAS
# =========================

def contar_motoristas(page):
    try:
        print("\nAguardando a lista de motoristas carregar...")

        lista = page.locator(
            '[data-testid="suggested-trucker-list"]'
        )

        # Espera a lista ficar visível
        lista.wait_for(
            state="visible",
            timeout=30000
        )

        cards_motoristas = lista.locator(
            '[data-testid="trucker-list-item"]'
        )

        # Aguarda a lista começar a receber motoristas
        page.wait_for_function(
            """() => {
                const lista = document.querySelector(
                    '[data-testid="suggested-trucker-list"]'
                );

                return lista &&
                    lista.querySelectorAll(
                        '[data-testid="trucker-list-item"]'
                    ).length > 0;
            }""",
            timeout=30000
        )

        # Aguarda a quantidade ficar estável por 2 segundos
        page.wait_for_function(
            """() => {
                const lista = document.querySelector(
                    '[data-testid="suggested-trucker-list"]'
                );

                if (!lista) return false;

                const contar = () =>
                    lista.querySelectorAll(
                        '[data-testid="trucker-list-item"]'
                    ).length;

                const quantidadeInicial = contar();

                if (quantidadeInicial === 0) return false;

                return new Promise(resolve => {
                    setTimeout(() => {
                        resolve(
                            contar() === quantidadeInicial
                        );
                    }, 2000);
                });
            }""",
            timeout=30000
        )

        quantidade = cards_motoristas.count()

        print(f"Motoristas encontrados: {quantidade}")

        avisar(
            "CAM AGROLOG - Fretebras",
            f"Motoristas encontrados: {quantidade}"
        )

        return quantidade

    except PlaywrightTimeoutError:
        print(
            "\nTempo esgotado: a lista não carregou "
            "ou nenhum motorista apareceu."
        )

        avisar(
            "CAM AGROLOG - Fretebras",
            "A lista de motoristas não carregou a tempo."
        )

        return 0

    except Exception as erro:
        print(f"\nErro ao contar motoristas: {erro}")
        return 0
    
def selecionar_todos_motoristas(page):

    try:

        print("\nSelecionando todos os motoristas...")

        checkbox_todos = page.locator(
            "[data-testid='list-header'] label.fuel-checkbox-label"
        )

        if checkbox_todos.count() == 0:

            print("Nenhum motorista encontrado.")

            page.go_back()

            return False

        checkbox_todos.scroll_into_view_if_needed()

        checkbox_todos.click(force=True)

        page.wait_for_timeout(2000)

        print("Todos os motoristas selecionados!")

        return True

    except Exception as erro:

        print(erro)

        page.go_back()

        return False        
    
# =========================
# ABRIR CHAT (ENVIO FINAL)
# =========================

def abrir_chat_envio(page):

    try:

        print("\nAbrindo chat de envio...")

        page.wait_for_timeout(3000)

        botao_chat = page.locator(
            "button[data-testid='share-freight']"
        ).first

        botao_chat.wait_for(
            state="visible",
            timeout=15000
        )

        botao_chat.scroll_into_view_if_needed()

        botao_chat.click(force=True)

        page.wait_for_timeout(5000)

        print("Chat aberto com sucesso!")

    except Exception as erro:

        print("\nErro ao abrir chat:")

        print(erro)

        page.go_back()

# =========================
# CLICAR EM COMPARTILHAR
# =========================

def enviar_chat_compartilhar(page, nome_cidade):
    try:
        print("\nAguardando campo de mensagem...")

        # 1. Espera o campo de mensagem carregar
        campo_texto = page.locator(
            'textarea[aria-label="Mensagem complementar"]'
        )

        campo_texto.wait_for(
            state="visible",
            timeout=30000
        )
        page.wait_for_timeout(800)
        # 2. Preenche a mensagem
        cidade_formatada = nome_cidade.strip().title()
        mensagem = f"Frete Representado em {cidade_formatada}."

        campo_texto.fill(mensagem)

        print(f"Mensagem preenchida: {mensagem}")
                
        page.wait_for_timeout(500)

        # 3. Localiza o botão confirmado pelo HTML
        botao_compartilhar = page.locator(
            'button[aria-label="Compartilhar"]'
            '[data-variant="primary"]'
            '[data-size="large"]'
        )

        botao_compartilhar.wait_for(
            state="visible",
            timeout=30000
        )

        # 4. Espera o botão ficar habilitado
        page.wait_for_function(
            """() => {
                const botao = document.querySelector(
                    'button[aria-label="Compartilhar"]'
                );

                return botao &&
                    botao.offsetParent !== null &&
                    !botao.disabled &&
                    botao.getAttribute('data-disabled') !== 'true' &&
                    botao.getAttribute('data-loading') !== 'true';
            }""",
            timeout=30000
        )

        # 5. Clica no botão
        botao_compartilhar.click(timeout=10000)

        print("Clique em Compartilhar realizado!")

        return True

    except Exception as erro:
        print("\nErro ao compartilhar:")
        print(erro)

        return False

