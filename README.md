# Phase 3 Design Decisions

## Booking IDs

Booking IDs follow the format:

BOOK_001
BOOK_002
BOOK_003

If malformed IDs such as BOOK_ABC are found, the system ignores them during ID generation and displays a warning while viewing bookings.

## Pressure Score

Pressure Score is stored when a booking is created.

The value acts as a historical snapshot and is not recalculated later. This ensures reports show the operational pressure that existed at booking creation time.

Pressure Score Formula:

Pressure Score =
Total Quantity +
(Item Count × 10) +
(Overlapping Bookings × 20)

Pressure Levels:

- LOW (< 50)
- MEDIUM (< 100)
- HIGH (>= 100)

## Tracked Equipment

Tracked equipment uses individual unit identifiers.

Example:

LED WALL
- LED001
- LED002

Each unit can be assigned independently to different bookings.

Assignment records store:

- item_id
- booking_id
- unit_id

Item names are resolved from inventory data when displayed to avoid stale duplicate data.

## Data Validation

The system validates:

- Inventory records
- Customer records
- Booking records
- Booking item records
- Quantity values
- Date ranges
- Deposit amounts

Invalid records generate warnings and are not processed.

## Future Enhancements

Future phases may include:

- Booking cancellation workflow
- Equipment release workflow
- Assignment history
- Utilization reporting
- Booking editing
- Dynamic pressure analytics