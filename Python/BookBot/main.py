def count_words(book_path):
    with open(book_path) as novel:
        novel_contents = novel.read()
        words_arrray = novel_contents.split()
        return len(words_arrray)

def number_of_each_char(book_path):
    char_count = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
    with open(book_path) as novel:
        novel_content = novel.read().lower()
        for i in range(len(novel_content)): 
            if novel_content[i] in char_count:
                char_count[novel_content[i]] = char_count[novel_content[i]] + 1
    return char_count

def main():
    char_to_count = "r"
    novel_path = "novel.txt"
    total_words = count_words(novel_path)
    total_each_char = number_of_each_char(novel_path)
    print(f"Total words in book is {total_words} \nTotal number of each char is {total_each_char}")

main()