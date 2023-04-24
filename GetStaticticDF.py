import sqlite3

import numpy as np
import pandas as pd
import pprint

from pandas import Series


def statistic_table():
    con = sqlite3.connect(r"\\projects\StranaDev_Family\999 BIM\FamilyManager\Статистика\FM_statistics.db")
    df = pd.read_sql_query("SELECT * FROM UserAction", con)
    df = df.rename({'CommandName': 'Имя команды', 'Time': 'Дата'}, axis=1)
    df['Дата'] = pd.to_datetime(df['Дата'], unit='s').dt.strftime('%d %b %Y')
    df['Имя команды'] = df['Имя команды'].replace("ItemSelect", "Разместить эл-т") \
        .replace("UpdateFamilies", "Обновить все сем-ва").replace("DownloadMaterials", "Загрузить материалы") \
        .replace("LoadTypesInPJ", "Выбрать типы и загрузить").replace("SelectAllTypesInPJ", "Выделить все типы сем-ва") \
        .replace("SelectAllTypesInPJinActiveView", "Выделить все типы сем-ва на виде") \
        .replace("SelectTypeInPJ", "Выделить тип в проекте").replace("SelectTypeInPJinActiveView",
                                                                     "Выделить тип на виде") \
        .replace("UpdateTypesInPJ", "Обновить сем-во").replace("LoadSelectedTypesInPJ", "Загрузить выбранные типы")
    df['Project'] = df.apply(lambda row: str(row[5]).split("\\")[-1].split(".")[0], axis=1)
    return df


def family_table():
    con = sqlite3.connect(r"\\projects\StranaDev_Family\999 BIM\FamilyManager\family_db.db")
    df = pd.read_sql_query("SELECT * FROM Familiрes", con)
    return df


def family_history_table():
    con = sqlite3.connect(r"\\projects\StranaDev_Family\999 BIM\FamilyManager\family_db.db")
    df = pd.read_sql_query("SELECT * FROM family_history", con)

    return df


def table_for_time_line_graf(df): # требуется сосчитать сумму по столбцам такая то команда такая то дата число использований
    df_grouped = df.groupby(by="Дата")["Имя команды"].value_counts().reset_index()
    df_grouped = df_grouped.rename({'count': 'Число использований'}, axis=1)
    return df_grouped




if __name__ == '__main__':
    statistic_table()
