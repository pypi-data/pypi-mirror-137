import os
from .error import *
import datetime


class Read():
    @staticmethod
    def character_cluster(num, startNum, chars):
        if startNum <= num < startNum + len(chars):
            return chars[num - startNum]
        else:
            return ""

    def __init__(self, file_name, notOut=False, ignoringMeta=False):
        self.name = file_name
        self.meta = False
        self.__Bytes = None
        self.__decoded_text = None
        self.notOut = notOut
        self.ignoringMeta = ignoringMeta
        self.__metaTime = None
        try:
            with open(file_name, "rb") as test:
                pass
        except PermissionError:
            raise Access
        except FileNotFoundError:
            raise Location
        with open(file_name, "rb") as file:
            allBytes = file.read()
            if allBytes[0] == 164 and allBytes[1] == 166 and allBytes[2] == 165:
                Bytes = allBytes.hex()
                Bytes = [Bytes[i:i + 2] for i in range(0, len(Bytes), 2)]
                for num in range(0, len(Bytes)):
                    if not Bytes[num][0].isdigit() and Bytes[num][1] == "0":
                        Bytes[num] = Bytes[num][0]
                if "a8" in Bytes and not ignoringMeta:
                    self.meta = True
                    self.__metaTime = datetime.datetime(
                        int(f"{int(Bytes[4], 16)}{int(Bytes[5], 16)}"), int(Bytes[6], 16),
                        int(Bytes[7], 16), int(Bytes[8], 16), int(Bytes[9], 16))
            else:
                raise FileType
            done = ""
            for e in range(0, len(Bytes)):
                i = int(f"0x{Bytes[e]}", 0)
                if self.meta and e in range(4, 10):
                    continue
                if i in range(3, 13):
                    done += str(i - 3)
                if i == 1:
                    done += "\n"
                if i == 2:
                    done += " "
                done += self.character_cluster(i, 13, "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".lower())
                done += self.character_cluster(i, 46, "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
                done += self.character_cluster(i, 79, "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower())
                done += self.character_cluster(i, 105, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                done += self.character_cluster(i, 131, '.,?!@#$:;"')
                done += self.character_cluster(i, 141, "'[]{}()_-=+*~`&/\^%№<>|")
            if done != "":
                self.__decoded_text = done
            if Bytes != "":
                self.__Bytes = Bytes

    def Out(self):
        if not self.notOut:
            return self.__decoded_text
        else:
            raise OutBlock

    def ByteOut(self, array=True):
        if not self.notOut:
            if array:
                return self.__Bytes
            else:
                return "".join(self.__Bytes)
        else:
            raise OutBlock

    def MetaOut(self, datetime_mode=True):
        if not self.notOut:
            if self.meta:
                if datetime_mode:
                    return self.__metaTime
                else:
                    return f'{int(f"{int(self.__Bytes[4], 16)}{int(self.__Bytes[5], 16)}")}-{int(self.__Bytes[6], 16)}-' \
                           f'{int(self.__Bytes[7], 16)} {int(self.__Bytes[8], 16)}:{int(self.__Bytes[9], 16)}'
            else:
                raise NoneMeta
        else:
            raise OutBlock


def about():
    print(
        "what is it .aef?\n.aef (alternative encoding file) is a simple experiment to create a text encoding.\n"
        "Here each character occupies one byte, there are almost all the characters that are on the keyboard "
        "(except special characters).\nThere is metadata in the form of the file creation date. "
        "\nAt the beginning of the file there are three special characters that are contained in this encoding, "
        "\nwith the help of them the program can determine that this is a .aef extension file.\n"
        "The experiment will continue.")
