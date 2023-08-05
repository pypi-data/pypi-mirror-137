import toontown
import toontown.models


def main():
    with toontown.SyncToontownClient() as client:
        print(client.doodles())
        print(client.field_offices())
        print(client.invasions())
        # print(client.login(username, password))
        print(client.population())


main()
