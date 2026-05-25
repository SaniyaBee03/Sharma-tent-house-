#1. Three-sentence specification
   
I am building a command-line management system for Sharma Tent House to replace the handwritten ledger currently used for handling bookings, inventory tracking, deliveries, returns, payments, damages, and daily event operations.

The system will be used by both Rakesh Sharma and Ankit, because Rakesh ji needs quick access to booking availability and operational information during customer calls, while Ankit will handle day-to-day tasks like entering bookings, updating deliveries, recording payments, and managing returned items.

This system will safely manage inventory across overlapping event dates, prevent operational mistakes like double-booking or incorrect returns, and permanently store all business activity using JSON files.

#2. The information the program must remember

After reading the full story carefully, I understood that the actual challenge while building this system will be managing inventory movement between multiple events happening at the same time, especially during wedding season when deliveries, pickups, damages, late returns, and payment confusion all happen together.That's why I divided the system into multiple connected sections.

A. Customer Profiles

customer_id :-	string,	Yes

full_name :-	string,	Yes

phone_number :-	string,	Yes

alternate_contact :-	string,	No

address :-	string,	Yes

trust_level :-	string,	Yes

I added trust_level because from the story it is clear that Rakesh ji gives discount to his father's friends depending on their history with the business.

B. Inventory Catalog

item_id :-	string,	Yes

item_name :-	string,	Yes

total_quantity :-	integer,	Yes

rental_price_per_day :-	integer,	Yes

replacement_cost :-	integer,	Yes

maintenance_required :-	boolean,	Yes

inventory_mode:- string, Yes

Inventory modes

bulk_inventory
Examples:
chairs, plates, glasses

tracked_inventory
Examples:
gas burners, pedestal fans

individually_tracked
Examples:
LED walls, imported sound systems, bridal sofa sets

This section stores all rentable items owned by Sharma Tent House.
For example:-
chairs
plates
glasses
gas burners
LED walls
bridal sofa set

C.Individually Tracked Units

unit_id:- string, Yes

parent_item_id:- string, Yes

display_name:- string, Yes

current_state:- string, Yes

assigned_booking_id:- string, No

D. Event Bookings

booking_id:-	string,	Yes

customer_id:-	string,	Yes

event_name:-	string,	Yes

event_type:-	string,	Yes

event_start_date:-	string,	Yes

event_end_date:-	string,	Yes

delivery_date:-	string,	Yes

pickup_date:-	string,	Yes

venue_location:-	string,	Yes

discount_amount:-	integer,	Yes

deposit_received:-	integer,	Yes

booking_status:- string, Yes

E. Booking Inventory Lines

line_id:- string, Yes

booking_id:- string, Yes

item_id:- string, Yes

booked_quantity:- integer, Yes

returned_quantity:- integer, Yes

damaged_quantity:- integer, Yes

missing_quantity:- integer, Yes

daily_rate:- integer, Yes

total_days:- integer, Yes

line_total:- integer, Yes

F. Financial Transactions

transaction_id:-	string,	Yes

booking_id:-	string,	Yes

amount:-	integer,	Yes

payment_mode:-	string,	Yes

transaction_date:-	string,	Yes

transaction_type:- string, Yes

G. Damage and Loss Register

report_id:-	string,	Yes

booking_id:-	string,	Yes

item_id:-	string,	Yes

issue_category:-	string,	Yes

quantity:-	integer,	Yes

estimated_loss:-	integer,	Yes

recovery_status:-	string,	Yes

usable_quantity:- integer, Yes


#3. How the groupings connect to each other

Customer Profiles connect with Event Bookings.

Event Bookings connect with Booking Inventory Lines.

Inventory Catalog connects with Booking Inventory Lines.

Financial Transactions connect directly with Event Bookings.

Damage and Loss Register connects with both Inventory Catalog and Event Bookings.

All the sections in my system are connected because the tent house business is not only about taking bookings. Every booking affects inventory, payments, deliveries, damages, and future availability at the same time.


