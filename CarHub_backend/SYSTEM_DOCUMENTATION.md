# CarHub System Documentation

Last verified against the repository: 2026-08-11

## 1. Purpose of this document

This is the living technical guide for the entire CarHub system. It explains what the project is intended to become, what is implemented today, how the backend and frontend are organized, and where future development should continue.

This document describes the code as it currently exists. Planned behavior is labelled **Planned** and known incomplete or unsafe behavior is labelled **Known issue**.

Update this document whenever a change affects:

- the data model;
- an API endpoint or response shape;
- authentication or authorization;
- pricing or checkout rules;
- a major frontend flow;
- installation or environment configuration;
- the implementation status of a planned feature.

`PROGRESS.md` is the short task tracker. This file is the long-form system explanation.

## 2. Product vision

CarHub is a digital car dealership system for browsing and configuring new cars, listing unique used vehicles, managing a shopping cart, and eventually processing bookings, orders, payments, sales, inventory, and accessory recommendations.

The intended product has four important sales flows:

1. New vehicle already in stock.
2. Unique used vehicle.
3. New vehicle made to order.
4. Vehicle imported by request.

Only catalog, configuration, account, and new-car cart foundations are currently implemented. Orders, payments, accessory sales, and the four complete checkout flows are not yet implemented.

## 3. Repository structure

```text
CarHub/
|-- CarHub_backend/          Django and Django REST Framework
|   |-- accounts/            Registration, profiles, account endpoints
|   |-- cars/                Catalog, configuration, used cars, and cart
|   |-- config/              Project settings, root URLs, pagination
|   `-- manage.py
|-- CarHub_Frontend/         React single-page frontend
|   |-- public/
|   `-- src/
|       |-- components/
|       |-- context/
|       |-- data/            Current static car data
|       `-- styles/
|-- PROGRESS.md              Short implementation tracker
|-- README.md                Brief project introduction and setup
|-- SYSTEM_DOCUMENTATION.md  This document
`-- requirements.txt         Python environment snapshot
```

## 4. High-level architecture

```text
Customer or staff
       |
       +------------------------------+
       |                              |
React frontend                  Django admin
(currently static/simulated)    (real database management)
       |                              |
       | planned HTTP/JSON             |
       v                              v
Django REST Framework API --------> Django ORM
       |                              |
       +------------------------------+
                      |
                    MySQL
```

The backend and frontend are separate applications. The backend exposes JSON endpoints under `/api/`. The frontend is not yet connected to those endpoints and currently uses static JavaScript data and browser `localStorage`.

## 5. Technology stack

### Backend

- Python 3.12 development environment
- Django 6.0
- Django REST Framework 3.16.1
- Simple JWT 5.5.1
- django-filter 25.2
- MySQL through `mysqlclient`
- Pillow for uploaded car images

### Frontend

- React 19
- Create React App / `react-scripts` 5
- React Icons
- React Testing Library
- Plain CSS

## 6. Backend applications

### 6.1 `accounts`

The accounts application extends Django's built-in `User` with a one-to-one `CustomerProfile`.

`CustomerProfile` currently stores:

- phone;
- address;
- gender;
- ID-card value;
- created and updated timestamps.

Registration creates both `User` and `CustomerProfile`. JWT tokens use the standard Simple JWT views.

VIP membership currently has two competing concepts:

- `IsVIPUser` and catalog serializers check membership in Django's `VIP` group.
- `add_to_cart` tries to access `CustomerProfile.is_vip`, but that field does not exist.

**Known issue:** one authoritative VIP rule must be selected and reused everywhere before checkout work continues. The Django `VIP` group is the currently functioning implementation.

### 6.2 `cars`

The cars application currently owns several different responsibilities:

- new-car catalog;
- configuration options and price calculation;
- used-car inventory foundations;
- cart and selected configuration storage;
- vehicle images.

As the project grows, orders, accessories, and inventory may deserve separate Django applications. They should not automatically be added to `cars` simply because they relate to vehicles.

## 7. Domain model

### 7.1 Core vehicle identity

```text
Brand 1 ---- * Car 1 ---- * CarModel
                   |
                   +----- * UsedCar
```

- `Brand` is the manufacturer, such as Toyota.
- `Car` is the model family, such as Toyota Corolla.
- `CarModel` is a sellable/configurable new-car model for a particular year.
- `UsedCar` is one unique physical vehicle associated with a `Car`.

`UsedCar` deliberately does not inherit the price from `CarModel`. A used vehicle has its own acquisition cost and selling prices.

### 7.2 New-car pricing and descriptive data

`CarModel` contains:

