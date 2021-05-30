import datetime
import re


def isemail(string):
    """
    Verifica se uma string é um email

    :param string: email a verificar

    :return: boolean
    """
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.search(regex, string):
        return True
    return False


def isfloat(string):
    """
    Verifica se uma string é um float

    :param string: string a verificar

    :return: boolean
    """
    try:
        float(string)
    except ValueError:
        return False
    return True


def isint(string):
    """
    Verifica se um numero é um inteiro

    :param string: string a verificar

    :return: boolean
    """
    try:
        int(string)
    except ValueError:
        return False
    return True


def validateTypes(content, types):
    """
    Verifica os tipos do content com os types

    :param content: conteudo a verificar
    :param types: tipos para corresponderem

    :return: boolean
    """
    assert len(content) == len(types), "'content' list and 'types' list does not have the same length!"

    if type(content) is dict:
        content = list(content.values())
    for i in range(len(content)):
        if type(content[i]) is not types[i] or types[i] is None:
            if type(content[i]) is str:
                if types[i] is int and isint(content[i]):
                    continue
                elif types[i] is float and isfloat(content[i]):
                    continue
            return False
    return True


def validateDates(dateList):
    """
    Verifica o formato de uma lista de datas

    :param dateList: lista de datas

    :return: boolean
    """
    isvalid = True
    for date in dateList:
        isvalid = isvalid & validateDate(date)
    return isvalid


def validateDate(date):
    """
    Verifica se a data tem um dos seguintes formatos:\n
    - %Y-%m-%d %H:%M:%S \n
    - %Y/%m/%d %H:%M:%S \n
    - %Y-%m-%d %H:%M \n
    - %Y/%m/%d %H:%M \n

    :param date: data

    :return: boolean
    """
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M'):
        try:
            datetime.datetime.strptime(date, fmt)
            return True
        except ValueError:
            pass
    return False


if __name__ == '__main__':
    pass
