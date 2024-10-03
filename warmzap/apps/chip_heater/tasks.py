import json
from datetime import timedelta
from random import randint

from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from chip_heater.models import Chip, Message


@shared_task
def send_message_and_schedule_next(chip_id: int):
    chip = Chip.objects.get(id=chip_id)
    send_to = (
        Chip.objects.filter(stage=Chip.StageChoices.STARTED)
        .order_by('?')
        .first()
        .number
    )
    message = Message.objects.all().order_by('?').first()

    chip.send_message(send_to, message.message)

    next_message_time = timezone.now() + timedelta(seconds=randint(30, 180))  # noqa: S311
    start_hour = 8
    end_hour = 21
    if start_hour > next_message_time.hour >= end_hour:
        next_message_time = (timezone.now() + timedelta(days=1)).replace(
            hour=8
        )

    schedule = ClockedSchedule.objects.create(clocked_time=next_message_time)
    PeriodicTask.objects.create(
        clocked=schedule,
        name=f'mensagem {chip.id} {chip.name} {next_message_time}',
        task='chip_heater.tasks.send_message_and_schedule_next',
        args=json.dumps([chip.id]),
        one_off=True,
    )
