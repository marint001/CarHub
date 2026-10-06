RESPONSE DEFAULTS (apply to every reply unless I override):
- Answer directly. No preamble, filler, affirmations, or trailing summary clauses.
- Use plain prose or tight lists. No decorative headers for short answers.
- Do not use Extended Thinking or web search unless my prompt is explicitly complex or time-sensitive.
- If a task is simple (formatting, grammar, short translation), note once that Haiku may suffice.
- At 15+ messages, offer once to summarize key context for a fresh chat.
- If I request a correction, note once that editing my last message saves tokens.

CarHub — session summary

Project: Django + DRF backend, React frontend (not yet connected). Long-form docs: SYSTEM_DOCUMENTATION.md and PROGRESS.md at repo root — read both before continuing. PROGRESS.md §6/§6a/§4 and "Known bugs fixed (2026-10-06 session)" are up to date.

User context: New to Python/coding, learning as they build. Wants to write model/logic code themselves; I review and explain concepts rather than writing it for them. Only implement directly if explicitly asked (documentation updates like this file are fine to do directly).

Status: Models/admin for CarModel, UsedCar, and Accessory (with compatibility) are all finished (migrations through 0013, applied). UsedCar is fully wired end-to-end: serializer, filter, views, URLs. Accessory serializer is done; filter/views/urls are not. Still nothing committed to git — all changes sitting uncommitted on the `marint` branch alongside older uncommitted work.

Done this session (user-written, reviewed by me):
- Fixed `add_to_cart`'s VIP-price bug — it referenced non-existent `customer.is_vip` and crashed for every user. Now checks `request.user.is_staff or request.user.groups.filter(name='VIP').exists()`, falling back to `car.price` when `car.vip_price` is `None`.
- Fixed `UsedCarSerializer` to actually gate `vip_price` (was a plain unguarded field — any user could read a used car's VIP price). Now matches `CarListSerializer`'s gated `SerializerMethodField` pattern.
- Wrote and fixed `AccessorySerializer`/`AccessoryCompatibilitySerializer`/`AccessoryImageSerializer`: had a wrong `Meta.model` (`CarModel` instead of `AccessoryCompatibility`), a `year` field sourced from a nonexistent `car.year`, and a `compatibility`/`compatibilities` related_name mismatch. All fixed; VIP-gated the same way.
- Cleaned up redundant `price`/`display_price`/`vip_price` field triples across `CarDetailSerializer`/`UsedCarSerializer`/`AccessorySerializer` — dropped `display_price`, kept `price` + gated `vip_price` + `is_vip_visible`.
- Confirmed `used_car_list`/`used_car_detail` are intentionally separate from `car_list`/`car_detail` (used cars and new cars are on different frontend pages) — no merged listing needed.

Ready for next chat:
1. Accessory filter (brand/year/min_price/max_price/requires_installation/compatibility — discussed, not written), `accessory_list`/`accessory_detail` views, `urls.py` entries. Mirrors the used-car pattern exactly.
2. Sanity-check used_car_list/used_car_detail against real DB rows (same verification CarDetailSerializer got) — still not done.
3. Nothing committed to git yet — worth doing before more work piles up uncommitted.

Two design gaps found in a prior session (logged in PROGRESS.md §2, §7, and the "To Do" section — non-blocking, don't derail the accessory work above unless the user wants to pivot):
- No exterior body-paint color option for new cars — Color is only wired into WheelPackage (rim/trim), CarModel has no paint field/join table. Fix mirrors the existing option pattern (CarModelEngine etc.): a CarModelColor join table + colors field on CarDetailSerializer + color_id on the configurator/cart serializers.
- No stock/inventory concept for new cars — UsedCar.status (available/reserved/sold) covers used cars since each row is one physical vehicle, but CarModel has no equivalent; the same config could have units in stock and units on order simultaneously. Probably belongs on the future Order/Sale model (§5), not CarModel itself. This feeds directly into the still-undesigned §5 "4 payment flows" work.
