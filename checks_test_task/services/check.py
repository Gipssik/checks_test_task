from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from checks_test_task.conf.constants import ErrorMessages, PaymentType
from checks_test_task.exceptions import ValidationException
from checks_test_task.filters.check import CheckFilter
from checks_test_task.models import Check, Payment
from checks_test_task.schemas.check import CheckCreateSchema
from checks_test_task.services.base import BaseService
from checks_test_task.services.payment import PaymentService
from checks_test_task.services.product import ProductService


class CheckService(BaseService[Check]):
    MODEL = Check

    async def create_check(self, check_data: CheckCreateSchema, user_id: int) -> Check:
        """Create a new check.

        Does not commit the related objects to the database if the payment is not valid.
        """
        product_service = ProductService(self.session)
        payment_service = PaymentService(self.session)

        check_obj = self.MODEL(user_id=user_id)

        products = await product_service.create_products(check_data.products, check_obj, commit=False)
        payment = await payment_service.create_payment(check_data.payment, check_obj, commit=False)

        check_obj.total_price = sum(product.total_price for product in products)
        check_obj.rest = payment.amount - check_obj.total_price

        if check_obj.rest < 0:
            raise ValidationException(ErrorMessages.CHECK_AMOUNT_EXCEEDED)

        await self.insert_obj(check_obj, commit=True)
        await self.session.refresh(check_obj)
        return check_obj

    async def get_checks(self, check_filter: CheckFilter, user_id: int):
        """Get all checks for a user applying the filter and pagination"""

        query = check_filter.filter(
            select(self.MODEL).join(Payment).where(self.MODEL.user_id == user_id).order_by(self.MODEL.id)
        )
        return await paginate(self.session, query)

    async def get_check(self, check_id: int):
        """Get a check by id"""

        return await self.fetch_one(filters=(self.MODEL.id == check_id,), options=(joinedload(self.MODEL.user),))

    async def get_formatted_check(self, check: Check) -> str:
        """Get a formatted string representation of a check.

        Example:
        ```
             ФОП Джонсонюк Борис
        ==============================
        3.00 x 298870.00
        Mavic 3T             896610.00
        ------------------------------
        20.00 x 31000.00
        Дрон FPV з акумулятором 6S
        чорний               620000.00
        ------------------------------
        13.00 x 114.40
        Цукерки від Миколая
                               1487.20
        ==============================
        СУМА                1518097.20
        Готівка             1903001.00
        Решта                384903.80
        ==============================
               18.12.2024 03:05
             Дякуємо за покупку!
        ```
        """

        default_width = 30
        min_spacing = 5
        user_width = len(check.user.name) + 4
        width = max(default_width, user_width)
        check_str = ""

        check_str += f"{check.user.name.center(width)}\n"

        check_str += f"{'=' * width}\n"

        product_strs = []
        for product in check.products:
            product_str = f"{product.quantity:.2f} x {product.price_per_unit:.2f}".ljust(width) + "\n"
            product_name = product.name
            total_price = f"{product.total_price:.2f}"
            product_str += self._get_aligned_strings(product_name, total_price, width, min_spacing) + "\n"
            product_strs.append(product_str)
        check_str += f"{'-' * width}\n".join(product_strs)

        check_str += f"{'=' * width}\n"

        check_str += self._get_aligned_strings("СУМА", f"{check.total_price:.2f}", width, min_spacing) + "\n"
        payment_str = "Картка" if check.payment.payment_type == PaymentType.CASH else "Готівка"
        check_str += self._get_aligned_strings(payment_str, f"{check.payment.amount:.2f}", width, min_spacing) + "\n"
        check_str += self._get_aligned_strings("Решта", f"{check.rest:.2f}", width, min_spacing) + "\n"

        check_str += f"{'=' * width}\n"

        created_at = check.created_at.strftime("%d.%m.%Y %H:%M").center(width)
        check_str += created_at + "\n"
        check_str += "Дякуємо за покупку!".center(width) + "\n"

        return check_str

    @staticmethod
    def _get_aligned_strings(left_str: str, right_str: str, width: int, min_spacing: int) -> str:
        """Get aligned strings, where the `left_str` is aligned to the left and the `right_str` is aligned to the
        right"""

        spacing = max(min_spacing, width - len(left_str) - len(right_str))
        string = f"{left_str}{' ' * spacing}{right_str}"

        # if there's enough space for the string and spacing
        if len(string) == width:
            return string

        # if there's not enough space for the string and spacing, but the left string is shorter than the width
        if len(left_str) <= width:
            string = left_str.ljust(width) + "\n"
            string += right_str.rjust(width)
            return string

        # split the left string by spaces, and the words that are longer than the width
        # will be split into multiple lines
        left_strs = left_str.split()
        index = 0
        while index < len(left_strs):
            current_str = left_strs[index]
            if len(current_str) > width:
                left_strs[index] = current_str[:width]
                left_strs.insert(index + 1, current_str[width:])

            index += 1

        left_str = ""
        for ls in left_strs:
            if len(left_str) + len(ls) > width:
                left_str += "\n"
            elif left_str:
                left_str += " "
            left_str += ls

        # check if there's enough space for the right string and spacing
        last_newline_index = left_str.rfind("\n")
        taken_space = len(left_str) - last_newline_index - 1
        if taken_space + spacing + len(right_str) > width:
            left_str += "\n"
            taken_space = 0

        string = left_str + right_str.rjust(width - taken_space)
        return string
