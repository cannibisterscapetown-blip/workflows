---
description: Update the Advent Calendar collection for the day
---
This workflow automates the daily update of the Advent Calendar collection on Shopify.

It performs the following steps:
1.  Identifies the "Advent calendar" collection.
2.  Removes any existing products from the collection and restores their original prices.
3.  Reads the schedule from `advent_calendar_schedule.json`.
4.  Finds today's scheduled product.
5.  Applies the scheduled discount to the product.
6.  Adds the product to the "Advent calendar" collection.

To run this workflow, simply execute the following command:

```bash
python3 advent_calendar_manager.py
```

You can also specify a specific day (e.g., for testing or manual override) by passing the day number as an argument:

```bash
python3 advent_calendar_manager.py <day_number>
```
Example: `python3 advent_calendar_manager.py 5` (Runs the update for Day 5)
