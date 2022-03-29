USE first_test;

GO

IF EXISTS (SELECT * FROM sys.sysobjects WHERE Name = 'books_table')
    BEGIN
        DROP TABLE books_table
        PRINT 'books_table already exists, dropping table and recreating'
    END

GO

CREATE TABLE books_table
(
    bookID INT IDENTITY(1, 1) PRIMARY KEY,
    rating VARCHAR(20),
    product_type VARCHAR(20),
    upc VARCHAR(20),
    title VARCHAR(20)
);

GO