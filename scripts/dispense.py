from brownie import *

def main():
    for i in range(10):
        shot(i)
#define function "shot"
def shot(i):
    return Token.deploy('Margarita',
                        'MAR',
                        18,
                        1e21,
                        {'from': accounts[i]})