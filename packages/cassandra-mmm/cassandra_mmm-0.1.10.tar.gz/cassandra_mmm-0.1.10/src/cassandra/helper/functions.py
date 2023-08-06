def helper_data():
    with open("./helper/text/clean_and_format.txt") as f: # The with keyword automatically closes the file when you are done
        print(f.read())

    with open("./helper/text/pivot.txt") as f:
        print(f.read())

def helper_nevergrad():
    with open("./helper/text/nevergrad.txt") as f:
        print(f.read())