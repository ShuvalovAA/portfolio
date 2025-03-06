# -*- coding: utf-8 -*-
from typing import Optional, Tuple, Any
from tqdm import tqdm
from django.db import connections
from django.core.management.base import BaseCommand
from psycopg2.extras import DictCursor


class QueryBuilder:
    """Класс построения запросов."""

    def __init__(
        self,
        new_table   # type: str
    ):
        # type: (...) -> None
        """Инициализация класса."""
        self.new_table = new_table
        self.old_table = new_table + '_old'

    def get_sql_get_column_names(self):
        # type: () -> str
        """Метод получения запроса на список имён столбцов таблицы."""
        sql_query = """
            SELECT
                column_name
            FROM
                information_schema.columns
            WHERE
                table_name = '{new_table}'
        """
        return sql_query.format(new_table=self.new_table)

    def get_sql_old_table_max_id(self):
        # type: () -> str
        """Метод получения запроса на максимальный id в старой табилце."""
        sql_query = """
            SELECT
                max(id)
            FROM
                {old_table}
        """
        return sql_query.format(old_table=self.old_table)

    def get_sql_get_chunk_for_update(
        self,
        start,  # type: int
        end     # type: int
    ):
        # type: (...) -> str
        """Метод получения запроса на id для обновления строк из старой таблицы."""
        sql_query = """
            SELECT
                id
            FROM
                {old_table}
            ORDER BY
                id
            OFFSET {start}
            LIMIT {end}
        """
        return sql_query.format(old_table=self.old_table, start=start, end=end)

    def get_sql_get_chunk_for_delete(
        self,
        old_table_max_id,   # type: int
        start,              # type: int
        end                 # type: int
    ):
        # type: (...) -> str
        """Метод получения запроса на id для удаления строк из новой таблицы."""
        sql_query = """
            SELECT
                id
            FROM
                {new_table}
            WHERE
                id <= {old_table_max_id}
            ORDER BY
                id
            OFFSET {start}
            LIMIT {end}
        """
        return sql_query.format(new_table=self.new_table, old_table_max_id=old_table_max_id, start=start, end=end)

    def get_sql_update(
        self,
        chunk,          # type: Tuple[int]
        names_list      # type: Tuple[str]
    ):
        # type: (...) -> str
        """Метод получения запроса на обновления строк."""
        def _prepare_chunk_str(chunk):
            return chunk if len(chunk) > 1 else (chunk[0], chunk[0])

        def _get_column_names_list_for_query(names_list):
            return ', '.join(['{name}=t0.{name}'.format(name=name) for name in names_list])

        sql_query = """
            UPDATE
                {new_table} as t1
            SET
                {columns}
            FROM
                {old_table} as t0
            WHERE
                age(t1.xmin) > age(t0.xmin) AND t1.id=t0.id
                AND t0.id in {chunk}
        """
        return sql_query.format(
            new_table=self.new_table,
            columns=_get_column_names_list_for_query(names_list),
            old_table=self.old_table,
            chunk=chunk
        )

    def get_sql_delete(
        self,
        chunk   # type: Tuple[int]
    ):
        # type: (...) -> str
        """Метод получения запроса на удаления строк."""
        sql_query = """
            DELETE FROM
                {new_table}
            WHERE
                NOT EXISTS (
                    SELECT 1
                    FROM
                        {old_table}
                    WHERE
                        id = {new_table}.id
                )
                AND {new_table}.id in {chunk}
        """
        return sql_query.format(
            new_table=self.new_table,
            chunk=chunk,
            old_table=self.old_table
        )


