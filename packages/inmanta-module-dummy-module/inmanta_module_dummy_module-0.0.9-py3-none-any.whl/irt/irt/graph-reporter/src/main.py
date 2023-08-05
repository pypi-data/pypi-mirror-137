"""
    :copyright: 2020 Inmanta
    :contact: code@inmanta.com
    :license: Inmanta EULA
"""
import json
import logging
import os
import tempfile
import time
from typing import List, Optional, Tuple

import click
import requests
from slack_sdk import WebClient

LOGGER = logging.getLogger("graph-reporter")


class GraphSpec:
    def __init__(
        self,
        base_url: str,
        title: str,
        dashboard_id: str,
        panel_id: int,
        extra_query_params: List[str] = [],
    ) -> None:
        self.base_url = base_url
        self.title = title
        self.dashboard_id = dashboard_id
        self.panel_id = panel_id
        self.extra_query_params = extra_query_params

    def _get_from_and_to_time(self, time_window_days: int) -> Tuple[int, int]:
        now_millis = int(time.time() * 1000)
        from_time = now_millis - (time_window_days * 24 * 60 * 60 * 1000)
        to_time = now_millis
        return from_time, to_time

    def _get_image_renderer_url(self, time_window_days: int) -> str:
        from_time, to_time = self._get_from_and_to_time(time_window_days)
        path = f"/render/d-solo/{self.dashboard_id}"
        params = f"?orgId=1&panelId={self.panel_id}&from={from_time}&to={to_time}&width=1000&height=500&tz=Europe%2FBrussels"
        extra_params = (
            f"&{'&'.join(self.extra_query_params)}" if self.extra_query_params else ""
        )
        return f"{self.base_url}{path}{params}{extra_params}"

    def get_view_panel_url(self, time_window_days: int) -> str:
        from_time, to_time = self._get_from_and_to_time(time_window_days)
        path = f"/d/{self.dashboard_id}"
        params = f"?orgId=1&viewPanel={self.panel_id}&from={from_time}&to={to_time}"
        extra_params = (
            f"&{'&'.join(self.extra_query_params)}" if self.extra_query_params else ""
        )
        return f"{self.base_url}{path}{params}{extra_params}"

    def download_graph(self, time_window_days: int, destination_file_name: str) -> None:
        url = self._get_image_renderer_url(time_window_days)
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        with open(destination_file_name, "wb") as f:
            f.write(response.content)


def send_graphs_to_slack(
    slack_token: str,
    channel_id: str,
    file_to_upload: str,
    title: str,
    comment: str,
    thread_ts: Optional[str] = None,
) -> str:
    client = WebClient(token=slack_token)
    # The join call is idempotent
    client.conversations_join(channel=channel_id)

    optional_params = {"thread_ts": thread_ts} if thread_ts else {}
    response = client.files_upload(
        channels=channel_id,
        file=file_to_upload,
        title=title,
        filetype="png",
        initial_comment=comment,
        **optional_params,
    )
    if not thread_ts:
        return response["file"]["shares"]["public"][channel_id][0]["ts"]
    else:
        return thread_ts


@click.command()
@click.option(
    "--slack-token",
    default=lambda: os.getenv("SLACK_TOKEN"),
    show_default="$SLACK_TOKEN",
    required=True,
)
@click.option("--channel-id", required=True)
@click.argument("index_file", type=click.File("r"))
def main(slack_token: str, channel_id: str, index_file) -> None:
    logging.basicConfig(level=logging.INFO)

    index_content = json.load(index_file)
    base_url = str(index_content["base_url"])
    time_window_days = index_content["time_window_days"]
    if not isinstance(time_window_days, int):
        raise Exception("Config option `time_window_days` should be an integer")
    if time_window_days <= 0:
        raise Exception("Config option `time_window_days` should be a positive number")

    with tempfile.TemporaryDirectory() as dir_name:
        thread_ts = None
        for graph in index_content["graphs"]:
            graph_spec = GraphSpec(base_url=base_url, **graph)
            LOGGER.info("Processing image with title: %s", graph_spec.title)
            file_name = os.path.join(
                dir_name, f"{graph_spec.title.replace(' ', '-')}.png"
            )
            graph_spec.download_graph(time_window_days, file_name)
            # Send first message to channel and the rest as a reply to the first message
            thread_ts = send_graphs_to_slack(
                slack_token=slack_token,
                channel_id=channel_id,
                file_to_upload=file_name,
                title=graph_spec.title,
                comment=graph_spec.get_view_panel_url(time_window_days),
                thread_ts=thread_ts,
            )
            os.remove(file_name)


if __name__ == "__main__":
    main()
