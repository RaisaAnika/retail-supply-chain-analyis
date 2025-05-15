# This dataset is a simulated representation of the operations of a mid-sized retail company.It incorporates multiple realistic dimensions of a modern supply chain and order management system, including customer behavior, promotions, shipping logistics, manufacturing, and returns.

# Customer Behavior
# Every customer has a unique ID and associated attributes such as gender (including “Unknown”), age, customer segment (e.g., Teen, Athlete), geographic information (region and city), and loyalty tier (Bronze, Silver, Gold).
# Customers join through various channels such as web, mobile app, or referrals.
# Some customers have made multiple purchases, while others signed up but never placed an order—reflecting dormant accounts often found in real databases.
# Orders and Order Lines
# Each row in the dataset represents one product on an order (an order line). Some orders include multiple products, and as such, share the same Order ID across multiple rows to reflect multi-line orders.
# Orders include order date, order priority (High, Normal, Low), quantity ordered, and the quantity that was ultimately fulfilled.
# Inventory availability is captured through fields such as stock level, reorder point, and a flag indicating whether the order was successfully allocated to available stock.
# Promotions
# A variety of promotions are included, such as first-order discounts, birthday offers, seasonal sales, and Black Friday campaigns.
# Each promotion includes a code, type, start and end dates, discount percentage, and minimum spend requirements.
# Promotions are only applied if all eligibility criteria are met. For example, the "FIRSTORDER" promotion is only applied to a customer’s first purchase, and all promotions require the order to fall within the specified date range and minimum spend.
# Discounts directly affect the final selling price and revenue calculation.
# Shipping and Fulfillment
# Shipping information is only available for orders that were fulfilled (i.e., not cancelled).
# Shipments include tracking ID, carrier name, transportation mode, service level (e.g., Express, Economy), and shipping route.
# Shipping, promised delivery, and actual delivery dates are used to calculate shipping and fulfillment lead times.
# Delivery exceptions such as weather delays or address issues are included for a small subset of deliveries to simulate real-world last-mile issues.
# Returns
# Returns are only processed for delivered orders.
# Returned units, reasons (e.g., defective, didn’t fit), return request date, status, and refund details are included.
# Refund amounts are calculated based on the final selling price at the time of purchase.
# Manufacturing and Quality
# Each order line is linked to a simulated production batch that includes a production start and end date, enabling calculation of manufacturing lead time.
# Manufacturing cost, batch volume, inspection results, and defect rates are also tracked to reflect basic quality control processes.
# Suppliers and Warehousing
# Each order is associated with a randomly assigned supplier and warehouse.
# Supplier performance is modeled using both promised and actual lead times, allowing for supplier reliability analysis.
# Warehouses have unique IDs and locations and are linked to each order’s fulfillment.
# Lead Time Analysis
# The dataset intentionally includes raw date fields rather than pre-calculated lead times to allow for dynamic analysis.

# Users can compute:

# Manufacturing Lead Time: ProductionEndDate - ProductionStartDate
# Shipping Lead Time: DeliveryDate - ShipDate
# Order Fulfillment Lead Time: DeliveryDate - OrderDate


!pip install faker
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import timedelta


fake = Faker()
random.seed(42)
Faker.seed(42)
NUM_ROWS = 6000


categories = ['Running Shoes', 'Gym Wear', 'Jackets', 'Sneakers', 'Socks', 'Caps']
promo_catalog = [
    {'PromoID': 'FIRSTORDER', 'PromoType': 'Welcome', 'DiscountPct': 10, 'MinSpend': 30},
    {'PromoID': 'BLKFRI', 'PromoType': 'Black Friday', 'DiscountPct': 25, 'MinSpend': 20},
    {'PromoID': 'BDAY25', 'PromoType': 'Birthday', 'DiscountPct': 25, 'MinSpend': 15},
    {'PromoID': 'SUMMER15', 'PromoType': 'Seasonal', 'DiscountPct': 15, 'MinSpend': 25},
    {'PromoID': 'NEW10', 'PromoType': 'General', 'DiscountPct': 10, 'MinSpend': 10}
]
return_modes = ['Ground', 'Air', 'Postal', 'Pick-Up']
genders = ['Male', 'Female', 'Non-binary', 'Unknown']
segments = ['Athlete', 'Casual', 'Professional', 'Teen', 'Senior']
shipping_carriers = ['FedEx', 'UPS', 'DHL', 'USPS']
transportation_modes = ['Air', 'Sea', 'Land']
routes = ['North Route', 'South Route', 'East Route', 'West Route']
ship_methods = ['Standard', 'Express', 'Economy']
return_reasons = ['Didn’t Fit', 'Changed Mind', 'Defective', 'Wrong Item']

