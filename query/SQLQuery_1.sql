SELECT 
    col.COLUMN_NAME, 
    col.DATA_TYPE, 
    col.IS_NULLABLE,
    col.CHARACTER_MAXIMUM_LENGTH,
    tc.CONSTRAINT_TYPE,
    ccu.CONSTRAINT_NAME
FROM 
    INFORMATION_SCHEMA.COLUMNS AS col
LEFT JOIN 
    INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu
    ON col.COLUMN_NAME = ccu.COLUMN_NAME 
    AND col.TABLE_NAME = ccu.TABLE_NAME
    AND col.TABLE_SCHEMA = ccu.TABLE_SCHEMA
LEFT JOIN 
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
    ON ccu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
    AND ccu.TABLE_NAME = tc.TABLE_NAME
    AND ccu.TABLE_SCHEMA = tc.TABLE_SCHEMA
WHERE 
    col.TABLE_NAME = 'House' 
    AND col.TABLE_SCHEMA = 'dbo'
    AND (tc.CONSTRAINT_TYPE = 'PRIMARY KEY' OR tc.CONSTRAINT_TYPE = 'FOREIGN KEY' OR tc.CONSTRAINT_TYPE IS NULL);
