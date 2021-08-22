DROP DATABASE IF EXISTS ECommerce_Database;
CREATE DATABASE IF NOT EXISTS ECommerce_Database;
USE ECommerce_Database;

CREATE TABLE Uk_Ecommerce_Data(
	Unique_id INT NOT NULL,
    InvoiceNo VARCHAR(10),
    StockCode VARCHAR(10),
    Description VARCHAR(40),
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(8,2),
    CustomerID INT,
    Country VARCHAR(25),
	CONSTRAINT pk_Uk_Ecommerce_Data PRIMARY KEY(Unique_id)
);