# Static reference tables
warehouses = [{'WarehouseID': f'WH{str(i).zfill(3)}', 'WarehouseLocation': fake.city()} for i in range(1, 11)]
suppliers = [fake.company() for _ in range(20)]
skus = [f"XYZ-{cat[:3].upper()}-{str(i).zfill(3)}" for cat in categories for i in range(1, 101)]
customers = [{
    'CustomerID': f"CUST{str(i).zfill(5)}",
    'Gender': random.choice(genders),
    'Age': random.randint(18, 65),
    'Segment': random.choice(segments),
    'Region': fake.state(),
    'City': fake.city(),
    'SignupChannel': random.choice(['Web', 'App', 'Referral']),
    'SignupDate': fake.date_between(start_date='-2y', end_date='-6M'),
    'BirthDate': fake.date_of_birth(minimum_age=18, maximum_age=65),
    'LoyaltyTier': random.choices(['Bronze', 'Silver', 'Gold'], weights=[0.6, 0.3, 0.1])[0]
} for i in range(4000)]

# Generate records
records = []
order_counter = 100000
used_customer_ids = []

for _ in range(NUM_ROWS):
    customer = random.choice(customers)
    customer_id = customer['CustomerID']
    new_order = random.random() < 0.7 or customer_id not in used_customer_ids
    if new_order:
        order_id = f"ORD{order_counter}"
        order_date = fake.date_between(start_date='-6M', end_date='today')
        used_customer_ids.append(customer_id)
        order_counter += 1

    order_line_id = f"{order_id}-L{random.randint(1, 5)}"
    sku = random.choice(skus)
    category = next(cat for cat in categories if cat[:3].upper() in sku)
    price = round(random.uniform(20, 300), 2)
    stock = random.randint(0, 1000)
    reorder_point = random.randint(50, 300)
    quantity = random.randint(1, 10)
    was_allocated = stock >= quantity
    availability = was_allocated
    units_sold = quantity if was_allocated else random.randint(0, quantity)

    # Promotions
    promo = random.choice(promo_catalog)
    promo_start = fake.date_between(start_date='-6M', end_date='-1M')
    promo_end = promo_start + timedelta(days=random.randint(5, 30))
    promo_applied = order_date >= promo_start and order_date <= promo_end and (price * quantity) >= promo['MinSpend']
    if promo_applied:
        discount = promo['DiscountPct']
        final_price = round(price * (1 - discount / 100), 2)
    else:
        promo = {k: None for k in promo}
        discount = 0
        final_price = price

    revenue = round(units_sold * final_price, 2)
    order_priority = random.choice(['High', 'Normal', 'Low'])
    order_status = random.choices(['Delivered', 'Cancelled', 'Returned', 'In Transit'], weights=[0.7, 0.1, 0.1, 0.1])[0]
    cancellation_reason = random.choice(['Out of Stock', 'Customer Cancelled', 'Payment Issue']) if order_status == 'Cancelled' else 'None'

    if order_status != 'Cancelled':
        ship_date = order_date + timedelta(days=random.randint(1, 5))
        delivery_date = ship_date + timedelta(days=random.randint(1, 10))
        promised_date = ship_date + timedelta(days=random.randint(2, 7))
        carrier = random.choice(shipping_carriers)
        tracking_id = f"TRK{random.randint(100000,999999)}"
        ship_method = random.choice(ship_methods)
        shipping_cost = round(random.uniform(5, 50), 2)
        delivery_exception = random.choices([None, 'Address Issue', 'Weather Delay', 'Lost in Transit'], weights=[0.9, 0.03, 0.05, 0.02])[0]
    else:
        ship_date = delivery_date = promised_date = None
        carrier = tracking_id = ship_method = delivery_exception = None
        shipping_cost = 0.0

    if order_status == 'Delivered':
        returned_units = random.randint(0, units_sold)
    else:
        returned_units = 0

    return_id = f"RET{random.randint(100000,999999)}" if returned_units > 0 else None
    return_status = random.choice(['Approved', 'Declined', 'Completed', 'In Progress']) if returned_units > 0 else None
    return_reason = random.choice(return_reasons) if returned_units > 0 else None
    return_mode = random.choice(return_modes) if returned_units > 0 else None
    return_request_date = delivery_date + timedelta(days=random.randint(1, 14)) if returned_units > 0 else None
    return_completed_date = return_request_date + timedelta(days=random.randint(1, 10)) if returned_units > 0 else None
    refund_amount = round(returned_units * final_price, 2) if returned_units > 0 else 0.0

    production_start = order_date - timedelta(days=random.randint(10, 30))
    production_end = production_start + timedelta(days=random.randint(5, 15))
    manufacturing_cost = round(random.uniform(10, 250), 2)
    production_volume = random.randint(100, 10000)
    inspection_result = random.choices(['Pass', 'Fail'], weights=[0.9, 0.1])[0]
    defect_rate = round(random.uniform(0.005, 0.1), 3)

    supplier = random.choice(suppliers)
    supplier_lead_promised = random.randint(5, 15)
    supplier_lead_actual = supplier_lead_promised + random.randint(-2, 5)
    warehouse = random.choice(warehouses)

    record = {
        "OrderID": order_id,
        "OrderLineID": order_line_id,
        "CustomerID": customer_id,
        "SKU": sku,
        "Category": category,
        "Price": price,
        "PromoApplied": promo_applied,
        "PromoID": promo['PromoID'],
        "PromoType": promo['PromoType'],
        "DiscountPercent": discount,
        "MinSpend": promo['MinSpend'],
        "PromoStartDate": promo_start if promo_applied else None,
        "PromoEndDate": promo_end if promo_applied else None,
        "FinalPrice": final_price,
        "OrderDate": order_date,
        "OrderPriority": order_priority,
        "QuantityOrdered": quantity,
        "UnitsSold": units_sold,
        "Availability": availability,
        "WasAllocated": was_allocated,
        "RevenueGenerated": revenue,
        "TrackingID": tracking_id,
        "CarrierName": carrier,
        "CarrierServiceLevel": ship_method,
        "TransportationMode": random.choice(transportation_modes),
        "Route": random.choice(routes),
        "ShipDate": ship_date,
        "PromisedDeliveryDate": promised_date,
        "DeliveryDate": delivery_date,
        "ShippingTime": (delivery_date - ship_date).days if ship_date and delivery_date else None,
        "ShippingCost": shipping_cost,
        "DeliveryExceptionReason": delivery_exception,
        "ReturnID": return_id,
        "ReturnRequestDate": return_request_date,
        "ReturnStatus": return_status,
        "ReturnCompletedDate": return_completed_date,
        "ReturnReason": return_reason,
        "ReturnMode": return_mode,
        "ReturnedUnits": returned_units,
        "RefundAmount": refund_amount,
        "ProductionStartDate": production_start,
        "ProductionEndDate": production_end,
        "ManufacturingCost": manufacturing_cost,
        "ProductionVolume": production_volume,
        "InspectionResult": inspection_result,
        "DefectRate": defect_rate,
        "SupplierName": supplier,
        "SupplierLeadTimePromised": supplier_lead_promised,
        "SupplierLeadTimeActual": supplier_lead_actual,
        "WarehouseID": warehouse['WarehouseID'],
        "WarehouseLocation": warehouse['WarehouseLocation'],
        "CustomerGender": customer['Gender'],
        "CustomerAge": customer['Age'],
        "CustomerSegment": customer['Segment'],
        "CustomerRegion": customer['Region'],
        "CustomerCity": customer['City'],
        "SignupDate": customer['SignupDate'],
        "BirthDate": customer['BirthDate'],
        "LoyaltyTier": customer['LoyaltyTier'],
        "SignupChannel": customer['SignupChannel']
    }

    records.append(record)
    
df = pd.DataFrame(records)
df.head()
