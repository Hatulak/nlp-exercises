import re

def main():

    with open("maraton.txt", "r") as f:
        text = f.read()

        print(re.findall("2:[0-9]{2}:[0-9]{2}", text))
        # print(re.findall("[0-9]:[0-9]{2}:[0-9]{2}", text))



if __name__ == "__main__":
    main()
