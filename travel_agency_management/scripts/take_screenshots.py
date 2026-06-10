#!/usr/bin/env python3
import asyncio
import json
import os
from pathlib import Path
from urllib.parse import urlencode

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright


ODOO_URL = os.environ.get("ODOO_URL", "http://localhost:8069").rstrip("/")
ODOO_LOGIN = os.environ.get("ODOO_LOGIN", "admin")
ODOO_PASSWORD = os.environ.get("ODOO_PASSWORD", "admin")
ODOO_DB = os.environ.get("ODOO_DB", "database")

MODULE_DIR = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = MODULE_DIR / "docs" / "screenshots"


async def wait_odoo(page, delay=1800):
    try:
        await page.wait_for_load_state("load", timeout=10000)
    except PlaywrightTimeoutError:
        pass
    await page.wait_for_timeout(delay)


async def rpc(page, model, method, args=None, kwargs=None):
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": model,
            "method": method,
            "args": args or [],
            "kwargs": kwargs or {},
        },
        "id": 1,
    }

    response = await page.context.request.post(
        f"{ODOO_URL}/web/dataset/call_kw/{model}/{method}",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )

    data = await response.json()

    if data.get("error"):
        raise RuntimeError(data["error"])

    return data.get("result")


async def xmlid(page, external_id):
    if "." not in external_id:
        raise RuntimeError(f"External ID invalide: {external_id}")

    module, name = external_id.split(".", 1)

    records = await rpc(
        page,
        "ir.model.data",
        "search_read",
        [
            [
                ["module", "=", module],
                ["name", "=", name],
            ]
        ],
        {
            "fields": ["res_id", "model"],
            "limit": 1,
        },
    )

    if not records:
        raise RuntimeError(
            f"External ID introuvable: {external_id}. "
            "Vérifie que le module est installé et que les données demo sont chargées."
        )

    return records[0]["res_id"]


async def login(page):
    db_name = ODOO_DB or "database"

    login_url = f"{ODOO_URL}/web/login?{urlencode({'db': db_name})}"
    await page.goto(login_url, wait_until="domcontentloaded")
    await page.wait_for_timeout(1500)

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    await page.screenshot(
        path=str(SCREENSHOT_DIR / "_debug_login_page.png"),
        full_page=True,
    )

    visible_login_count = await page.locator("input[name='login']:visible").count()

    if visible_login_count == 0:
        # Odoo may already be logged in or may have redirected to the backend.
        await page.goto(
            f"{ODOO_URL}/web?{urlencode({'db': db_name})}",
            wait_until="domcontentloaded",
        )
        await wait_odoo(page)
        await page.wait_for_timeout(1500)
        return

    login_input = page.locator("input[name='login']:visible").first
    password_input = page.locator("input[name='password']:visible").first
    submit_button = page.locator("button[type='submit']:visible").first

    await login_input.wait_for(state="visible", timeout=60000)
    await login_input.fill(ODOO_LOGIN)

    await password_input.wait_for(state="visible", timeout=60000)
    await password_input.fill(ODOO_PASSWORD)

    await submit_button.wait_for(state="visible", timeout=60000)
    await submit_button.click()

    await wait_odoo(page)
    await page.wait_for_timeout(2000)

    if await page.locator("input[name='login']:visible").count() > 0:
        await page.screenshot(
            path=str(SCREENSHOT_DIR / "_debug_login_failed.png"),
            full_page=True,
        )
        raise RuntimeError(
            "Login failed: Odoo still shows the login page. "
            "Check ODOO_LOGIN, ODOO_PASSWORD, and ODOO_DB."
        )


async def goto_backend(page, action=None, model=None, view_type=None, res_id=None):
    params = {}

    if action:
        params["action"] = action
    if model:
        params["model"] = model
    if view_type:
        params["view_type"] = view_type
    if res_id:
        params["id"] = res_id

    await page.goto(f"{ODOO_URL}/web#{urlencode(params)}", wait_until="domcontentloaded")
    await wait_odoo(page)
    await page.wait_for_timeout(1800)


async def capture(page, filename):
    path = SCREENSHOT_DIR / filename
    await page.screenshot(path=str(path), full_page=True)

    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"Capture vide ou absente: {path}")

    print(f"OK {filename}")


async def prepare_existing_booking_for_screenshots(page, booking_id):
    data = await rpc(
        page,
        "travel.booking",
        "read",
        [[booking_id], ["state", "sale_order_id"]],
    )

    state = data[0].get("state")
    sale_order = data[0].get("sale_order_id")
    sale_order_id = sale_order[0] if sale_order else False

    if not sale_order_id:
        if state in ("draft", "submitted"):
            try:
                if state == "draft":
                    await rpc(page, "travel.booking", "action_submit", [[booking_id]])
                await rpc(page, "travel.booking", "action_approve", [[booking_id]])
            except Exception as exc:
                print(f"INFO approval skipped or already done: {exc}")

        await rpc(page, "travel.booking", "action_create_sale_order", [[booking_id]])

        data = await rpc(
            page,
            "travel.booking",
            "read",
            [[booking_id], ["sale_order_id"]],
        )
        sale_order = data[0].get("sale_order_id")
        sale_order_id = sale_order[0] if sale_order else False

    if not sale_order_id:
        raise RuntimeError("Impossible de trouver ou créer le devis pour la réservation.")

    try:
        await rpc(page, "travel.booking", "action_confirm_booking", [[booking_id]])
    except Exception as exc:
        print(f"INFO confirmation skipped or already done: {exc}")

    return booking_id, sale_order_id


