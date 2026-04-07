from enum import Enum

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    PIX = "pix"
    INVOICE = "boleto"