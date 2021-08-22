#dw_ecommerce database redshift
CREATE TABLE dw_ecommerce.public.uk_ecommerce
(
  unitprice DECIMAL(8,2),
  description VARCHAR(40),
  unique_id INT NOT NULL,
  quantity INT,
  country VARCHAR(25),
  invoiceno VARCHAR(10),
  invoicedate TIMESTAMP,
  Year INT,
  Quarter INT,
  Month VARCHAR(10),
  Week_of_Month INT,
  Day VARCHAR(10),
  customerid INT,
  stockcode VARCHAR(10)
);