async def main():

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 1000})

        await login(page)

        action_destination = await xmlid(
            page,
            "travel_agency_management.action_travel_destination",
        )
        action_package = await xmlid(
            page,
            "travel_agency_management.action_travel_package",
        )
        action_departure = await xmlid(
            page,
            "travel_agency_management.action_travel_departure",
        )
        action_booking = await xmlid(
            page,
            "travel_agency_management.action_travel_booking",
        )
        action_analysis = await xmlid(
            page,
            "travel_agency_management.action_travel_booking_analysis",
        )

        destination_id = await xmlid(
            page,
            "travel_agency_management.destination_marrakech",
        )
        package_id = await xmlid(
            page,
            "travel_agency_management.package_marrakech",
        )
        departure_id = await xmlid(
            page,
            "travel_agency_management.departure_marrakech",
        )
        booking_draft_id = await xmlid(
            page,
            "travel_agency_management.booking_marrakech_draft",
        )
        booking_submitted_id = await xmlid(
            page,
            "travel_agency_management.booking_istanbul_submitted",
        )
        booking_approved_id = await xmlid(
            page,
            "travel_agency_management.booking_paris_approved",
        )
        customer_id = await xmlid(
            page,
            "travel_agency_management.partner_customer_sara",
        )
        package_dubai_id = await xmlid(
            page,
            "travel_agency_management.package_dubai",
        )
        nationality_id = await xmlid(page, "base.ma")

        await page.goto(f"{ODOO_URL}/web", wait_until="domcontentloaded")
        await wait_odoo(page)
        await page.wait_for_timeout(1500)
        await capture(page, "01_menu_principal.png")

        await goto_backend(page, action_destination, "travel.destination", "list")
        await capture(page, "02_liste_destinations.png")

        await goto_backend(
            page,
            action_destination,
            "travel.destination",
            "form",
            destination_id,
        )
        await capture(page, "03_formulaire_destination.png")

        await goto_backend(page, action_package, "travel.package", "list")
        await capture(page, "04_liste_packages.png")

        await goto_backend(
            page,
            action_package,
            "travel.package",
            "form",
            package_id,
        )
        await capture(page, "05_formulaire_package.png")

        await goto_backend(page, action_departure, "travel.departure", "list")
        await capture(page, "06_liste_departs.png")

        await goto_backend(
            page,
            action_departure,
            "travel.departure",
            "form",
            departure_id,
        )
        await capture(page, "07_formulaire_depart.png")

        await goto_backend(page, action_booking, "travel.booking", "list")
        await capture(page, "08_liste_reservations.png")

        await goto_backend(
            page,
            action_booking,
            "travel.booking",
            "form",
            booking_draft_id,
        )
        await capture(page, "09_reservation_brouillon.png")

        await goto_backend(
            page,
            action_booking,
            "travel.booking",
            "form",
            booking_submitted_id,
        )
        await capture(page, "10_reservation_soumise.png")

        await goto_backend(
            page,
            action_booking,
            "travel.booking",
            "form",
            booking_approved_id,
        )
        await capture(page, "11_reservation_approuvee.png")

        workflow_booking_id, sale_order_id = await prepare_existing_booking_for_screenshots(
            page,
            booking_approved_id,
        )

        sale_action = await xmlid(page, "sale.action_orders")

        await goto_backend(page, sale_action, "sale.order", "form", sale_order_id)
        await capture(page, "12_devis_odoo.png")

        await goto_backend(
            page,
            action_booking,
            "travel.booking",
            "form",
            workflow_booking_id,
        )
        await capture(page, "13_reservation_confirmee.png")

        await page.goto(
            f"{ODOO_URL}/report/html/"
            f"travel_agency_management.report_travel_booking_document/"
            f"{workflow_booking_id}",
            wait_until="domcontentloaded",
        )
        await wait_odoo(page)
        await page.wait_for_timeout(1500)
        await capture(page, "14_bon_reservation_pdf.png")

        await goto_backend(page, action_analysis, "travel.booking", "graph")
        await capture(page, "15_vue_graph_reservations.png")

        await goto_backend(page, action_analysis, "travel.booking", "pivot")
        await capture(page, "16_vue_pivot_reservations.png")

        try:
            groups_action = await xmlid(page, "base.action_res_groups")
            await goto_backend(page, groups_action, "res.groups", "list")
            await capture(page, "17_groupes_securite.png")
        except (RuntimeError, PlaywrightTimeoutError) as exc:
            print(f"SKIP 17_groupes_securite.png: {exc}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())