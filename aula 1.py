import random

elements= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=~`"

password = ""

tamanho = int(input("Digite o tamanho da senha: "))

for i in range(tamanho):
    password += random.choice(elements)


print("Senha gerada: ", password)



















