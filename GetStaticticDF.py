import sqlite3

import pandas as pd


def statistic_table():
    con = sqlite3.connect(r"C:\Users\gette.e\Desktop\FM_statistics.db")
    df = pd.read_sql_query("SELECT * FROM UserAction", con)
    df = df.rename({'CommandName': 'Имя команды', 'Time': 'Дата'}, axis=1)
    df['Дата'] = pd.to_datetime(df['Дата'], unit='s').dt.strftime('%d %b %Y')
    df['Имя команды'] = df['Имя команды'].replace("ItemSelect", "Разместить эл-т") \
        .replace("UpdateFamilies", "Обновить все сем-ва").replace("DownloadMaterials", "Загрузить материалы") \
        .replace("LoadTypesInPJ", "Выбрать типы и загрузить").replace("SelectAllTypesInPJ",
                                                                      "Выделить все типы сем-ва") \
        .replace("SelectAllTypesInPJinActiveView", "Выделить все типы сем-ва на виде") \
        .replace("SelectTypeInPJ", "Выделить тип в проекте").replace("SelectTypeInPJinActiveView",
                                                                     "Выделить тип на виде") \
        .replace("UpdateTypesInPJ", "Обновить сем-во").replace("LoadSelectedTypesInPJ", "Загрузить выбранные типы")
    df['Project'] = df.apply(lambda row: str(row[5]).split("\\")[-1].split(".")[0], axis=1)
    return df


def family_table():
    con = sqlite3.connect(r"\\projects\StranaDev_Family\999 BIM\FamilyManager\family_db.db")
    df = pd.read_sql_query("SELECT * FROM Families", con)
    return df


def family_history_table():
    con = sqlite3.connect(r"\\projects\StranaDev_Family\999 BIM\FamilyManager\family_db.db")
    df = pd.read_sql_query("SELECT * FROM family_history", con)
    df = df.rename({'Data': 'Дата'}, axis=1)
    df['Дата'] = pd.to_datetime(df['Дата'], unit='s').dt.strftime('%d %b %Y')
    df["Creater"] = df["Creater"].str.lower()
    return df


def table_for_time_line_graf(
        df):  # требуется сосчитать сумму по столбцам такая то команда такая то дата число использований
    df_grouped = df.groupby(by="Дата")["Имя команды"].value_counts().reset_index(name='count')
    df_grouped = df_grouped.rename({'count': 'Число использований'}, axis=1)
    return df_grouped


def table_for_bim_time_line_graf(df):
    df_grouped = df.groupby(by="Дата")["Creater"].value_counts().reset_index(name='count')
    df_grouped = df_grouped.rename({'count': 'Число внесенных изменений'}, axis=1)
    return df_grouped


def family_news_table(df, family_table):
    df = df.rename({'Name': 'Имя семейства', 'Version': 'Версия', 'Comment': 'Комментарий к версии',
                    'Creater': 'Разработчик', 'Types': 'Типы семейств'}, axis=1)
    # Добавить в DateFraim колонку с разделом
    def chapter(row, family_table):
        ttt = family_table[family_table['Name'] == row[0]].reset_index()
        return ttt.KeyWords[0]

    df['Раздел'] = df.apply(lambda row: chapter(row, family_table), axis=1)

    return df[["Имя семейства", "Комментарий к версии", "Версия",
               "Разработчик", 'Раздел', "Дата"]]


if __name__ == '__main__':
    FullTable = statistic_table()
    TimeLineStat = table_for_time_line_graf(FullTable)
