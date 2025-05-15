| ------------ | ---------------------------------------------------------- |
| View Name    | Description                                                |
| ------------ | ---------------------------------------------------------- |
| `customers`  | One row per customer, with demographic and signup details  |
| `products`   | Product/SKU details: price, category, inspection           |
| `orders`     | One row per order (aggregated from order lines)            |
| `promotions` | Promo metadata like discount %, promo window               |
| `returns`    | One row per return event                                   |
| `shipments`  | One row per delivery/shipping instance                     |
| `suppliers`  | Supplier lead times and info                               |
| `warehouses` | Warehouse locations and IDs                                |
| ------------ | ---------------------------------------------------------- |


### customers

This view extracts unique customer profiles from the raw transactional dataset. In the original flat table, customer details were repeated across every product line. By normalizing this into a separate `customers` view, we make the model cleaner and enable easier analysis of customer behavior.

Fields include:
- Demographics: Gender, Age, Segment
- Location: Region and City
- Signup details: Channel, Date, Loyalty Tier


### products

This view contains one row per unique SKU. It captures product-level attributes useful for pricing, quality control, and category-level sales analysis.

### promotions

Lists distinct promotions used in the dataset. Helps analyze performance of each promotion type and cycle, such as FIRSTORDER, BDAY25, and BLKFRI.

### returns

Captures individual return events, including return method, reason, and status. One row per return, not per product. Enables return rate and refund impact analysis.

### warehouses

Contains unique warehouse IDs and their geographic locations. Useful for analyzing inventory, fulfillment efficiency, and location-based logistics.

### suppliers

Unique list of suppliers

### shipments

Details shipment records including shipping duration, promised delivery windows, carriers, and any delivery exceptions. I want to do lead time analysis and SLA monitoring.

### orders

Summarizes each order (one row per OrderID), aggregating values from the order line items. Useful for basket analysis, revenue per order, and time-based order tracking.

