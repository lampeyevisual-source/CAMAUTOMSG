from winotify import Notification


def avisar(titulo, mensagem):

    try:

        toast = Notification(
            app_id="CAM AGROLOG",
            title=str(titulo),
            msg=str(mensagem),
            duration="long"
        )

        toast.show()

        print(f"[NOTIFICAÇÃO] {titulo}")

    except Exception as e:

        print(f"[ERRO NOTIFICAÇÃO] {e}")