- year and internal `code`;
- normal price, optional VIP price, and optional internal cost;
- drive, fuel-tank capacity, seating capacity, and description;
- created and updated timestamps.

`CarModelSpecification` is a one-to-one dimension record containing interior and exterior length, width, and height.

`CarModelImage` stores multiple ordered images. `is_primary` identifies the intended main image, but the database does not currently enforce that only one image is primary.

### 7.3 New-car configuration

Reusable option definitions:

- `Engine` with fuel type, engine description, and horsepower;
- `Transmission`;
- `Brake`;
- `Exhaust`;
- `FeatureCategory` and `Feature`;
- wheel design, wheel size, tyre, tyre size, and color;
- `WheelPackage`, which combines the wheel-related definitions.

Per-model join records define availability and price adjustments:

- `CarModelEngine`;
- `CarModelTransmission`;
- `CarModelBrake`;
- `CarModelExhaust`;
- `CarModelFeature`;
- `CarModelWheelPackage`.

This separation means an engine can be reused, while the join row answers: “Is this engine available for this car model, and how much does it add?”

`FeatureCategory.is_configurable` distinguishes customer-selectable options from informational equipment. `display_order` controls grouping order.

### 7.4 Used cars

Every `UsedCar` row is one physical inventory unit, even if another row has the same brand, model, year, and color.

Current used-car data includes:

- relationship to `Car`;
- year and mileage;
- condition: excellent, good, fair, or poor;
- status: available, reserved, or sold;
- acquisition `cost`, normal `price`, and optional `vip_price`;
- unique, validated 17-character VIN;
- installed transmission, fuel type, and exterior color;
- description and timestamps.

Customer endpoints must return only `available` vehicles. Staff should retain access to reserved and sold records. A sold used car should not be deleted because it will eventually be referenced by sales history.

Used cars now have a full serializer (`UsedCarSerializer`, with nested `UsedCarImageSerializer` and `ColorSerializer`), a filter (`UsedCarFilter`: brand/year/min_price/max_price/condition/fuel_type), and public list/detail views and URLs (`used-cars/`, `used-cars/<int:pk>/`), both restricted to `status='available'`.

**Still not implemented:** cart representation (a `CartItem` cannot reference a `UsedCar`) and order integration.

### 7.5 Internal inventory-code policy

CarHub uses human-readable internal codes separate from database IDs and VINs.

Planned prefixes:

| Item type | Prefix | Example |
|---|---:|---:|
| New car model | `001` | `0010001` |
| Unique used car | `002` | `0020001` |
| Accessory | `003` | `0030001` |

Rules agreed during design:

- staff may provide a valid unique code manually;
- if blank, the system generates a code;
- automatic generation selects the lowest number that has never been assigned;
- a manually entered high number does not advance generation past lower gaps;
- assigned codes are immutable and never recycled;
- sold or inactive records remain stored, preserving their codes;
- generation must eventually be transaction-safe to prevent simultaneous duplicate assignments.

`UsedCar.code` and `Accessory.code` now use `assign_code()`, the shared generator (lowest-never-assigned number, transaction-safe retry on collision). **Still not implemented:** `CarModel.code` is not unique or automatically generated, and code-history protection (preventing reassignment of a retired code) doesn't exist yet.

### 7.6 Cart

```text
CustomerProfile 1 ---- 1 Cart 1 ---- * CartItem
                                         |
                                         1
                                         |
                              CartItemConfiguration
                                         |
                                         *
                                  CartItemFeature
```

- A customer has at most one cart.
- A `CartItem` currently references only `CarModel`; used cars cannot yet be added.
- `base_price` and `unit_price` are snapshots stored when adding the item.
- `CartItemConfiguration` stores selected engine, transmission, brake, exhaust, and wheel package join rows.
- `CartItemFeature` stores selected feature join rows.
- Matching configurations are intended to merge by increasing quantity.

A used car must never use quantity greater than one. Its future cart and reservation flow must be designed separately from repeatable new-car quantities.

### 7.7 Accessories and recommendations

Planned examples include floor mats, paint-protection film, tint, rain covers, stickers, spoilers, and front splitters.

The intended separation is:

- an `Accessory` catalog record describes the product or installation service;
- compatibility records determine which vehicles can use it;
- cart/order selections record what a customer chose;
- completed order lines provide real sales counts for recommendations.

Until completed orders exist, the application cannot truthfully calculate “best-selling” accessories. A temporary featured-accessory flag or compatible-accessory list may be used during development.

