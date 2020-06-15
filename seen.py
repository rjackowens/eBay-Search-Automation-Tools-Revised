import mmap

names = [
    "some random thing",
    "joe",
    "yoyoyoyoyo",
    "woop",
    "estella"
]

# with open("seen.txt", mode="r+") as file:
#     already_in_file = file.readlines()
#     for x in names:
#         if x not in already_in_file:
#             print(f"{x} is new, adding to seen.txt")
#             file.writelines(x + "\n")

word_iterator = "jack"

# with open('seen.txt', 'rb', 0) as file, \
#     mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
#     if s.find(word_iterator.encode()) == -1:
#         print(f"{word_iterator} is new, adding to seen.txt")
#         file.writelines(word_iterator.encode())


with open('seen.txt', mode="r+") as file:
    if word_iterator not in file.read():
        print(f"{word_iterator} is new, adding to seen.txt")
        file.writelines(word_iterator)



# with open("seen.txt", mode="r+") as file:
#     already_in_file = file.readlines()
#     for x in already_in_file:
#         if "joe" not in x:
#             print(f"{x} is new, adding to seen.txt")
#             file.writelines(x)
