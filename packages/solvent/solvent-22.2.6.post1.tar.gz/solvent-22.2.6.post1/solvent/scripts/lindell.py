import time

import log
import pomace

from . import Script


class MyPillow(Script):

    URL = "https://www.mypillow.com/"

    def run(self, page) -> pomace.Page:
        person = pomace.fake.person

        pomace.shared.client.clear_cookies()
        page = pomace.visit(self.URL)

        log.debug("Waiting for modal...")
        for _ in range(10):
            time.sleep(0.5)
            modal = pomace.shared.browser.find_by_id("ltkpopup-content")
            if modal and modal.visible:
                break
        else:
            log.warn("No modal found")

        log.info(f"Submitting email address: {person.email_address}")
        page.fill_email_address(person.email_address)
        page = page.click_activate_offer(wait=1)
        log.info(f"Submitting phone number: {person.phone}")
        page.fill_phone(person.phone)
        return page.click_get_mobile_alerts(wait=1)

    def check(self, page) -> bool:
        success = "Thanks!" in page
        if success:
            page.click_continue_shopping(wait=0)
        return success


class FrankSpeech(Script):

    URL = "https://frankspeech.com/"
    SKIP = True

    def run(self, page) -> pomace.Page:
        log.info("Clearing cookies")
        pomace.shared.client.clear_cookies()
        page = pomace.visit(self.URL)

        page.fill_phone_number(pomace.fake.phone_number.replace("-", ""))
        return page.click_submit()

    def check(self, page) -> bool:
        return "home" in page.url
