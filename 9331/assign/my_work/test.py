


class a():
    def __init__(self, host):
        self.address = None
        self.host = host

    def change(self):
        self.host.con = 1


class b():
    def __init__(self):
        self.con = 0

    def changecon(self):
        new = a(self)
        new.change()
        print(self.con)

if __name__ == '__main__':
    a = "Store a123"
    b = 4100 % 256

    print(a.split(), b)

