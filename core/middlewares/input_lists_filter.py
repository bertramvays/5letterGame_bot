def no(word, letters_no):
    # Функция пропускает слова по списку букв которых нет в слове
    if len(letters_no) == 0:
        return True
    else:
        return not any([i in word for i in letters_no])


def letter_position_filter(word, known_position, unknown_position):
    # Функция пропускает слова по спискам известных позиций и неизвестных
    letter_list = list(word)
    bool_filter_list = []  # список значений проверки позиций букв в слове.
    for let in known_position:
        kn_indexes_of_letters = [i + 1 for i, v in enumerate(letter_list) if let[0] == v]  # индексы встречающихся букв
        if len(kn_indexes_of_letters) == 0:
            bool_filter_list.append(False)
        else:
            for _ in kn_indexes_of_letters:
                if letter_list[int(let[1]) - 1] == let[0]:
                    bool_filter_list.append(True)
                else:
                    bool_filter_list.append(False)
    for let in unknown_position:
        unk_indexes_of_letters = [i for i, v in enumerate(letter_list) if let[0] == v]
        if len(unk_indexes_of_letters) == 0:
            bool_filter_list.append(False)
        else:
            for i in unk_indexes_of_letters:
                if i + 1 == int(let[1]):
                    bool_filter_list.append(False)
                else:
                    bool_filter_list.append(True)
    return all(bool_filter_list)
