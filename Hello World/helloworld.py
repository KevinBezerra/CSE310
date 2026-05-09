# function
def hello_world():

    #list
    poem = [
        "A blank screen, a blinking line,",
        "Logic and syntax start to entwine.",
        "No heartbeat here, no lungs to fill,",
        "Just silicon waiting on human will.",
        "One command, a compilation hurled,",
        "And the ghost in the machine says: 'Hello World.'"
    ]

    print("--- Press ENTER to read ---")

    #for loop
    for line in poem:
        input() # waits for the user to press enter
        print(line, end="") # prevents double spacing

    print("\n\n[End of Program]")

if __name__ == "__main__":
    hello_world()