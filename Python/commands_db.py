# /usr/bin/python3.12

"""Скрипт удаления данных по таблице
"""
import aiopg
import asyncio
import argparse
import typer
import json
from typing import Tuple, Dict, List, Union
from typing_extensions import Annotated
from progress.bar import IncrementalBar
from contextlib import asynccontextmanager


# OPTIONS FOR SCRIPTS

TABLES_LIST_DICTS: List[Dict[str, str]] = [
    {'table_name': 'push2' 'marker_field': 'update_date'},
    {'table_name': 'push1', 'marker_field': 'create_date'},
]
MARKER_OPERATOR_KEY: int = 1
MARKER_POINT: str = '2024-01-01'


class ConnectorPG:
    """Коннектор для PG.

        table_name: str -
        field_marker: str -
        marker_type_key: int -
        marker_point: str -
    """

    PG_DATABASE: str = ''
    PG_USER: str = ''
    PG_PASSWORD: str = ''
    PG_HOST: str = ''
    DSN: str = f'dbname={PG_DATABASE} user={PG_USER} password={PG_PASSWORD} host={PG_HOST}'
    LIMIT_FOR_SELECT = 20000

    def __init__(
        self,
        table_name: str,
        marker_field: str,
        marker_operator_key: int,
        marker_point: str
    ) -> None:
        self.table_name = table_name
        self.marker_field = marker_field
        self.marker_point = marker_point
        self.marker_operator = self.marker_operator_map.get(marker_operator_key)
        if not self.marker_operator:
            raise TypeError('Premission marker_operator_key: 1, 2')

    @property
    def marker_operator_map(self):
        map: Dict[int, str] = {1: '<', 2: '>'}
        return map

    async def _run_query(self, sql: str):
        """Выполнить запрос."""
        async with self._get_connect_cursor() as cursor_method:
            cursor = await cursor_method()
            await cursor.execute(sql)
            return await cursor.fetchall()

    @asynccontextmanager
    async def _get_connect(self):
        """Получить соедние с PG."""
        async with aiopg.connect(self.DSN) as con:
            yield con

    @asynccontextmanager
    async def _get_connect_cursor(self):
        """Получить курсор для PG."""
        async with self._get_connect() as connect:
            try:
                yield connect.cursor
            finally:
                connect.close()

    async def delete_rows(self, tuple_ids: Tuple[int]) -> None:
        """Удалить записи."""
        query = f'''
            DELETE FROM {self.table_name} WHERE id in {tuple_ids}
        '''
        print(query)
        # await self._run_query(sql=QUERY)

    async def get_chunck_rows(self) -> Tuple[int]:
        """Получить чанк строк."""
        query = f'''
            SELECT
                id
            FROM
                {self.table_name}
            WHERE
                    to_char({self.marker_field},'YYYY-mm-dd') {self.marker_operator} '{self.marker_point}'
                AND
                    partner_id not in (1860, 1938, 2303, 2164)
            LIMIT {self.LIMIT_FOR_SELECT}
        '''
        breakpoint()
        tuple_ids = await self._run_query(sql=query)
        tuple_ids = tuple([el[0] for el in tuple_ids])
        return tuple_ids

    async def get_total_count(self) -> Tuple[int]:
        """Получить количество строк под удаление."""
        query = f'''
            SELECT
                count(*)
            FROM
                {self.table_name}
            WHERE
                    to_char({self.marker_field},'YYYY-mm-dd') {self.marker_operator} '{self.marker_point}'
        '''
        # total_count = await self._run_query(sql=query)
        total_count = 812439616
        return total_count


class BaseStarter:
    """Базовый класс стартетров команд."""
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name


class DeleteStarter(BaseStarter):
    """Класс стартера процесса удаления данных из таблицы."""

    def __init__(
        self,
        table_name: str,
        marker_field: str,
        marker_operator_key: int,
        marker_point: str
    ) -> None:
        super().__init__(table_name)
        self.marker_field = marker_field
        self.marker_operator_key = marker_operator_key
        self.marker_point = marker_point

    async def run(self):
        """Начать процесс удаления данных."""

        must_do = True
        connector = ConnectorPG(
            table_name=self.table_name,
            marker_field=self.marker_field,
            marker_operator_key=self.marker_operator_key,
            marker_point=self.marker_point
        )
        total_count = await connector.get_total_count()
        progress_bar = IncrementalBar(
            f'DELETE FROM {connector.table_name}',
            max=int(total_count / connector.LIMIT_FOR_SELECT),
        )

        while must_do:
            tuple_ids = await connector.get_chunck_rows()
            if not tuple_ids:
                must_do = False
                progress_bar.finish()
                continue
            progress_bar.next()
            await connector.delete_rows(tuple_ids)
        progress_bar.finish()


if __name__ == '__main__':


    for table_dict in TABLES_LIST_DICTS:
        asyncio.run(
            DeleteStarter(
                table_name=table_dict['table_name'],
                marker_field=table_dict['marker_field'],
                marker_operator_key=MARKER_OPERATOR_KEY,
                marker_point=MARKER_POINT
            ).run()
        )
