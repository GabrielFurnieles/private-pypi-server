from p1.module1 import hello_p1
from p2.module2 import hello_p2


def hello_uv3():
    hello_p1()
    hello_p2()
    print("Hello, UV3!")


hello_uv3()
