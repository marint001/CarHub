# CarHub Progress Tracker

Last updated: 2026-10-06

Legend: [x] done and verified · [~] partially done / has known issues · [ ] not started

## 1. Car Catalog & Browsing
- [x] Models: Brand, Car, CarModel (backend/cars/models.py)
- [x] Admin entry for Brand/Car/CarModel (registered in cars/admin.py)
- [x] `car_list` API endpoint with filtering (cars/filters.py) and sorting
- [x] Pagination via PageNumberPagination
- [x] `CarListSerializer` with VIP/staff price visibility logic
- [ ] Frontend wired to `car_list` (currently uses static src/data/carsData.js)

## 2. Car Detail & Customization
- [x] Models: Engine, Transmission, Brake, Exhaust, WheelDesign/WheelSize/Tyre/TyreSize/Color/WheelPackage, FeatureCategory/Feature
- [x] Per-CarModel join tables: CarModelEngine, CarModelTransmission, CarModelBrake, CarModelExhaust, CarModelWheelPackage, CarModelFeature
- [x] All registered in Django admin - manufacturer data can be entered now
- [x] `CarDetailSerializer` - tested against real DB rows (car id 1 & 2), confirmed correct output
- [x] Feature grouping by category with `is_configurable` flag (fixed together)
- [x] `calculate_configuration` endpoint - price breakdown by selected options
- [x] `CarModelSpecification` (dimensions) wired into `CarDetailSerializer` via `specs` SerializerMethodField, handles cars with no specs row yet
- [x] Plain spec fields exposed: `drive`, `fuel_tank`, `seating_capacity`, `description`
- [x] Car images: `CarModelImage` model, migration applied, Pillow installed, MEDIA_URL/MEDIA_ROOT configured, admin inline on CarModel page, `images` field in `CarDetailSerializer` with working absolute URLs (verified with a real uploaded PNG)
- [ ] Data entry pass: enter a real manufacturer's full spec sheet for one car and verify every field end-to-end (this is the "next" step you described)
- [ ] Frontend wired to real car detail data
- [ ] **Gap found 2026-09-15:** no exterior body-paint color option exists for new cars. `Color` is currently only used inside `WheelPackage` (rim/trim color bundled into a wheel package) - `CarModel` has no paint-color field or join table, so `calculate_configuration`/`add_to_cart` can't price a paint choice. Fix would mirror the existing option pattern: a `CarModelColor` join table (`car_model` FK, `color` FK, `price`), then a `colors` field on `CarDetailSerializer` and a `color_id` on `CarConfigurationSerializer`/`AddToCartSerializer`.

## 3. Comparison Tool
- [ ] Backend: no dedicated compare endpoint yet - likely just needs multiple `car_detail` calls from frontend, revisit once data entry is done
- [ ] Frontend: CompareTool.js currently uses static carsData.js

## 4. Cart
- [x] Models: Cart, CartItem, CartItemConfiguration, CartItemFeature
- [x] `add_to_cart` - builds config, matches existing identical cart items, handles VIP pricing (fixed 2026-10-06, see below - was crashing for every user)
- [x] `view_cart` - lists items with computed cart_total
- [x] `remove_cart_item`
- [x] `update_cart_quantity` - fixed bug (was writing to non-existent `total_price` field), now wired to URL correctly
- [x] `CartConfigurationSerializer.get_wheel` - fixed bug (wrong field names `shape`/`size`), verified against real data
- [ ] Cart is only in-memory/pre-purchase - not yet linked to any Order/Sale concept

## 5. Purchase / Checkout / Booking (NOT STARTED)
- [ ] No Order/Sale/Booking model exists yet
- [ ] No Payment model exists yet
- [ ] No booking-fee / deposit field anywhere
- [ ] Design needed: 4 distinct payment flows (in-stock, used, made-to-order, import) - likely needs a status/state-machine field per order type
- [ ] This is the next big backend design task after data entry pass

