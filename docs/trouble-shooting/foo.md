
```sh
    @staticmethod
    def _default_pin_factory():
        # We prefer lgpio here as it supports PWM, and all Pi revisions without
        # banging on registers directly.  If no third-party libraries are
        # available, however, we fall back to a pure Python implementation
        # which supports platforms like PyPy
        #
        # NOTE: If the built-in pin factories are expanded, the dict must be
        # updated along with the entry-points in setup.py.
        default_factories = {
            'lgpio':   'gpiozero.pins.lgpio:LGPIOFactory',
            'rpigpio': 'gpiozero.pins.rpigpio:RPiGPIOFactory',
            'pigpio':  'gpiozero.pins.pigpio:PiGPIOFactory',
            'native':  'gpiozero.pins.native:NativeFactory',
        }
        name = os.environ.get('GPIOZERO_PIN_FACTORY')
        if name is None:
            # If no factory is explicitly specified, try various names in
            # "preferred" order
            for name, entry_point in default_factories.items():
                try:
                    mod_name, cls_name = entry_point.split(':', 1)
                    module = __import__(mod_name, fromlist=(cls_name,))
                    pin_factory = getattr(module, cls_name)()
                    if name == 'native':
                        warnings.warn(NativePinFactoryFallback(native_fallback_message))
                    return pin_factory
                except Exception as e:
                    warnings.warn(
                        PinFactoryFallback(f'Falling back from {name}: {e!s}'))
>           raise BadPinFactory('Unable to load any default pin factory!')
E           gpiozero.exc.BadPinFactory: Unable to load any default pin factory!

.venv/lib/python3.11/site-packages/gpiozero/devices.py:302: BadPinFactory
----------------------------- Captured stdout call -----------------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Can't connect to pigpio at localhost(8888)

Did you start the pigpio daemon? E.g. sudo pigpiod

Did you specify the correct Pi host/port in the environment
variables PIGPIO_ADDR/PIGPIO_PORT?
E.g. export PIGPIO_ADDR=soft, export PIGPIO_PORT=8888

Did you specify the correct Pi host/port in the
pigpio.pi() function? E.g. pigpio.pi('soft', 8888)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
=============================== warnings summary ===============================

```