import logging
from notifications.emailer import send_email
import json

class EmailHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.events = {}

    def emit(self, record):

        executor = getattr(record, "executor", None)
        # if executor != 'scheduler':
        #     return

        uuid = getattr(record, "uuid", None)
        if not uuid:
            return

        if record.levelno == 29:
            self.send_summary(uuid)
            return

        if uuid not in self.events:
            self.events[uuid] = {
                "new": [],
                "filled": []
            }


        if record.levelno == 25:
            self.events[uuid]["new"].append(record)

        elif record.levelno == 27:
            self.events[uuid]["filled"].append(record)

    def send_summary(self, uuid):

        events = self.events.pop(uuid, None)

        if not events:
            return

        if events["filled"]:

            lines = []
            html_lines = []

            sorted_filled = sorted(
                events["filled"],
                key=lambda r: json.loads(r.info)["source"].lower()
            )

            for idx, record in enumerate(sorted_filled, start=1):
                job = json.loads(record.info)

                lines.append(
                    f'{idx}. {job["source"]} - '
                    f'{job.get("job_id", job["url"])} - '
                    f'{job["job_name"]}'
                )

                html_lines.append(
                    f'<p>{idx}. {job["source"]} - '
                    f'{job.get("job_id", job["url"])} - '
                    f'<a href="{job["url"]}">'
                    f'{job["job_name"]}</a></p>'
                )

            send_email(
                f"Filled Positions ({len(sorted_filled)})",
                "\n".join(lines),
                "\n".join(html_lines),
                "System"
            )

        if events["new"]:

            summary_links = []

            sorted_new = sorted(
                events["new"],
                key=lambda r: json.loads(r.info)["source"].lower()
            )

            for idx, record in enumerate(sorted_new, start=1):
                job = json.loads(record.info)

                html_link = (
                    f'<p>{idx}. {job["source"]} - '
                    f'<a href="{job["url"]}">'
                    f'{job["job_name"]}</a></p>'
                )

                summary_links.append(html_link)

            send_email(
                f"New Jobs List ({len(sorted_new)})",
                "",
                "\n".join(summary_links),
                "new"
            )
