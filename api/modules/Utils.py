import datetime


def validateTypes(content, types):
    """
    Verifica os tipos do content com os types

    :param content: conteudo a verificar
    :param types: tipos para corresponderem

    :return: boolean
    """
    if type(content) is dict:
        content = list(content.values())
    for i in range(len(content)):
        if type(content[i]) is not types[i] or types[i] is None:
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
    d = "2021-06-10 00:00"
    print(validateDates([d]))
