/*Запрос обновления строк в целевой таблице на основе возвраста версии строк в исходной таблице.*/

UPDATE
    new_table as t1
SET
    t1.column = t0.column 
FROM
    old_table as t0
WHERE
    /*чем age меньше, тем "свежее" версия строки*/
    age(t1.xmin) > age(t0.xmin) AND t1.id=t0.id
    AND t0.id in (1, 2, 3);