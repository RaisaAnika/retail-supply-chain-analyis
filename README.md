# Retail-supply-chain-analysis
A project to analyse end-to-end processes with a retail supply chain using SQL and Power BI

The dataset (flat table) has been synthesized using the Python library called Faker.
This dataset simulates the operations  a mid-sized retail apparel company.
The data was generated and used to showcase advanced data modeling, analytics, and storytelling using SQL and Power BI. It includes promotions, shipping, manufacturing, customer behavior, and return tracking — all structured with realistic business logic and interdependencies.

---

### Business Logic Considered

#### Customers
- Each customer is assigned a unique `CustomerID`.
- Customers have attributes like `Gender`, `Age`, `Segment`, `Region`, `City`, `SignupDate`, `BirthDate`, `SignupChannel`, and `LoyaltyTier`.
- Some customers are **repeat buyers** (appear multiple times).
- Some customers exist in the system but **never placed an order**, simulating dormant accounts.

#### 🛍️ Orders
- Each row represents a **single order line** (one product within an order).
- Some `OrderID`s are repeated to simulate **multi-line orders** (e.g., buying socks and shoes together).
- Every order has an `OrderDate`, `OrderPriority`, and a quantity of units ordered and sold.
- Stock availability is checked using the `StockLevel`, and allocation is reflected in `WasAllocated` and `Availability`.

#### 🎁 Promotions
- Promotions include codes like `FIRSTORDER`, `BLKFRI`, `BDAY25`, each with:
  - A specific discount %
  - A `PromoStartDate` and `PromoEndDate`
  - A `MinSpend` requirement
- `PromoApplied = True` only if:
  - The order falls within the promo window
  - Spend meets or exceeds the minimum threshold
  - (For `FIRSTORDER`) it is the customer’s first-ever purchase
- Final prices and revenue are adjusted accordingly.

#### 🚚 Shipping
- Shipping data is only populated for orders that are **not cancelled**.
- Each shipment includes:
  - `TrackingID`, `CarrierName`, `ShipMethod`, `TransportationMode`, `Route`
  - `ShipDate`, `PromisedDeliveryDate`, `DeliveryDate`
  - `ShippingTime` is derived from `DeliveryDate – ShipDate`
  - `DeliveryExceptionReason` is included for 5–10% of orders (e.g., "Address Issue", "Weather Delay").

#### 🔁 Returns
- Only **delivered orders** can be returned.
- If returned, the dataset captures:
  - `ReturnedUnits`, `ReturnReason`, `ReturnStatus`, `ReturnRequestDate`, `ReturnCompletedDate`, and `RefundAmount`
  - `RefundAmount = ReturnedUnits × FinalPrice`

#### 🏭 Manufacturing
- Each order line includes production metadata:
  - `ProductionStartDate`, `ProductionEndDate` → used to calculate manufacturing lead time
  - `ManufacturingCost`, `ProductionVolume`, `InspectionResult`, and `DefectRate`

#### 🔗 Supplier & Warehouse
- Orders are linked to a `SupplierName`, with both:
  - `SupplierLeadTimePromised`
  - `SupplierLeadTimeActual`
- Products ship from randomly assigned warehouses (`WarehouseID`, `WarehouseLocation`)

#### ⏱️ Lead Times
- Lead times are **not precomputed**, allowing you to analyze them in SQL/Power BI:
  - `Manufacturing Lead Time = ProductionEndDate - ProductionStartDate`
  - `Shipping Lead Time = DeliveryDate - ShipDate`
  - `Fulfillment Lead Time = DeliveryDate - OrderDate`



