/*Запрос получения списка имён колонок у таблицы.*/
SELECT
    column_name
FROM
    information_schema.columns
WHERE
    table_name = 'new_table';