#4. File structure

In the file structure i will use smaller json files because it will make the system easier to maintain and make debugging easier if something goes wrong during peak wedding season.

For example:- ## customers.json

[

  {
  
    "customer_id": "CUST-014",
    
    "full_name": "Rajesh Agarwal",
    
    "phone_number": "9876543210",
    
    "alternate_contact": "9829034567",
    
    "address": "Talwandi, Kota",
    
    "trust_level": "high"
    
  },

  {
  
    "customer_id": "CUST-021",
    
    "full_name": "Manoj Mehta",
    
    "phone_number": "9988776655",
    
    "alternate_contact": "",
    
    "address": "Mahaveer Nagar, Kota",
    
    "trust_level": "medium"
    
  }
  
]

## bookings.json

[

  {
  
    "booking_id": "BOOK-2026-041",
    
    "customer_id": "CUST-014",
    
    "event_name": "Agarwal Wedding",
    
    "event_type": "Wedding",
    
    "event_start_date": "2026-12-18",
    
    "event_end_date": "2026-12-20",
    
    "delivery_date": "2026-12-17",
    
    "pickup_date": "2026-12-21",
    
    "venue_location": "Vigyan Nagar, Kota",
    
    "booking_status": "confirmed",
    
    "discount_amount": 5000,
    
    "deposit_received": 25000
    
  }
  
]

## inventory.json

[

  {
  
    "item_id": "ITEM-CHAIR-001",
    
    "item_name": "White Plastic Chair",
    
    "inventory_mode": "bulk_inventory",
    
    "total_quantity": 500,
    
    "rental_price_per_day": 12,
    
    "replacement_cost": 450,
    
    "maintenance_required": false
    
  },

  {
  
    "item_id": "ITEM-BURNER-001",
    
    "item_name": "Commercial Gas Burner",
    
    "inventory_mode": "tracked_inventory",
    
    "total_quantity": 6,
    
    "rental_price_per_day": 250,
    
    "replacement_cost": 1200,
    
    "maintenance_required": false
    
  },

  {
  
    "item_id": "ITEM-LED-001",
    
    "item_name": "LED Video Wall",
    
    "inventory_mode": "individually_tracked",

    "total_quantity": 2,
    
    "rental_price_per_day": 8500,
    
    "replacement_cost": 120000,

    "maintenance_required": false
    
  }
  
]


## tracked_units.json

[

  {
  
    "unit_id": "LED-UNIT-01",
    
    "parent_item_id": "ITEM-LED-001",
    
    "display_name": "Outdoor LED Wall Unit 1",
    
    "current_state": "reserved",
    
    "assigned_booking_id": "BOOK-2026-041"
    
  },

  {
  
    "unit_id": "LED-UNIT-02",
    
    "parent_item_id": "ITEM-LED-001",
    
    "display_name": "Outdoor LED Wall Unit 2",
    
    "current_state": "available",
    
    "assigned_booking_id": ""
    
  }
  
]

## booking_inventory_lines.json

[

  {
  
    "line_id": "LINE-001",
    
    "booking_id": "BOOK-2026-041",
    
    "item_id": "ITEM-CHAIR-001",
    
    "booked_quantity": 200,
    
    "returned_quantity": 193,
    
    "damaged_quantity": 5,
    
    "missing_quantity": 2,
    
    "daily_rate": 12,
    
    "total_days": 3,
    
    "line_total": 7200
    
  },

  {
  
    "line_id": "LINE-002",
    
    "booking_id": "BOOK-2026-041",
    
    "item_id": "ITEM-LED-001",
    
    "booked_quantity": 1,
    
    "returned_quantity": 1,
    
    "damaged_quantity": 0,
    
    "missing_quantity": 0,
    
    "daily_rate": 8500,
    
    "total_days": 3,
    
    "line_total": 25500
    
  }
  
]

## transactions.json

