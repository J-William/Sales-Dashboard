-- Sales Data Schema
CREATE TABLE IF NOT EXISTS "sales" (
"Order ID" TEXT,
  "Order Date" TIMESTAMP,
  "Ship Date" TIMESTAMP,
  "Ship Mode" TEXT,
  "Customer ID" TEXT,
  "Customer Name" TEXT,
  "Segment" TEXT,
  "Country" TEXT,
  "City" TEXT,
  "State" TEXT,
  "Postal Code" INTEGER,
  "Region" TEXT,
  "Product ID" TEXT,
  "Category" TEXT,
  "Sub-Category" TEXT,
  "Product Name" TEXT,
  "Sales" REAL,
  "Quantity" INTEGER,
  "Discount" REAL,
  "Profit" REAL,
  "Delivery Time" REAL
);
CREATE INDEX "ix_sales_Order ID"ON "sales" ("Order ID");