class SyncHandler:
    """Класс процесса синхронизации данных после переноса данных в другую таблицу."""

    def __init__(
        self,
        query_builder,      # type: QueryBuilder
        database,           # type: str
        chunk_size=2000     # type: Optional[int]
    ):
        # type: (...) -> None
        """Инициализация класса."""
        self.query_builder = query_builder
        self.database = database
        self.chunk_size = chunk_size

    def _execute_query_with_fetchall(
        self,
        query,          # type: str
        column_name     # type: str
    ):
        # type: (...) -> Tuple[Any]
        """Метод исполнения запроса для выборки данных всех полученных строк."""
        with connections[self.database].cursor() as cursor_wrapper:
            dict_cur = cursor_wrapper.cursor.connection.cursor(cursor_factory=DictCursor)
            dict_cur.execute(query)
            result = dict_cur.fetchall()
        return tuple([row[column_name] for row in result])

    def _execute_query_with_fetchone(
        self,       
        query,          # type: str
        column_name     # type: str
    ):
        # type: (...) -> Any
        """Метод исполнения запроса для выборки данных одной полученной строки."""
        with connections[self.database].cursor() as cursor_wrapper:
            dict_cur = cursor_wrapper.cursor.connection.cursor(cursor_factory=DictCursor)
            dict_cur.execute(query)
            result = dict_cur.fetchone()
        return result[column_name]

    def _execute_query(
        self,
        query   # type: str
    ):
        # type: (...) -> None
        """Метод исполнения запроса."""
        with connections[self.database].cursor() as cursor:
            cursor.execute(query)

    def _sync_updated_rows(
        self,
        max_id  # type: int
    ):
        # type: (...) -> None
        """Метод синхронизации строк, которые были обновлены пока делали миграцию."""
        sql_get_column_names = self.query_builder.get_sql_get_column_names()
        column_names = self._execute_query_with_fetchall(sql_get_column_names, 'column_name')
        for row_num_start in tqdm(
            range(0, max_id + self.chunk_size, self.chunk_size),
            desc='sync_updated_rows'
        ):
            sql_get_chunk_for_update = self.query_builder.get_sql_get_chunk_for_update(row_num_start, self.chunk_size)
            chunk = self._execute_query_with_fetchall(sql_get_chunk_for_update, 'id')
            if not chunk:
                continue
            
            chunk = tuple([int(i) for i in chunk])
            sql_update = self.query_builder.get_sql_update(chunk, column_names)
            self._execute_query(sql_update)

    def _sync_delete_rows(
        self,
        max_id  # type: int
    ):
        # type: (...) -> None
        """Метод синхронизации строк, которые были удалены пока делали миграцию."""
        for row_num_start in tqdm(
            range(0, max_id + self.chunk_size, self.chunk_size),
            desc='sync_delete_rows'
        ):
            sql_get_chunk_for_delete = self.query_builder.get_sql_get_chunk_for_delete(
                old_table_max_id=max_id,
                start=row_num_start,
                end=self.chunk_size
            )
            chunk = self._execute_query_with_fetchall(query=sql_get_chunk_for_delete, column_name='id')
            if not chunk:
                continue
            
            chunk = tuple([int(i) for i in chunk])
            sql_delete = self.query_builder.get_sql_delete(chunk)
            self._execute_query(sql_delete)

    def start_process(self):
        """Запуск процесса синхронизации."""
        query_old_table_max_id = self.query_builder.get_sql_old_table_max_id()
        old_table_max_id = self._execute_query_with_fetchone(
            query=query_old_table_max_id,
            column_name='max'
        )
        if old_table_max_id:
            self._sync_updated_rows(old_table_max_id)
            self._sync_delete_rows(old_table_max_id)


class Command(BaseCommand):
    """Команда для синхронизации таблиц после ручной  миграции.

    Покрывает кейс, когда мы меняем схему данных через создания новой таблицы.
    Например, нам нужно сменить у поля большой таблицы тип данных.
    После ручных операций данная команда позволит покрыть кейс, когда
    нам требуется согласовать данные старой таблицы и новой.

    Пример запуска команды:
        ./manage.py data_migrated_table_sync --table_name mytable --database default
    """

    def add_arguments(self, parser):
        parser.add_argument('--table_name', dest='table_name', type=str)
        parser.add_argument('--database', dest='database', type=str)

    def handle(self, *args, **options):
        table_name = options.get('table_name')
        database = options.get('database')
        query_builder = QueryBuilder(new_table=table_name)

        handler = SyncHandler(
            query_builder=query_builder,
            database=database
        )
        handler.start_process()
