from enum import Enum

class PaymentMethods(str, Enum):
    CREDIT_CARD = "credit_card"
    PIX = "pix"
    INVOICE = "invoice"