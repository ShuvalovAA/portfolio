# Основное

## Показать права на таблицу
```SQL
    SELECT grantee, privilege_type
	FROM information_schema.role_table_grants
	WHERE table_name='{name_table}';
```

## Показать блокировки таблицы
```SQL
    select t.relname, l.locktype, page, virtualtransaction, pid, mode, granted
    from pg_locks l, pg_stat_all_tables t
    where l.relation=t.relid
    order by relation asc;
```
## Показать долгие запросы
```SQL
    select pid, now() - pg_stat_activity.query_start as duration, query 
    from pg_stat_activity 
    where (now() - pg_stat_activity.query_start) > interval '2 minutes';
```
## Анализ запроса выполнив его
```SQL
EXPLAIN analyze  {my_sql_query}
```

## Почистить ВСЕ коннекты
```SQL
    Select 
    _terminate_backend(pid)  from pg_stat_activity where pid <> pg_backend_pid() AND datname = '{db_name}' ;
```

## войти принудительно
`sudo -u postgres psql`

Конфликтующие и блокирующие команды - https://pglocks.org/

### перенос дампа схемы:
* получить только схему: `pg_dump  -U postgres -d {db_name} --schema-only   >> 'dump.sql'`
* закинуть схему: `psql -U postgres {db_name} < dump.sql`

## Пример, где лежат логи
`/data/postgres/bk-01/pg_log/postgresql-2024-09-17_0000.log`