#!/bin/env python
from random import choices


def split_names(namelist, take=None):
    vowels_list = "ауоыиэяюёе"
    male_names = []
    female_names = []
    for name in namelist:
        if name[-1] in vowels_list:
            female_names.append(name.title())
        else:
            male_names.append(name.title())
    if not take:
        return male_names, female_names
    else:
        return choices(male_names, k=take), choices(female_names, k=take)


def family_generator(wordlist, take=1, male=True):
    consonant_list = list("бвгджзклмнпрстфхцчшщ")
    postfix = ["ев", "ов"]

    def check_rule(word):
        if end_with_list(word, consonant_list):
            return (word + postfix).title()
        else:
            if word[-1] == postfix[0]:
                if postfix[0] == "е" and end_with_list(word[:-1], consonant_list):
                    return (word + postfix).title()
                else:
                    return (word[:-1] + postfix).title()
            else:
                i = 1
                while not end_with_list(word[:-i], consonant_list):
                    if i > len(word):
                        return None
                    i += 1
                return (word[:-i] + postfix).title()
        return None

    def end_with_list(text, s_list):
        for symb in s_list:
            if text.endswith(symb):
                return True
        return False

    select_postfix = map(lambda x: x + "" if male else x + "а", choices(postfix, k=take))
    select_words = choices(wordlist, k=take)
    result_list = []
    for word, postfix in zip(select_words, select_postfix):
        result = None
        while not result:
            result = check_rule(word)
            if result:
                result_list.append(result)
    return result_list


if __name__ == "__main__":
    take_count = 10

    wordlist = open("word_rus.txt").read().split("\n")
    names = open("name_rus.txt").read().split("\n")

    male, female = split_names(names, take=take_count)

    f = map(lambda x: x[1] + " " + x[0], zip(family_generator(wordlist, take=take_count, male=False), female))
    m = map(lambda x: x[1] + " " + x[0], zip(family_generator(wordlist, take=take_count), male))

    print("{}\n{}".format("\n".join(f), "\n".join(m)))
