import logging
import requests
from celery.exceptions import MaxRetriesExceededError
from pretix.base.models import Event, Order, OrderPosition
from pretix.base.services.tasks import TransactionAwareTask
from pretix.celery_app import app

logger = logging.getLogger(__name__)


@app.task(
    base=TransactionAwareTask,
    bind=True,
    max_retries=10,
    retry_backoff=True,
    retry_backoff_max=3600,
)
def matrix_inviter_invite(self, event: int, order: int, order_position: int):
    order_position = OrderPosition.objects.get(pk=order_position)

    user_matrix_id = order_position.meta_info_data.get("question_form_data", {}).get(
        "matrix_inviter_matrix_id"
    )

    if not user_matrix_id:
        return

    event = Event.objects.get(pk=event)
    order = Order.objects.get(pk=order)
    room_matrix_id = event.settings.matrix_inviter_matrix_room

    try:
        r = requests.post(
            "https://{}/_matrix/client/v3/rooms/{}/invite".format(
                event.settings.matrix_inviter_matrix_server,
                room_matrix_id,
            ),
            headers={
                "Authorization": "Bearer {}".format(
                    event.settings.matrix_inviter_authorization_token
                ),
            },
            json={
                "user_id": user_matrix_id,
            },
        )
        r.raise_for_status()
    except (requests.ConnectionError, requests.HTTPError) as e:
        try:
            self.retry()
        except MaxRetriesExceededError:
            order.log_action(
                "pretix_matrix_inviter.error",
                data={
                    "matrix_id": user_matrix_id,
                    "matrix_room": room_matrix_id,
                    "error": "HTTP Code {}".format(r.status_code),
                },
            )
            raise e

    order.log_action(
        "pretix_matrix_inviter.invite_sent",
        data={
            "matrix_id": user_matrix_id,
            "matrix_room": room_matrix_id,
        },
    )