## 6. Used Cars
- [x] Model `UsedCar` rebuilt - now shares structure with `CarModel` where it makes sense: `car` FK (not free-text brand/model), `year`, `code` (auto-generated, prefix `002`), `price`/`vip_price`/`cost`, `description`, timestamps
- [x] Used-car-specific fields: `mileage`, `condition` (excellent/good/fair/poor), `status` (available/reserved/sold), `vin` (validated 17-char), `transmission` FK, `fuel_type`, `exterior_color` FK
- [x] `UsedCar.compatible_accessories()` - same `(car, year)`-keyed lookup as `CarModel`
- [x] `UsedCarImage` model (mirrors `CarModelImage`), inlined on `UsedCarAdmin`
- [x] Registered in Django admin with a real `ModelAdmin` (list_display/list_filter/search_fields)
- [x] `CarBasicSerializer`, `UsedCarImageSerializer`, `UsedCarSerializer` - done, `exterior_color` nested via `ColorSerializer`, excludes `cost` (internal margin field)
- [x] `UsedCarFilter` in filters.py (brand/year/min_price/max_price/condition/fuel_type), mirrors `CarModelFilter`
- [x] `used_car_list` / `used_car_detail` views + URLs (`used-cars/`, `used-cars/<int:pk>/`) - both public (no auth), both filtered to `status='available'` per SYSTEM_DOCUMENTATION.md §15
- [x] Migrations 0010-0013 applied

## 6a. Accessories
- [x] Model `Accessory` - code-generated (prefix `003`), name, description, price, vip_price, requires_installation, installation_fee, timestamps
- [x] `AccessoryImage` model, inlined on `AccessoryAdmin`
- [x] `AccessoryCompatibility` - links an accessory to a `(car, year)` pair, so one record covers both the new-car listing and any used-car listing with that model/year; inlined on `AccessoryAdmin`
- [x] Registered in Django admin
- [x] `AccessoryImageSerializer`, `AccessoryCompatibilitySerializer`, `AccessorySerializer` (VIP-gated `vip_price`/`is_vip_visible`, same pattern as `CarListSerializer`/`UsedCarSerializer`)
- [ ] `AccessoryFilter`, `accessory_list`/`accessory_detail` views, `urls.py` entries - next task, mirrors §6's used-car pattern

## 7. Stock / Inventory (NOT STARTED)
- [ ] No stock/quantity-on-hand model or field exists for new or used cars
- [ ] Needed to distinguish "in stock now" vs "made to order" vs "import"
- [ ] **Gap found 2026-09-15:** every `CarModel` row today just represents "this configuration exists and can be priced" - there's no notion of physical units on the lot vs. a factory order. `UsedCar.status` (available/reserved/sold) already tracks this per-unit for used cars since each `UsedCar` row *is* one physical vehicle, but new cars have no equivalent - the same `CarModel` config could have some units in stock and others special-ordered at once. This likely belongs on the future `Order`/`Sale` model (§5), not on `CarModel` itself.

## 8. Auth / Accounts
- [x] Backend: CustomerProfile model, register_customer, customer_profile, JWT token endpoints (SimpleJWT)
- [ ] Frontend AuthContext.js is fully simulated (localStorage + setTimeout) - not connected to backend yet, intentional per team's plan (frontend integration deferred until design is finalized)

