from django.dispatch import Signal


log_signal = Signal(providing_args=['requests', 'state'])
