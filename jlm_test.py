# some basic test code
name = input("Enter your name:")
print(f"Hello, {name}!")

high_num = int(input("How high would you like me to count? "))

# this checks if basic math and loops work
print(f"Counting from 1 to {high_num}:")
for i in range (1, high_num + 1):
    print(i)

print("Test complete!")