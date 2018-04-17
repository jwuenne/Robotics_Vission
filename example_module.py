'''
Created on Jun 29, 2017

@author: jwuenne
'''
counter = 4.0
x = 2
print(counter)
print("hello, World!")

    
mystring = 'hello'
print(mystring)
mystring = "hello"
print(mystring)
mystring = "Don't worry about apostrophes"
print(mystring)

print(x == 2) # prints out True
print(x == 3) # prints out False
print(x < 3) # prints out True

if x == 2 and counter ==5 :
    print("hello, World!")
else:
    print("good bye world")
 
 
 # Prints out the numbers 0,1,2,3,4
for x in range(5):
    print(x)

# Prints out 3,4,5
for x in range(3, 6):
    print(x)

# Prints out 3,5,7
for x in range(3, 8, 2):
    print(x)