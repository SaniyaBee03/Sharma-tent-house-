Phased Development Plan

I am dividing this project into 5 phases because building the complete Sharma Tent House system together will be difficult to manage and test. By working phase by phase, I can make sure each part is working properly before moving to the next one.

Every phase should:

work from the command line,

save data in JSON files,

keep data after restart,

and be fully demoable on its own.

## Phase 1 – Customer and Inventory Management

Purpose

In the first phase, I will focus on creating the basic structure of the system.

Before creating bookings or handling availability, I first want to make sure that customer information and inventory information can be stored properly and loaded again after restarting the program.

Features Included

Customer Management

The user should be able to:

add customers

view customer details

update customer information

search customers using phone number

The system will store customer information such as name, phone number, address, trust level and booking history.

Inventory Management

The user should be able to:

add inventory items

view inventory

update inventory details

This phase will support different inventory types such as chairs, tables, gas burners, fans and other rental items.

Tracked Equipment

For special items like LED walls, sound systems and sofa sets, the system should allow separate unit tracking.

#How I Will Test This Phase

Add customers

Add inventory items

Add tracked equipment

Exit the program

Restart the program

Verify all information is still available

Phase 1 will be complete when customer and inventory records are saved correctly and survive program restart.

## Phase 2 – Booking System and Availability Checking

Purpose

The main goal of this phase is to solve the booking conflict problem mentioned in the project brief.

The system should be able to tell whether inventory is available before accepting a booking.

Features Included

Create Booking

The user should be able to:

select a customer

enter event details

choose event dates

choose delivery and pickup dates

Add Inventory to Booking

A booking can contain multiple items such as:

chairs

tables

gas burners

fans

LED walls

Availability Validation

Before saving a booking, the system should:

check overlapping dates

calculate already reserved inventory

calculate available inventory

reject bookings if enough stock is not available

Tracked Item Validation

The same LED wall or sound system should not be assigned to two bookings at the same time.

# How I Will Test This Phase

Create a booking

Add inventory items

Create another booking on overlapping dates

Verify availability calculations

Verify overbooking is blocked

Phase 2 will be complete when booking and availability checking work correctly.

## Phase 3 – Delivery and Return Tracking

Purpose

After bookings are created, the next important task is tracking where inventory is moving.

This phase focuses on deliveries, pickups and inventory movement.

Features Included

Delivery Tracking

The user should be able to:

schedule deliveries

assign tempos

assign workers

Inventory Status Tracking

Inventory should move through different states such as:

available

reserved

out for delivery

at event

returning

under repair

Return Tracking

The system should support:

full returns

partial returns

pending returns

Late Returns

The system should identify inventory that has not been returned on time.

# How I Will Test This Phase

Create booking

Dispatch inventory

Mark delivery completed

Record partial return

Record complete return

Phase 3 will be complete when inventory movement can be tracked properly.

## Phase 4 – Payments, Damages and Loss Tracking

Purpose

This phase focuses on the money side of the business and handling damaged or missing inventory.

Features Included

Payment Tracking

The system should store:

deposits

balance payments

refunds

late fees

Damage Recording

The user should be able to record:

damaged items

missing items

repairable items

Customer Dues

The system should calculate:

amount paid

amount pending

deductions for damages

final customer balance

# How I Will Test This Phase

Record booking payment

Record additional payment

Record damaged item

Apply deduction

Calculate final amount

Phase 4 will be complete when payment and damage handling work correctly.

## Phase 5 – Reports, Validation and Final Improvements

Purpose

The final phase focuses on making the project easier to use and more reliable.

Instead of adding major features, I will improve the overall quality of the system.

Features Included

Reports

Generate reports such as:

active bookings

inventory currently out

customer history

damage reports

idle inventory reports

Validation

Test situations such as:

overbooking

invalid dates

duplicate records

incorrect returns

missing inventory

CLI Improvements

Improve menu structure, messages and overall usability.

# How I Will Test This Phase

I should be able to demonstrate the complete flow:

create customer

add inventory

create booking

check availability

dispatch items

record returns

record payments

generate reports

Phase 5 will be complete when the entire system works smoothly and can be demonstrated from start to finish without manual fixes.
