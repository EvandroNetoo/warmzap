from dataclasses import dataclass

from django.db import models


class SubscriptionPlanChoices(models.TextChoices):
    NO_PLAN = 'no plan', 'Sem plano'
    DISCOVERY = 'discovery', 'Descoberta'
    ASCENSION = 'ascension', 'Ascensão'
    ELITE = 'elite', 'Elite'
    VANGUARD = 'vanguard', 'Vanguard'
    PRODIGY = 'prodigy', 'Prodígio'
    SUPREME = 'supreme', 'Supremo'
    LEGENDARY = 'legendary', 'Lendário'
    INFINITY = 'infinity', 'Infinity'


@dataclass
class SubscriptionPlan:
    value: str
    label: str
    price: float
    chips_limit: int


SUBSCRIPTION_PLANS_SETTINGS = {
    SubscriptionPlanChoices.NO_PLAN: SubscriptionPlan(
        value=SubscriptionPlanChoices.NO_PLAN.value,
        label=SubscriptionPlanChoices.NO_PLAN.label,
        chips_limit=0,
        price=0.0,
    ),
    SubscriptionPlanChoices.DISCOVERY: SubscriptionPlan(
        value=SubscriptionPlanChoices.DISCOVERY.value,
        label=SubscriptionPlanChoices.DISCOVERY.label,
        chips_limit=1,
        price=50.0,
    ),
    SubscriptionPlanChoices.ASCENSION: SubscriptionPlan(
        value=SubscriptionPlanChoices.ASCENSION.value,
        label=SubscriptionPlanChoices.ASCENSION.label,
        chips_limit=5,
        price=125.0,
    ),
    SubscriptionPlanChoices.ELITE: SubscriptionPlan(
        value=SubscriptionPlanChoices.ELITE.value,
        label=SubscriptionPlanChoices.ELITE.label,
        chips_limit=10,
        price=225.0,
    ),
    SubscriptionPlanChoices.VANGUARD: SubscriptionPlan(
        value=SubscriptionPlanChoices.VANGUARD.value,
        label=SubscriptionPlanChoices.VANGUARD.label,
        chips_limit=50,
        price=500.0,
    ),
    SubscriptionPlanChoices.PRODIGY: SubscriptionPlan(
        value=SubscriptionPlanChoices.PRODIGY.value,
        label=SubscriptionPlanChoices.PRODIGY.label,
        chips_limit=100,
        price=850.0,
    ),
    SubscriptionPlanChoices.SUPREME: SubscriptionPlan(
        value=SubscriptionPlanChoices.SUPREME.value,
        label=SubscriptionPlanChoices.SUPREME.label,
        chips_limit=200,
        price=1600.0,
    ),
    SubscriptionPlanChoices.LEGENDARY: SubscriptionPlan(
        value=SubscriptionPlanChoices.LEGENDARY.value,
        label=SubscriptionPlanChoices.LEGENDARY.label,
        chips_limit=500,
        price=3750.0,
    ),
    SubscriptionPlanChoices.INFINITY: SubscriptionPlan(
        value=SubscriptionPlanChoices.INFINITY.value,
        label=SubscriptionPlanChoices.INFINITY.label,
        chips_limit=float('inf'),
        price=float('inf'),
    ),
}
