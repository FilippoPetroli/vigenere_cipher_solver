from itertools import zip_longest

file = 'texts/cipher0.txt'
max_length_key_test = 15


alphabet = 'abcdefghijklmnopqrstuvwxyz'

def split_text(text, n):
    return [text[i * n:(i + 1) * n] for i in range((len(text) + n - 1) // n )]


def distance_between_letters(letter1, letter2):
    distance = abs(ord(letter2.upper()) - ord(letter1.upper()))
    return distance


def open_file(file):
    with open(file, 'r') as file:
        return file.read()


def save_file(text):
    with open('result.txt', 'w') as file:
        file.write(text)


def substrings_by_position(split_text):
    new_list = []
    for sublist in split_text:
        for j, item in enumerate(sublist):
            if len(new_list) <= j:
                new_list.append([item])
            else:
                new_list[j].append(item)
    return new_list


def reverse_substrings_by_position(list_of_substrings):
    return ''.join([i for tup in zip_longest(*list_of_substrings, fillvalue='') for i in tup])


def calc_index_coincidence(text):
    text = text.upper()
    letter_frequency = [0] * 26
    letter_total = 0
    for letter in text:
        if letter.isalpha():
            letter_frequency[ord(letter.upper()) - 65] += 1
            letter_total += 1

    index_coincidence = 0
    for frequency in letter_frequency:
        index_coincidence += (frequency * (frequency - 1)) / (letter_total * (letter_total - 1))

    return index_coincidence


def caesar_cipher_decrypt(text, key):
    message = ''
    for char in text:
        if char in alphabet:
            position = alphabet.find(char)
            new_position = (position - key) % 26
            new_character = alphabet[new_position]
            message += new_character
        else:
            message += char
    return message


def find_key_length(file, max_length_key_test):
    text = open_file(file)

    key_length = 0
    ic = 0

    print('\nTesting different key lengths....\n')

    for i in range(1, max_length_key_test+1):

        chunks_text = split_text(text, i)

        new_list = substrings_by_position(chunks_text)

        sum = 0
        count = 0
        for item in new_list:
            sum += calc_index_coincidence(''.join(item))
            count += 1

        ic_chunk = sum/count

        print('Key length: ' + str(i) + '  |  Index of Coincidence: ' + str(ic_chunk))

        if (ic_chunk > ic) and (ic_chunk - ic > 0.01):
            ic = ic_chunk
            key_length = i

    print("\nIt's expected that the key length is " + str(key_length) + " because the index of coincidence is " + str(ic))
    return key_length


def decrypt(file, key_length):

    print('\nTrying to decrypt using a key length of ' + str(key_length) + '....\n')
    text = open_file(file)
    chunks_text = split_text(text, key_length)
    new_list = substrings_by_position(chunks_text)
    new_list_decrypted = []

    key = []

    for index, chunk_text in enumerate(new_list):
        count = {}

        for letter in chunk_text:
            if letter in count:
                count[letter] += 1
            else:
                count[letter] = 1

        count = dict(sorted(count.items(), key=lambda item: item[1], reverse=True))

        top_letter = list(count.items())[0][0]
        distance = distance_between_letters(top_letter, 'e')
        key.append(distance)

        print('For position ' + str(index) + ' a Caesar cipher of ' + str(distance) + ' is expected')

        new_list_decrypted.append(caesar_cipher_decrypt(chunk_text, distance))

    key = ''.join([alphabet[k] for k in key]).upper()
    print('\nThe key expected is: ' + key + '\n')
    print('Decrypted message saved in result.txt\n')

    save_file(reverse_substrings_by_position(new_list_decrypted))


key_length = find_key_length(file, max_length_key_test)
decrypt(file, key_length)