`Accessory` has `price` and optional `vip_price`, plus optional `requires_installation`/`installation_fee`. VIP price visibility must follow the same rule as new cars (§10): only staff or `VIP`-group members ever see `vip_price`, via gated `SerializerMethodField`s like `CarListSerializer`, not a plain passthrough field.

## 8. API surface

All paths below are relative to the backend host.

### Authentication and accounts

| Method | Path | Authentication | Purpose |
|---|---|---|---|
| POST | `/api/token/` | Public | Obtain JWT access and refresh tokens |
| POST | `/api/token/refresh/` | Refresh token | Obtain a new access token |
| POST | `/api/accounts/register/` | Public | Create a Django user and customer profile |
| GET | `/api/accounts/me/` | JWT | Return the current customer profile |
| GET | `/api/accounts/users/` | JWT | List users |

**Security note:** `/api/accounts/users/` currently allows any authenticated user to list user IDs, usernames, and emails. It should probably be restricted to staff or removed.

### Catalog, configuration, and cart

| Method | Path | Authentication | Purpose |
|---|---|---|---|
| GET | `/api/cars/` | Public | Paginated new-car list |
| GET | `/api/cars/cars/<id>/` | Public | New-car detail and configuration options |
| POST | `/api/cars/configurator/` | Public | Calculate configured new-car price |
| POST | `/api/cars/cart/add/` | JWT | Add or merge a configured new car |
| GET | `/api/cars/cart/` | JWT | Return current customer's cart |
| DELETE | `/api/cars/cart/item/<id>/remove/` | JWT | Remove one cart item |
| PATCH | `/api/cars/cart/item/<id>/update/` | JWT | Set cart-item quantity |
| GET | `/api/cars/used-cars/` | Public | Paginated used-car list (`status='available'` only) |
| GET | `/api/cars/used-cars/<id>/` | Public | Used-car detail (`status='available'` only) |

The new-car list supports:

- `brand` text filtering;
- exact `year` filtering;
- `min_price` and `max_price`;
- `sort` values for price, year, brand, and model, optionally prefixed with `-`;
- `page` and `page_size`, with a maximum page size of 50.

The used-car list supports the same `sort`/`page`/`page_size` plus `brand`, `year`, `min_price`, `max_price`, `condition`, and `fuel_type` filtering (`UsedCarFilter`).

The route `/api/cars/cars/<id>/` contains a repeated `cars` segment because the app itself is mounted at `/api/cars/` and its detail pattern begins with `cars/`.

## 9. Main backend workflows

### 9.1 New-car listing

1. Query `CarModel` with its `Car` and `Brand`.
2. Apply django-filter parameters.
3. Apply an allow-listed sort field.
4. Paginate.
5. Serialize price visibility according to authentication, staff status, and VIP group membership.

### 9.2 New-car detail

The detail response combines base model data, images, dimensional specifications, configuration join rows, feature groups, and prices.

**Known issue:** `car_detail` currently prefetches `car_model_engine_set`, but the model's related name is `car_model_engine`. This should be corrected and tested.

### 9.3 Configuration calculation

The client submits a car-model ID and optional join-row IDs. The backend verifies that option rows belong to the selected car, adds their price adjustments, and returns a total and breakdown.

Object lookup errors for several option IDs are not consistently converted into controlled `400` or `404` responses.

### 9.4 Add to cart

The endpoint validates input, obtains the customer's cart, calculates a unit price, validates one feature per category, searches for an identical configuration, and either increments quantity or creates cart/configuration rows.

**Fixed:** the VIP unit-price check now matches the serializers' `is_staff`/`VIP`-group condition, and falls back to `car.price` when `car.vip_price` is `None` (previously referenced the nonexistent `customer.is_vip` field and could crash on a null VIP price).

**Known issues (still open):**

- selected feature prices are added inside a nested loop and may be counted multiple times;
- several direct `.get()` calls can raise unhandled exceptions;
- debugging `print()` calls remain in matching logic;
- there are no automated cart tests.

## 10. Authentication and price visibility

JWT access tokens expire after 60 minutes. JWT is the default DRF authentication mechanism.

Current new-car list behavior:

- anonymous or normal customer: normal price;
- VIP group member: VIP price;
- staff: normal and VIP prices.

Internal cost must never be exposed to ordinary customers. This VIP-visibility rule now applies identically to new cars (`CarDetailSerializer`/`CarListSerializer`), used cars (`UsedCarSerializer`), and accessories (`AccessorySerializer`): `vip_price` is a gated `SerializerMethodField`, `None` unless the requesting user is staff or in the `VIP` group, with a paired `is_vip_visible` flag.

## 11. Frontend

The React application currently renders a single landing page containing navigation, hero content, a catalog, feature marketing, contact content, and a footer.

