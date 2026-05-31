# Phased Development Plan

I am dividing this project into 5 phases so that I can build the system step by step instead of trying to build everything at once.

My goal is to complete one part of the project, test it properly, and then move to the next phase. This will help me understand the system better and also make
debugging easier if something goes wrong.

The purpose of this phase is to build the smallest working version of the system.

I want to start with inventory because it is the foundation for bookings, availability checking, and all other operations that will be added in later phases.

Before creating customers, bookings, or payments, I first want to make sure that inventory data can be stored properly and loaded again after restarting the application.

Each phase should:

* solve one main problem,
* be fully usable from the command line,
* save data using JSON files,
* work even after restarting the program,
* and be independently testable.

---

# Phase 1 – Inventory Storage and Persistence

## Purpose

In the first phase, I want to build the smallest working version of the project.

Before creating customers, bookings, or payments, I first want to make sure that inventory data can be stored properly and loaded again after restarting the application.

## Features Included

### Inventory Management

The user should be able to:

* add inventory items
* view inventory items
* update inventory quantities
* search inventory items

Example items:

* Plastic Chairs
* Round Tables
* Pedestal Fans
* Gas Burners

### JSON Storage

The system should:

* create JSON files automatically if they do not exist
* save inventory data
* load inventory data when the program starts
* keep data available after restart

## How I Will Test This Phase

* Add multiple inventory items.
* Restart the application.
* Check whether all inventory data is still available.
* Update item quantities and verify the changes are saved correctly.

Phase 1 will be complete when inventory can be managed properly and all data remains available after restarting the program.

---

# Phase 2 – Customer Management and Booking Creation

## Purpose

After inventory management is working properly, I will add customer records and booking functionality.

This phase focuses on creating customer profiles and storing event bookings.

## Features Included

### Customer Management

The user should be able to:

* add customers
* view customer details
* update customer details
* search customers using their phone number

### Booking Management

The user should be able to:

* create a booking
* select a customer
* enter event details
* enter booking dates
* enter delivery and pickup dates

### Booking Inventory Lines

A single booking should be able to contain multiple inventory items with different quantities.

## How I Will Test This Phase

* Create multiple customer records.
* Create bookings for different customers.
* Add inventory items inside bookings.
* Restart the application and verify that customer and booking records are still available.

Phase 2 will be complete when customer records and booking records are working correctly and data is stored properly.

---

# Phase 3 – Availability Checking and Tracked Equipment

## Purpose

The main purpose of this phase is to prevent booking mistakes.

The system should check inventory availability before accepting a booking request.

## Features Included

### Availability Validation

The system should:

* check overlapping booking dates
* calculate reserved quantities
* calculate available quantities
* reject bookings when inventory is not available

### Individually Tracked Equipment

Support separate tracking for high-value equipment such as:

* LED Walls
* Imported Sound Systems
* Bridal Sofa Sets

The same equipment unit should not be assigned to multiple bookings at the same time.

### Pressure Score

The system should calculate a pressure score based on:

* booking size
* inventory requirements
* delivery overlap

I added pressure score because the story repeatedly describes
operational overload during peak season.
This gives the business a way to identify risky days before
problems happen.

## How I Will Test This Phase

* Create multiple bookings with overlapping dates.
* Verify inventory availability calculations.
* Try creating overbooked requests and confirm they are rejected.
* Test conflicts for individually tracked equipment.

Phase 3 will be complete when availability calculations and equipment tracking are working correctly.

---

# Phase 4 – Delivery, Return and Damage Handling

## Purpose

This phase focuses on what happens after a booking is confirmed.

The system should track inventory movement and monitor the condition of items when they return.

## Features Included

### Daily Operations Queue

Track activities such as:

* deliveries
* pickups
* emergency replacements

### Inventory States

Inventory should move through states such as:

* available
* reserved
* out for delivery
* at event
* returning
* under repair

### Return Management

Support:

* complete returns
* partial returns
* pending returns

### Damage and Loss Tracking

Record:

* damaged items
* missing items
* repairable items
* unrecoverable items

## How I Will Test This Phase

* Dispatch inventory for a booking.
* Record inventory returns.
* Record damaged items.
* Record missing items.
* Verify that inventory states are updated correctly.

Phase 4 will be complete when delivery tracking, return handling, and damage tracking work correctly.

---

# Phase 5 – Payments, Reports and Final Improvements

## Purpose

The final phase focuses on payments, reports, validations, and overall improvements.

At this stage, I want the system to feel complete and practical enough for daily use.

## Features Included

### Financial Transactions

Track:

* deposits
* balance payments
* refunds
* late fees
* damage deductions

### Reports

Generate reports such as:

* active bookings
* inventory currently outside the warehouse
* customer history
* damage reports
* idle inventory reports

### Validation and Improvements

Handle situations such as:

* invalid dates
* overbooking attempts
* duplicate records
* incorrect return quantities
* missing inventory

I will also try to improve menus, prompts, and error messages to make the system easier to use.

## How I Will Test This Phase

* Create complete booking workflows from start to finish.
* Record different types of payments.
* Record damages and deductions.
* Generate reports and verify the results.
* Test invalid situations and confirm the program handles them properly.

Phase 5 will be complete when the entire Sharma Tent House Management System works smoothly from inventory creation to final payment and reporting.