[

  {
  
    "transaction_id": "TXN-101",
    
    "booking_id": "BOOK-2026-041",
    
    "amount": 25000,
    
    "payment_mode": "cash",
    
    "transaction_date": "2026-11-10",
    
    "transaction_type": "deposit"
    
  },

  {
  
    "transaction_id": "TXN-102",
    
    "booking_id": "BOOK-2026-041",
    
    "amount": 15000,
    
    "payment_mode": "upi",
    
    "transaction_date": "2026-12-17",
    
    "transaction_type": "partial_balance_payment"
    
  }
  
]

## damages.json

[

  {
  
    "report_id": "DMG-001",
    
    "booking_id": "BOOK-2026-041",
    
    "item_id": "ITEM-CHAIR-001",
    
    "issue_category": "damaged",
    
    "quantity": 5,
    
    "estimated_loss": 2250,
    
    "recovery_status": "deducted_from_deposit",
    
    "usable_quantity": 3
    
  },

  {
  
    "report_id": "DMG-002",
    
    "booking_id": "BOOK-2026-041",
    
    "item_id": "ITEM-CHAIR-001",
    
    "issue_category": "missing",
    
    "quantity": 2,
    
    "estimated_loss": 900,
    
    "recovery_status": "customer_charged",
    
    "usable_quantity": 0
    
  }
  
]


#5. Operations

 1. User creates a customer profile → system checks duplicate phone numbers → customer profile saved.
 2. User creates a new booking request → system checks inventory availability for selected dates → booking accepted or rejected.
 3. User adds inventory items into booking → system updates running total → booking summary displayed.
 4. User selects event dates → system calculates rental duration automatically → pricing updated.
 5. User books individually tracked equipment → system reserves exact inventory unit → double-booking prevented.
 6. User requests unavailable quantity → system shows shortage details → booking blocked.
 7. User records deposit payment → system updates financial records → remaining balance displayed.
 8. User assigns tempo for delivery → system checks delivery load for that date → overload warning shown if needed.
 9. User opens operational calendar → system displays all deliveries and pickups scheduled for that day.
 10. User marks inventory as dispatched → inventory state changes from reserved to out_for_delivery.
 11. User marks event setup completed → booking becomes active event.
 12. User records partial item return → remaining pending items continue tracking.
 13. User records damaged inventory → damage register updated → repair workflow started.
 14. User records missing inventory → replacement cost added to customer dues.
 15. User records late return → late fee calculated automatically.
 16. User tries closing booking before all returns are completed → system blocks closure.
 17. User checks customer history → previous bookings, damages, and payment behavior displayed.
 18. User cancels booking → reserved inventory released automatically.
 19. User checks pressure dashboard → high-risk operational days highlighted.
 20. User views currently active events → all inventory currently outside shop displayed.
 21. User starts system next morning → all previous operational data restored automatically.
   

#6. Things that can go wrong

1. JSON file missing during first startup → system automatically creates required files.
2. User tries booking more inventory than available → booking rejected.
3. Individually tracked item already reserved for another event → system prevents double booking.
4. User enters invalid event date range → save operation blocked.
5. Customer cancels after inventory already dispatched → operational cancellation warning displayed.
6. Missing item value exceeds customer deposit → remaining balance added to dues.
7. User attempts to close booking with pending returns → unresolved inventory warning displayed.
8. System crashes during JSON write operation → backup recovery file maintained.
9. Staff forgets to mark returned items → overdue inventory appears in pending alerts.
10. Returned item marked available before inspection → item first enters inspection state.
11. Peak wedding season dates exceed operational handling capacity → warning displayed before confirmation.
12. Booking references deleted inventory item → validation error logged.
   

#7. One thing I don't know yet

One thing I am still unsure about is the cleanest way to handle overlapping booking validation for mixed inventory types. Bulk inventory like chairs works differently from individually tracked equipment like LED walls, especially when late returns or partial returns happen. I would probably need to experiment with multiple approaches before finalizing the implementation logic.
