name = "hello world"
print(name.title())

print("\tw\tw\tw\tw\tw\n\tw\tw\tw")
print(" w w w w w w w w")

my_foods = ["A","B","C"]
friend_foods = my_foods
he_foods = my_foods[:]
print(my_foods)
print(friend_foods)
print(he_foods)
my_foods.append("my")
friend_foods.append("friend")
he_foods.append("he")
print(my_foods)
print(friend_foods)
print(he_foods)
print("tab")
print("4space")

def eggs(someParameter):
    someParameter.append('Hello')
    
spam = [1, 2, 3]
eggs(spam)
print(spam)

def egg():
    global kk
    kk = 2
    
kk = 3
egg()
print(kk)
