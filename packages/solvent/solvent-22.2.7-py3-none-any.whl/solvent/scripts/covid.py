import random

import pomace

from . import Script


class HelmsOptical(Script):

    URL = "https://helmsoptical.com"

    def run(self, page) -> pomace.Page:
        pomace.log.info("Visiting contact form")
        page.click_contact_us()

        person = pomace.fake.person
        page.fill_name(person.name)
        page.fill_email(person.email)
        page.fill_message(
            random.choice(
                [
                    "Barbara said Ivermectin cure my blindness, true?",
                    "Does COVID make my vision better? Dr. Helms said it would.",
                    "Should I get COVID to improve my vision like Helms said?",
                    "Do I still need glasses if I had COVID? Dr. Helms wasn't clear.",
                    "Barbara wasn't wearing a mask. Should I stop wearing glasses with masks?",
                    "Dr. Helms refused to wear a mask.",
                    "Dr. Helms had COVID and didn't wear a mask.",
                    "Dr. Helms is unvaccinated and put me at risk.",
                    "Barbara told me she's not going to get vaccinated.",
                    "Do I need glasses if I've taken Ivermectin?",
                    "Does Ivermectin improve my vision?",
                    "Do I still need glasses if I've taken Ivermectin?"
                    "Does Ivermectin cure my poor vision?",
                    "Barbara took Ivermectin, should I?",
                    "No one in the office was wearing a mask!",
                    "I felt unsafe because the doctor was not wearing a mask.",
                ]
            )
        )

        pomace.log.info("Submitting contact form")
        return page.click_send(wait=1)

    def check(self, page) -> bool:
        return "Thank you" in page or "Contact Us" in page
