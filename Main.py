from .server import APIServer


def main():
    server = APIServer()
    server.run()


if __name__ == '__main__':
    main()