### Current behavior

- `App.js` passes `carsData.js` into `CarCatalog`.
- Catalog search and category filtering happen in browser memory.
- `CarCard` opens `CarDetail` and maintains a non-persistent local “liked” state.
- `CarDetail` uses static/fallback specifications and a simulated contact form.
- `AuthContext` stores simulated users, plaintext passwords, and fake tokens in `localStorage`.
- `BuyModal` displays an alert; it does not create a backend order.
- `CompareTool`, `BuyModal`, and `FinancingCalculator` exist but are not connected from `App.js`.
- `ThemeContext` exists but `ThemeProvider` is not mounted by `index.js` or `App.js`.
- There are currently no `fetch` or Axios calls to the backend.

### Required integration direction

1. Establish a configurable backend base URL.
2. Connect registration, JWT login, token storage, and profile retrieval.
3. Replace `carsData.js` with the new-car list endpoint.
4. Adapt frontend field names and price formatting to backend JSON.
5. Connect car detail and configuration calculation.
6. Connect cart actions.
7. Add used-car pages after used-car APIs exist.
8. Replace the simulated purchase request with booking/order behavior.

Passwords must never be stored in frontend `localStorage` after real authentication is connected.

## 12. Local development

### Backend

From the repository root on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
Set-Location CarHub_backend
python manage.py migrate
python manage.py runserver
```

MySQL must be running and the `carhub` database must exist. Current development settings expect:

```text
Host: localhost
Port: 3306
Database: carhub
User: root
Password: empty
```

Create an admin user when needed:

```powershell
python manage.py createsuperuser
```

Useful verification commands:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py showmigrations
python manage.py test
```

### Frontend

```powershell
Set-Location CarHub_Frontend
npm install
npm start
```

The frontend currently runs independently and does not need the backend for its static demo data.

## 13. Environment and deployment concerns

Current settings are development-only:

- `SECRET_KEY` is committed in source;
- `DEBUG` is enabled;
- `ALLOWED_HOSTS` is empty;
- database credentials are hard-coded;
- Django uses UTC rather than the project's Cambodia timezone;
- CORS is not configured for a separately hosted React frontend;
- uploaded media is served by Django only in debug mode;
- a stale `db.sqlite3` file exists even though settings use MySQL.

Before deployment, move secrets and database settings to environment variables, configure allowed hosts and CORS, choose a media-storage solution, run Django's deployment checks, and use a production web server.

## 14. Testing status

Both `cars/tests.py` and `accounts/tests.py` are currently empty. Manual verification has been used, but it is not enough to protect pricing, authorization, and order logic.

High-priority automated tests:

1. Registration creates exactly one customer profile.
2. Anonymous, normal, VIP, and staff price visibility.
3. Catalog filtering, sorting, and pagination.
4. Car detail option grouping and image URLs.
5. Configuration rejects option IDs belonging to another car.
6. Cart price calculations and identical-configuration matching.
7. Used-car VIN, status, and price validation.
8. Public used-car queries exclude reserved and sold vehicles.
9. Internal-code format, manual uniqueness, lowest-gap generation, immutability, and concurrent creation.
10. A used car cannot be reserved or sold twice.

## 15. Current roadmap

### Immediate

1. Implement and test internal codes for new and used cars.
2. Add a used-car image model and admin inline.
3. Add used-car list/detail serializers.
4. Add public used-car list/detail endpoints that expose only available inventory.
5. Add used-car filtering and tests.

### Next

1. Design a shared cart/order representation for new cars, unique used cars, and accessories.
2. Create accessory catalog and compatibility models.
3. Design inventory for in-stock new cars versus made-to-order/import vehicles.
4. Design booking, reservation, order, sale, and payment state transitions.
5. Preserve price and product-description snapshots on order lines.

### Later

1. Calculate best-selling compatible accessories from completed order lines.
2. Connect the React frontend to the real API.
3. Add staff reporting, auditing, and profitability views.
4. Prepare production configuration and deployment.

## 16. Contributor working rules

- Read this file and `PROGRESS.md` before changing a subsystem.
- Do not confuse database IDs, VINs, and CarHub internal codes.
- Do not expose acquisition cost through customer APIs.
- Do not delete sold vehicles or recycle assigned internal codes.
- Treat every used car as quantity one.
- Use `Decimal`, not floating-point numbers, for money.
- Preserve price snapshots on cart/order records rather than recalculating history from current catalog prices.
- Generate and review migrations before applying them.
- Add tests with every pricing, authentication, inventory, or state-transition feature.
- Update API tables and roadmap status in this document when behavior changes.

