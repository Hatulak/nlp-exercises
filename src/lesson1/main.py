import spacy
import random
import string
import collections



def main():
    create_words_dictionary()
    make_errors_in_some_words()
    repair_errors()
    compute_errors_remaining_after_repair()


def compute_errors_remaining_after_repair():
    nlp = spacy.load("en_core_web_sm")

    with open("przyklad.txt", 'r') as f:
        original_text = f.read()

    with open("przyklad_poprawiony.txt", 'r') as f:
        repaired_text = f.read()

    original_doc = nlp(original_text)
    original_words = [token.text for token in original_doc if token.is_alpha]

    repaired_doc = nlp(repaired_text)
    repaired_words = [token.text for token in repaired_doc if token.is_alpha]

    # print(original_words)
    # print(repaired_words)

    errors_counter = 0
    for i in range(len(original_words)):
        if original_words[i] != repaired_words[i]:
            print("original: " + original_words[i] + " | repaired: " + repaired_words[i])
            errors_counter = errors_counter + 1

    print(errors_counter)


def repair_errors():
    nlp = spacy.load("en_core_web_sm")

    with open("przyklad_z_bledami.txt", 'r') as f:
        text_with_errors = f.read()

    with open("slownik.txt", 'r') as f:
        text_dict = f.read()

    doc_with_errors = nlp(text_with_errors)
    text_tokens = [token for token in doc_with_errors]

    num_words_with_erros_dict = dict()

    for i in range(len(text_tokens)):
        num_words_with_erros_dict[i] = text_tokens[i]

    only_words_with_errors_num_text_dict = dict()
    for (key, value) in num_words_with_erros_dict.items():
        if value.is_alpha:
            only_words_with_errors_num_text_dict[key] = value.text

    doc_dict = nlp(text_dict)
    dict_words = [token.text for token in doc_dict if token.is_alpha]

    # print(dict_words)

    repaired_words = dict()

    for (key, word_that_may_contain_errors) in only_words_with_errors_num_text_dict.items():
        distance_word_dict = dict()
        for dict_word in dict_words:
            distance = compute_levenshtein_distance(word_that_may_contain_errors, dict_word)
            distance_word_dict[distance] = dict_word
            if distance == 0:
                break  # wyraz nie ma błędów, nie trzeba szukać dalej
        distance_word_dict_sorted = collections.OrderedDict(sorted(distance_word_dict.items()))

        repaired_words[key] = distance_word_dict_sorted[next(iter(distance_word_dict_sorted))]

    # print(num_words_with_erros_dict)
    # print(repaired_words)

    with open("przyklad_poprawiony.txt", 'w') as out:
        for i in range(len(text_tokens)):
            if i in repaired_words:
                out.write(repaired_words[i] + " ")
            else:
                out.write(text_tokens[i].text + " ")


def create_words_dictionary():
    nlp = spacy.load("en_core_web_sm")

    with open("przyklad.txt", "r") as f:
        my_text = f.read()

    my_doc = nlp(my_text)

    text_tokens = [token for token in my_doc]
    tokens = [token for token in my_doc if token.is_alpha]
    # print(len(tokens))

    words = [token.text for token in tokens]
    unique_words = set([token.text for token in tokens])
    # print(len(words))

    with open("slownik.txt", 'w') as out:
        [out.write(word + '\n') for word in unique_words]


def make_errors_in_some_words():
    nlp = spacy.load("en_core_web_sm")

    with open("przyklad.txt", "r") as f:
        my_text = f.read()

    my_doc = nlp(my_text)

    text_tokens = [token for token in my_doc]

    tokens = [token for token in my_doc if token.is_alpha]

    words = [token.text for token in tokens]

    number_of_words_to_modify = int(len(words) / 5)

    num_text_dict = dict()

    for i in range(len(text_tokens)):
        num_text_dict[i] = text_tokens[i]

    only_words_num_text_dict = dict()
    for (key, value) in num_text_dict.items():
        if value.is_alpha:
            only_words_num_text_dict[key] = value.text

    words_to_change_dict = dict(random.sample(only_words_num_text_dict.items(), number_of_words_to_modify))

    changed_words = dict()

    for (key, value) in words_to_change_dict.items():
        number_of_changes = get_number_of_changes()
        for i in range(number_of_changes):
            change_type = get_change_type(len(value))
            value = change_word(value, change_type)
        changed_words[key] = value

    with open("przyklad_z_bledami.txt", 'w') as out:
        for i in range(len(text_tokens)):
            if i in changed_words:
                out.write(changed_words[i] + " ")
            else:
                out.write(text_tokens[i].text + " ")


def get_number_of_changes():
    return random.randint(1, 3)


def get_change_type(word_length):
    if word_length < 2:
        return random.choice(["add", "swap"])
    return random.choice(["delete", "add", "swap"])  # returns: "delete", "add", "swap"


def change_word(word, change_type):
    if change_type == "delete":
        if len(word) == 1:
            raise ValueError("Cannot delete letter from 1-letter length word")
        listed_string = list(word)
        to_delete_letter_place = random.randint(0, len(word) - 1)
        listed_string[to_delete_letter_place] = ""
        return "".join(listed_string)
    elif change_type == "add":
        new_letter_place = random.randint(0, len(word))
        if new_letter_place == 0:
            return random.choice(string.ascii_letters) + word
        elif new_letter_place == len(word):
            return word + random.choice(string.ascii_letters)
        else:
            return word[:new_letter_place] + random.choice(string.ascii_letters) + word[new_letter_place:]

    elif change_type == "swap":
        listed_string = list(word)
        listed_string[random.randint(0, len(listed_string) - 1)] = random.choice(string.ascii_letters)
        return "".join(listed_string)
    else:
        raise ValueError(change_type + " - this is not a proper value")


def compute_levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return compute_levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


if __name__ == "__main__":
    main()
