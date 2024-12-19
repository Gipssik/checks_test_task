from checks_test_task.models import Payment, Check
from checks_test_task.schemas.check import PaymentSchema
from checks_test_task.services.base import BaseService


class PaymentService(BaseService[Payment]):
    MODEL = Payment

    async def create_payment(self, payment: PaymentSchema, check: Check, commit: bool = True) -> Payment:
        payment_obj = Payment(
            payment_type=payment.payment_type,
            amount=payment.amount,
            check=check,  # type: ignore
        )
        await self.insert_obj(payment_obj, commit=commit)
        return payment_obj
