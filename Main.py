from Controller import Controller

if __name__ == "__main__":
    controller = Controller()
    try:
        controller.start()
    except KeyboardInterrupt:
        print("Encerrando aplicação...")
        controller.stop()
