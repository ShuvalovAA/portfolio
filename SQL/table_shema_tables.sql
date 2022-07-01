SELECT reference_to,
        attr1.attname AS source_key,
        reference_from,
        attr2.attname AS referencing_key
FROM 
    (SELECT t.conkey,
        t.confkey,
        cast(shema_table.confrelid:: regclass AS varchar) AS reference_to,
        shema_table.conrelid:: regclass AS reference_from,
        confrelid,
        conrelid
    FROM pg_constraint AS shema_table
    CROSS JOIN unnest(shema_table.conkey, shema_table.confkey) AS t(conkey, confkey)
    WHERE shema_table.contype = 'f' ) AS shema_table_result
LEFT JOIN pg_attribute attr1
    ON attr1.attnum = shema_table_result.confkey
        AND attr1.attrelid = shema_table_result.confrelid
LEFT JOIN pg_attribute attr2
    ON attr2.attnum = shema_table_result.conkey
        AND attr2.attrelid = shema_table_result.conrelid
            