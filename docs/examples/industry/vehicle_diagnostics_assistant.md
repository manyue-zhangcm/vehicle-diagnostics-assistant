# Vehicle Diagnostics Assistant

A driver-facing assistant that helps car owners when something goes wrong with their vehicle. It can:

* explain OBD-II diagnostic trouble codes (DTCs), dashboard warnings and symptoms in plain language
* tell the driver whether the vehicle is safe to drive, starting every answer with that safety verdict
* recommend repairs with a parts, labor and total cost estimate, including parts availability and warranty status
* book a workshop appointment that opens a structured service ticket for the technicians

It's good for testing:

* how a Front Man coordinates several specialist agents with AAOSA
* how agents call CodedTools that stand in for real backend systems (DTC database, parts inventory,
  workshop calendar, work-order API)
* how to use `sly_data` to keep personal data such as the VIN and the owner's name away from the LLMs
* how a CodedTool can return data to the client application through `sly_data` with an `allow` policy

---

## File

[vehicle_diagnostics_assistant.hocon](../../../registries/industry/vehicle_diagnostics_assistant.hocon)

---

## Description

The `VehicleDiagnosticsAssistant` Front Man talks to the driver and delegates to four specialist agents:

* **DiagnosticsSpecialist**: looks up trouble codes, or candidate codes from symptoms, with `DtcLookup`, and checks
  the vehicle's powertrain, mileage and warranty with `VehicleProfile`. It reports severity, drivability and the
  likely causes.
* **RepairAdvisor**: gets the recommended repairs, part numbers and labor hours from `DtcLookup`, asks
  `PartsSpecialist` for prices and availability, and computes the cost at a labor rate of 95 EUR per hour.
* **PartsSpecialist**: checks price, stock and lead time with `PartsLookup`.
* **ServiceScheduler**: offers open slots from `ServiceSlots` and, once the driver confirms a slot, opens a service
  ticket with `ServiceTicketApi`.

The ticket gives the technicians the driver's complaint, the trouble codes, the preliminary diagnosis, the severity,
the recommended repairs and the parts to prepare, so the workshop is ready when the car arrives.

---

## Tools

All tools are mock implementations backed by in-memory data, located in the
[CodedTools folder](../../../coded_tools/industry/vehicle_diagnostics_assistant):

| Tool               | Purpose                                                                                   |
|--------------------|-------------------------------------------------------------------------------------------|
| `DtcLookup`        | Looks up codes such as `P0301`, `P0420`, `P0AA6` or `C0035`, or searches by symptoms.     |
| `VehicleProfile`   | Returns make, model, powertrain, mileage and warranty of the vehicle linked by its VIN.   |
| `PartsLookup`      | Returns price in EUR, stock and lead time of parts.                                       |
| `ServiceSlots`     | Lists open workshop slots for the next business days.                                     |
| `ServiceTicketApi` | Books the appointment and opens the service ticket.                                       |

Replace the catalogs in `dtc_catalog.py`, `parts_catalog.py` and `vehicle_registry.py`, or the tools themselves,
with calls to real systems to go beyond the demo.

---

## Sly data

The client application passes private data in `sly_data`. It is available to the CodedTools but never sent to the
LLMs:

```json
{
    "vin": "WVWZZZ1KZ8W000001",
    "customer_name": "Alex",
    "current_date": "2026-10-23"
}
```

* `vin`: identifies the vehicle. Demo VINs are `WVWZZZ1KZ8W000001` (2019 Volkswagen Golf, gasoline),
  `WBA7E2C51KB000002` (2022 BMW 530e, plug-in hybrid) and `WMEEJ9AA5FK000003` (2023 Mercedes-Benz EQA, electric).
* `customer_name`: optional. If absent, the agents ask the driver for their name before booking.
* `current_date`: optional `YYYY-MM-DD` date override, used by the warranty check and the appointment slots.

`ServiceTicketApi` returns a ticket summary with a masked VIN to the agents and appends the full ticket to
`sly_data["service_tickets"]`. The Front Man's `allow.to_upstream` policy returns that list to the client
application, for instance to forward it to a workshop management system.

In the nsflow UI, you can set the sly data in the `Sly Data` panel before starting the conversation.

---

## Example conversation

With `sly_data` set to `{"vin": "WVWZZZ1KZ8W000001", "customer_name": "Alex", "current_date": "2026-10-23"}`:

```text
Human:
My check engine light is on and my scanner shows P0301. The engine shakes at red lights.

AI:
Safety: limit your driving. If the check engine light starts flashing, stop driving, because the catalytic
converter can be damaged.

P0301 means the engine detected a misfire on cylinder 1. Most likely causes:
1. A worn spark plug
2. A faulty ignition coil
3. A clogged fuel injector

Estimated repairs for your 2019 Volkswagen Golf (warranty expired):
- Spark plug: 14.90 EUR parts + 38.00 EUR labor = 52.90 EUR (in stock)
- Ignition coil: 74.50 EUR parts + 38.00 EUR labor = 112.50 EUR (in stock)
- Fuel injector: 129.00 EUR parts + 104.50 EUR labor = 233.50 EUR (needs to be ordered, 3 days)

This is a preliminary diagnosis that a technician will confirm. Would you like to book an appointment?

Human:
Yes, the earliest one please.

AI:
The earliest open slot is Monday 2026-10-26 at 10:30. Shall I book it?

Human:
Yes.

AI:
Booked. Your service ticket is WO-1001 for Monday 2026-10-26 at 10:30.
The workshop will check the cylinder 1 spark plug and ignition coil first.
```

The exact wording varies from run to run.

---

## Sample queries

* My check engine light is on and my scanner shows P0301. What does it mean?
* The car shakes at idle and the check engine light is flashing. Can I keep driving?
* How much would it cost to fix code P0420?
* My EV shows a high voltage warning and code P0AA6.
* Please book me the earliest appointment to get it fixed.