## Known bugs fixed (2026-09-15 session)
- [x] `UsedCarFilter` referenced non-existent `UsedCar.CONDITION_CHOICES`/`UsedCar.FUEL_TYPE_CHOICES` (AttributeError on import, would've crashed the whole app) - fixed to `UsedCar.Condition.choices` (nested TextChoices) and `FuelType.choices` (top-level TextChoices)
- [x] `used_car_list`/`used_car_detail` briefly had `@permission_classes([IsAuthenticated])` by mistake - removed, both are public endpoints
- [x] `CarDetailSerializer.get_features` now includes `is_configurable` per category, grouped by category id (was missing entirely)
- [x] `update_cart_quantity` was assigning to non-existent `CartItem.total_price` field - fixed to compute `total_price` as a local value
- [x] `CartConfigurationSerializer.get_wheel` referenced non-existent fields `wheel_design.shape` and `wheel_size.size` - fixed to `wheel_design.name` and `wheel_size.size_inch`
- [x] `config/urls.py` mounted `cars.urls` twice (`api/cars/` and bare `api/`) creating duplicate routes for every cars endpoint - removed the duplicate, canonical prefix is now `api/cars/`
- [x] `CarDetailSerializer` was missing several real model fields entirely (drive, fuel_tank, seating_capacity, description, specs, images) - added them
- [x] `CarModelImage` admin registration referenced an unimported name (NameError) - fixed import, added as inline on CarModelAdmin

## Known bugs fixed (2026-10-06 session)
- [x] `add_to_cart` referenced non-existent `customer.is_vip` (`CustomerProfile` has no such field) - crashed with `AttributeError` for every user, VIP or not, on every add-to-cart call. Fixed to the same `request.user.is_staff or request.user.groups.filter(name='VIP').exists()` check used in the serializers, with a fallback to `car.price` when `car.vip_price` is `None` (prevents `TypeError` from adding to `None`).
- [x] `UsedCarSerializer` was serializing `vip_price` as a plain passthrough field with no gating at all - any anonymous/non-VIP user could read a used car's VIP price. Fixed to gated `SerializerMethodField`s (`get_vip_price`/`get_is_vip_visible`), matching `CarListSerializer`.
- [x] `AccessoryCompatibilitySerializer` had `Meta.model = CarModel` (should be `AccessoryCompatibility`) and `year = IntegerField(source='car.year')` (`Car` has no `year` field at all - would've crashed on serialize; the real `year` lives on `AccessoryCompatibility` itself). Both fixed.
- [x] `AccessorySerializer.compatibility` field name didn't match the model's `related_name='compatibilities'` (no `source=` given) - would've crashed with `AttributeError`. Renamed field to `compatibilities`.
- [x] Removed redundant `price`/`display_price`/`vip_price` triple-exposure in `CarDetailSerializer`/`UsedCarSerializer`/`AccessorySerializer` - dropped `display_price` (was just repackaging the other two fields), kept `price` + gated `vip_price` + `is_vip_visible`. Also removed a leftover dead `display_price = SerializerMethodField()` declaration in `UsedCarSerializer` with no matching method.

## Ready for next session
- [ ] Sanity-check `used_car_list`/`used_car_detail` against real DB rows (same verification `CarDetailSerializer` got) - still not done
- [ ] Accessory filter/views/urls (§6a) - serializer is done, this is the remaining piece
- [ ] Nothing from the used-car or accessory work (filters.py/views.py/urls.py/serializers.py), or this session's cart fix, is committed to git yet - all still sitting uncommitted on `marint`

## To Do (open design questions, non-blocking)
- [ ] New-car exterior paint color option (see §2) - needs `CarModelColor` join table + serializer/configurator wiring
- [ ] Stock/inventory distinction for new cars: in-stock vs. made-to-order vs. import (see §7) - needs design decision on whether this lives on `CarModel`, a new `Order`/`Sale` model, or both
- [ ] PROGRESS.md §5 design needed: 4 distinct payment flows (in-stock, used, made-to-order, import) - depends on the stock/inventory decision above

## Notes on URL structure (for reference)
- All cars endpoints live under `api/cars/...` (e.g. `api/cars/cart/add/`, `api/cars/configurator/`)
- Accounts endpoints live under `api/accounts/...`
- JWT auth: `api/token/` and `api/token/refresh/`
- `include()` concatenates prefixes: the path defined inside `cars/urls.py` gets the app's mount prefix (`api/cars/`) stuck on the front automatically
