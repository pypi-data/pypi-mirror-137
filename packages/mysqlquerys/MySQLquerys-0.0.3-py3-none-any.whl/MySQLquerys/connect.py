# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 19:58:48 2021

@author: -
https://www.postgresqltutorial.com/postgresql-python/connect/
"""

import mysql.connector as misql
import traceback
import sys
import csv
from datetime import datetime
import json
from MySQLquerys.config import config


class DbConnection:
    def __init__(self, db_type='MySQL'):
        self.iniFile = r"D:\Python\MySQL\SQL_Query\database.ini"
        self.data_base_type = db_type
        try:
            params = config(filename=self.iniFile, section=db_type)
            self.connection = misql.connect(**params)
        except Exception as err:
            print(err)

    @property
    def version(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        cursor.close()
        return db_version

    @property
    def databases(self):
        cursor = self.connection.cursor()
        cursor.execute('SHOW DATABASES')
        dbase = cursor.fetchall()
        dataBases = []
        for i in dbase:
            if i[0] == 'information_schema' or i[0] == 'performance_schema' or i[0] == 'mysql' or i[0] == 'sys':
                continue
            dataBases.append(i[0])
        cursor.close()
        return dataBases
    
    @property
    def active_data_base(self):
        return self.dataBase

    @active_data_base.setter
    def active_data_base(self, data_base_name):
        self.dataBase = DataBase(self.data_base_type, data_base_name)

    def drop_data_base(self, schema_name):
        cursor = self.connection.cursor()
        query = 'DROP SCHEMA {}'.format(schema_name)
        cursor.execute(query)
        cursor.close()

    def create_data_base(self, schema_name):
        try:
            cursor = self.connection.cursor()
            query = 'CREATE SCHEMA {}'.format(schema_name)
            cursor.execute(query)
            cursor.close()
        except misql.Error as err:
            print('mysql.Error', err.msg)
        except Exception:
            print(traceback.format_exc())
        else:
            print('successfully executed query: ', query)


class DataBase(DbConnection):
    def __init__(self, db_type, data_base_name):
        super().__init__(db_type)
        self.connection.database = data_base_name
        self.data_base_name = data_base_name

    def drop_table(self, tableName):
        cursor = self.connection.cursor()
        query = 'DROP TABLE {}'.format(tableName)
        cursor.execute(query)
        cursor.close

    @property
    def tables(self):
        cursor = self.connection.cursor()
        cursor.execute('SHOW tables')
        tabs = cursor.fetchall()
        tables = []
        for i in tabs:
            tables.append(i[0])
        cursor.close()
        return tables

    @property
    def active_table(self):
        return self.table

    @active_table.setter
    def active_table(self, table_name):
        self.table = Table(self.data_base_type, self.data_base_name, table_name)

    def createTableFromFile(self, file):
        print(sys._getframe().f_code.co_name)
        # print(file)
        cursor = self.connection.cursor()
        if isinstance(file, str):
            commands = file.split(';')
        for command in commands:
            print('executing command: ', command)
            cursor.execute(command)

    def renameTable(self, oldTableName, newTableName):
        query = "RENAME TABLE {} TO {}".format(oldTableName, newTableName)
        cursor = self.connection.cursor()
        cursor.execute(query)
        cursor.close()

    def deleteAllRows(self, table_name):
        query = 'DELETE FROM {}'.format(table_name)
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()


class Table(DataBase):
    def __init__(self, db_type, data_base_name, table_name):
        super().__init__(db_type, data_base_name)
        self.table_name = table_name

    @property
    def tableProperties(self):
        query = 'SHOW CREATE TABLE {}'.format(self.table_name)
        cursor = self.connection.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        cursor.close()
        return res[1]

    @property
    def columnsNames(self):
        query = 'DESC {}'.format(self.table_name)
        cursor = self.connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cols = []
        for col in res:
            cols.append(col[0])
        cursor.close()
        return cols

    @property
    def columnsProperties(self):
        query = 'DESC {}'.format(self.table_name)
        colNames = ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra']
        cursor = self.connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cols = {}
        for col in res:
            colName, colType, null, key, default, extra = col
            colType = str(colType.decode("utf-8"))
            cols[colName] = [colType, null, key, default, extra]
        cursor.close()
        return cols

    @property
    def noOfRows(self):
        query = 'SELECT * FROM {}'.format(self.table_name)
        cursor = self.connection.cursor()
        cursor.execute(query)
        cursor.fetchall()
        rowNo = cursor.rowcount
        cursor.close()
        return rowNo

    @property
    def data(self):
        query = 'SELECT * FROM {}'.format(self.table_name)
        cursor = self.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return records

    def get_column_type(self, column):
        colProps = self.columnsProperties[column]
        colType = colProps[0]
        return colType

    def add_row(self, columns, values):
        print(len(columns), len(values))
        strCols = (('{}, ' * len(columns)).format(*columns))
        strCols = '({})'.format(strCols[:-2])
        strVals = ('%s,'*len(columns))
        strVals = '({})'.format(strVals[:-1])

        query = "INSERT INTO {} {} VALUES {}".format(self.table_name, strCols, strVals)
        #######
        print(query)
        for i in range(len(columns)):
            print(columns[i], values[i])
        #######
        if isinstance(values, int):
            values = (values, )
        elif isinstance(values, str):
            values = (values,)

        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

        return cursor.lastrowid

    def modify2AutoIncrement(self, column, colType):
        query = 'ALTER TABLE {} MODIFY {} {} AUTO_INCREMENT;'.format(self.table_name, column, colType)
        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()

    def modifyType(self, column, colType):
        query = 'ALTER TABLE {} MODIFY {} {};'.format(self.table_name, column, colType)
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()

    def deleteRow(self, condition):
        colName, value = condition
        query = 'DELETE FROM {} WHERE {} = {} '.format(self.table_name, colName, value)
        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query, value)
        self.connection.commit()
        cursor.close()

    def changeCellContent(self, column2Modify, val2Moify, refColumn, refValue):
        query = "UPDATE {} SET {} = %s WHERE {} = %s".format(self.table_name, column2Modify, refColumn)
        # print(query)
        cursor = self.connection.cursor()
        vals = (val2Moify, refValue)
        # print(vals)
        cursor.execute(query, vals)
        self.connection.commit()
        cursor.close()

    def dropColumn(self, column2Del):
        query = "ALTER TABLE {} DROP COLUMN %s;".format(self.table_name)
        query = "ALTER TABLE {} DROP COLUMN {};".format(self.table_name, column2Del)
        print(query)
        cursor = self.connection.cursor()
        # vals = (column2Del, )
        cursor.execute(query)
        self.connection.commit()
        cursor.close()

    def executeQuery(self, query):
        print(sys._getframe().f_code.co_name)
        # print(file)
        cursor = self.connection.cursor()
        if isinstance(query, str):
            commands = query.split(';')
        for command in commands:
            print('executing command: ', command)
            cursor.execute(command)

    def filterRows(self, matches):
        filterText = ''
        for match in matches:
            search_col, search_key = match
            if isinstance(search_key, tuple):
                min, max = search_key
                new = "{} > '{}' AND {} < '{}' AND ".format(search_col, min, search_col, max)
                filterText += new
            elif isinstance(search_key, list):
                new = "{} IN {} AND ".format(search_col, tuple(search_key))
                filterText += new
            else:
                new = "{} = '{}' AND ".format(search_col, search_key)
                filterText += new

        query = "SELECT * FROM {} WHERE ".format(self.table_name) + filterText[:-4]
        cursor = self.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return records

    def importCSV(self, inpFile):
        with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
            linereader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for i, row in enumerate(linereader):
                if i == 0:
                    tableHead = row
                    continue
                if '' in row or 'None' in row:
                    new_strings = []
                    for string in row:
                        if string == '' or string == 'None':
                            new_strings.append(None)
                        else:
                            new_strings.append(string)
                    row = new_strings
                self.add_row(tableHead, row)

    def importSparkasseCSV(self, inpFile):
        with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
            linereader = csv.reader(csvfile, delimiter=';', quotechar='"')
            indxBuchungstag = self.columnsNames.index('Buchungstag')
            indxValutDatum = self.columnsNames.index('Valutadatum')
            indxBetrag = self.columnsNames.index('Betrag')
            for i, row in enumerate(linereader):
                # print(row)
                row.insert(0, i)
                if i == 0:
                    tableHead = row
                    continue
                if '' in row or 'None' in row:
                    new_strings = []
                    for string in row:
                        if string == '' or string == 'None':
                            new_strings.append(None)
                        else:
                            new_strings.append(string)
                    row = new_strings
                buchungstag = row[indxBuchungstag]
                valutDatum = row[indxValutDatum]
                betrag = row[indxBetrag]
                betrag = float(betrag.replace(',', '.'))
                buchungstag = self.convertDatumFormat4SQL(buchungstag)
                valutDatum = self.convertDatumFormat4SQL(valutDatum)

                row[indxBuchungstag] = buchungstag
                row[indxValutDatum] = valutDatum
                row[indxBetrag] = betrag
                self.add_row(self.columnsNames, row)

    def convertDatumFormat4SQL(self, datum):
        # print(sys._getframe().f_code.co_name)
        # newDate = datetime.strptime(datum, '%d.%m.%y')
        for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%m/%d/%Y', '%d.%m.%y'):
            try:
                newDate = datetime.strptime(datum, fmt)
                return newDate.date()
            except ValueError:
                pass
        raise ValueError('no valid date format found')

    def convertTimeFormat4SQL(self, time):
        # print(sys._getframe().f_code.co_name)
        # newDate = datetime.strptime(datum, '%d.%m.%y')
        for fmt in ('%H:%M', '%H:%M:%S'):
            try:
                newDate = datetime.strptime(time, fmt)
                return newDate.time()
            except ValueError:
                pass
        raise ValueError('no valid date format found')

    def returnColumn(self, col):
        query = 'SELECT {} FROM {}'.format(col, self.table_name)
        cursor = self.connection.cursor()
        # vals = (column2Del, )
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        values = []
        for i in records:
            values.append(i[0])
        return values

    def returnColumns(self, cols):
        strTableHead = ''
        for col in cols:
            strTableHead += '{}, '.format(col)
        strTableHead = strTableHead[:-2]

        query = 'SELECT {} FROM {}'.format(strTableHead, self.table_name)
        cursor = self.connection.cursor()
        # vals = (column2Del, )
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        values = []
        for i in records:
            values.append(i)
        return values

    def returnCellsWhere(self, col, matches):
        if isinstance(matches, tuple):
            searchCol, searchKey = matches
            if isinstance(searchKey, str) or isinstance(searchKey, int):
                query = "SELECT {} FROM {} WHERE {} = '{}'".format(col, self.table_name, searchCol, searchKey)
            if isinstance(searchKey, tuple):
                query = "SELECT {} FROM {} WHERE {} IN {}".format(col, self.table_name, searchCol, searchKey)
        elif isinstance(matches, list):
            text = ''
            for i in matches:
                searchCol, searchKey = i
                new = '{} = "{}" AND '.format(searchCol, searchKey)
                text += new
            query = "SELECT {} FROM {} WHERE ".format(col, self.table_name) + text[:-4]
        else:
            raise TypeError('{} must be tuple or list of tuples'.format(matches))

        cursor = self.connection.cursor()
        # print('query', query)
        cursor.execute(query)
        records = cursor.fetchall()
        # print(records)
        cursor.close()
        values = []
        colType = self.get_column_type(col)
        for i in records:
            if colType == 'json':
                values.append(json.loads(i[0]))
            else:
                values.append(i[0])
        return values

    def returnColsWhere(self, cols, matches):
        relCols = ''
        for col in cols:
            relCols += '{}, '.format(col)
        relCols = relCols[:-2]

        if isinstance(matches, tuple):
            searchCol, searchKey = matches
            if isinstance(searchKey, str) or isinstance(searchKey, int):
                query = "SELECT {} FROM {} WHERE {} = '{}'".format(relCols, self.table_name, searchCol, searchKey)
            if isinstance(searchKey, tuple):
                query = "SELECT {} FROM {} WHERE {} IN '{}'".format(relCols, self.table_name, searchCol, searchKey)
            if searchKey is None:
                query = "SELECT {} FROM {} WHERE {} IS NULL".format(relCols, self.table_name, searchCol)
        elif isinstance(matches, list):
            text = ''
            for i in matches:
                searchCol, searchKey = i
                if searchKey is None:
                    new = '{} IS NULL AND '.format(searchCol)
                else:
                    new = '{} = "{}" AND '.format(searchCol, searchKey)
                text += new
            query = "SELECT {} FROM {} WHERE ".format(relCols, self.table_name) + text[:-4]
        else:
            raise TypeError('{} must be tuple or list of tuples'.format(matches))

        cursor = self.connection.cursor()
        # print('query', query)
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        values = []
        for i in records:
            values.append(i)
        return values

    def returnRowsWhere(self, matches):
        if isinstance(matches, tuple):
            searchCol, searchKey = matches
            if isinstance(searchKey, str) or isinstance(searchKey, int):
                query = "SELECT * FROM {} WHERE {} = '{}'".format(self.table_name, searchCol, searchKey)
            if isinstance(searchKey, tuple):
                query = "SELECT * FROM {} WHERE {} IN '{}'".format(self.table_name, searchCol, searchKey)
            if searchKey is None:
                query = "SELECT * FROM {} WHERE {} IS NULL".format(self.table_name, searchCol)
        elif isinstance(matches, list):
            text = ''
            for i in matches:
                searchCol, searchKey = i
                if searchKey is None:
                    new = '{} IS NULL AND '.format(searchCol)
                else:
                    new = '{} = "{}" AND '.format(searchCol, searchKey)
                text += new
            query = "SELECT * FROM {} WHERE ".format(self.table_name) + text[:-4]
        else:
            raise TypeError('{} must be tuple or list of tuples'.format(matches))

        cursor = self.connection.cursor()
        # print('query', query)
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        values = []
        for i in records:
            values.append(i)
        return values

    # def unionTables(self):
    #     query =


if __name__ == '__main__':
    try:
        db = DbConnection('MySQL')
        print(db.version)

        # dataBase = DataBase('MySQL', 'cheltuieli')
        # print(dataBase.tables)

        table = Table('MySQL', 'cheltuieli', 'real_expenses')
        table = Table('MySQL', 'myfolderstructure', 'apartament')

    except Exception as error:
        print(error)
