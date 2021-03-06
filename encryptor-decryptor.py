import requests, subprocess, sys, cryptography
from cryptography.fernet import Fernet


def get_lang_and_mode(mode):
    with open("lang.txt","r") as lang_file:
        list_ = lang_file.readlines()
        language = list_[0]
        if mode == "":
            if len(list_) == 2:
                mode = list_[1]
            else:
                mode = "terminal"
        lang_list = list(language)
        if lang_list[-1] == "\n":
            lang_list.pop()
        language = "".join(lang_list)
        if len(list_) >= 2:
            mode = list_[1]
            with open("lang.txt","w") as lang_file:
                lang_file.write(language)
    return language, mode


def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    loop = True
    exit_ = False
    while loop == True:
        while True:
            if language == "English":
                choice = input("Do you want to use the encryption (1) or decryption (2) function? --> ")
            else:
                choice = input("Vuoi usare la funzione di criptazione (1) o decriptazione (2)? --> ")
            if choice.lower() == "exit":
                if language == "English":
                    print("Goodbye!\n")
                else:
                    print("Arrivederci!\n")
                loop = False
                break
            elif choice == "1" or choice == "1.":
                if language == "English":
                    choice_2 = input("Do you want to encrypt a string (1) or a file (2)? --> ")
                else:
                    choice_2 = input("Vuoi criptare una stringa (1) o un file (2)? --> ")
                if choice_2.lower() == "exit":
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                exit_ = encryptor(choice_2, language)
                if exit_ == True:
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                else:
                    break
            elif choice == "2" or choice == "2.":
                if language == "English":
                    choice_2 = input("Do you want to decrypt a string (1) or a file (2)? --> ")
                else:
                    choice_2 = input("Vuoi decriptare una stringa (1) o un file (2)? --> ")
                if choice_2.lower() == "exit":
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                exit_ = decryptor(choice_2, language)
                if exit_ == True:
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                else:
                    break
            else:
                if language == "English":
                    print("You have not entered a valid choice!")
                else:
                    print("Non hai inserito una scelta valida!")
        if loop == True:
            while True:
                if language == "English":
                    choice = input("Do you want to exit the program? [Y/n]: ")
                else:
                    choice = input("Vuoi uscire dal programma? [Y/n]: ")
                choice = choice.lower()
                if choice == "y" or choice == "yes":
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                elif choice == "n" or choice == "no":
                    if language == "English":
                        print("Returning to the menu!\n")
                    else:
                        print("Ritorno al menù!\n")
                    if mode == "menu":
                        with open("lang.txt", "a") as lang_file:
                            lang_file.write("\nmenu")
                        subprocess.Popen("encryptor-decryptor.bat", shell=True)
                        sys.exit()
                    else:
                        break
                else:
                    if language == "English":
                        print("You have not entered a valid choice!")
                    else:
                        print("Non hai inserito una scelta valida!")


def encryptor(choice, language):
    exit_ = False
    write_key()
    key = load_key()
    f = Fernet(key)
    if choice == "1" or choice == "1.":
        if language == "English":
            string = input("Insert the string to encrypt --> ")
        else:
            string = input("Inserisci la stringa da criptare --> ")
        if string.lower() == "exit":
            exit_ = True
        else:
            string = string.encode()
            encrypted_string = f.encrypt(string)
            if language == "English":
                print(f"Done!\nString encrypted: {encrypted_string}")
            else:
                print(f"Fatto!\nStringa criptata: {encrypted_string}")
    else:
        while True:
            if language == "English":
                file_name = input("Insert the name of the file to encrypt --> ")
            else:
                file_name = input("Inserisci il nome del file da criptare --> ")
            if file_name.lower() == "exit":
                exit_ = True
            else:
                try:
                    # file_data = open(file_name).read()
                    with open(file_name, "rb") as file:
                        file_data = file.read()
                    encrypted_data = f.encrypt(file_data)
                    with open(f"{file_name} - Encrypted.txt", "wb") as file:
                        file.write(encrypted_data)
                    if language == "English":
                        print("Done!")
                    else:
                        print("Fatto!")
                    break
                except FileNotFoundError:
                    if language == "English":
                        print("File not found!")
                    else:
                        print("File non trovato!")
    return exit_


def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("key.key", "rb").read()


def decryptor(choice, language):
    exit_ = False
    key = load_key()
    f = Fernet(key)
    if choice == "1" or choice == "1.":
        while True:
            if language == "English":
                encrypted_string = input("Insert the encrypted string --> ")
            else:
                encrypted_string = input("Inserisci la stringa criptata --> ")
            if encrypted_string.lower() == "exit":
                exit_ = True
                break
            else:
                try:
                    encrypted_string = encrypted_string.encode()
                    decrypted_string = f.decrypt(encrypted_string)
                    if language == "English":
                        print(f"Done!\nString decrypted: {decrypted_string}")
                    else:
                        print(f"Fatto!\nStringa decriptata: {decrypted_string}")
                    break
                except Exception:
                    if language == "English":
                        print("You have not entered a valid crypted string!")
                    else:
                        print("Non hai inserito una stringa criptata valida!")
    else:
        while True:
            try:
                if language == "English":
                    file_name = input("Insert the name of the file to decrypt --> ")
                else:
                    file_name = input("Inserisci il nome del file da decriptare --> ")
                if file_name.lower() == "exit":
                    exit_ = True
                else:
                    # file_data = open(file_name.read()).encode()
                    with open(file_name, "rb") as file:
                        encrypted_data = file.read()
                    decrypted_data = f.decrypt(encrypted_data)
                    with open(f"{file_name} - Decrypted.txt", "wb") as file:
                        file.write(decrypted_data)
                    if language == "English":
                        print("Done!")
                    else:
                        print("Fatto!")
                break
            except FileNotFoundError:
                if language == "English":
                    print("File not found!")
                else:
                    print("File non trovato!")
            except cryptography.fernet.InvalidToken:
                if language == "English":
                    print("File not valid!")
                else:
                    print("File non valido!")
    return exit_


if __name__ == "__main__":
    main()
