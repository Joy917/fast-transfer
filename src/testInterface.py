import interface


client = interface.Interface()
def upTest():
    result = client.upLoad("D:/test1.zip","D:/10086")
    while result:
        print client.perUp

def downTest():
    result = client.downLoad("D:/test1.zip", "D:/10086")
    while result:
        print client.perDown

if __name__ == "__main__":
    # upTest()
    downTest()