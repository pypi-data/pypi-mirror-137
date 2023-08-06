# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pwmled', 'pwmled.driver', 'pwmled.led', 'pwmled.transitions']

package_data = \
{'': ['*']}

install_requires = \
['adafruit-blinka>=5.5.1,<7.0',
 'adafruit-circuitpython-pca9685>=3.3.2,<4.0',
 'pigpio>=1.78,<2.0',
 'python-singleton>=0.1.2,<1.0']

setup_kwargs = {
    'name': 'pwmled',
    'version': '1.6.9',
    'description': 'Control LEDs connected to a micro controller using pwm.',
    'long_description': "# python-pwmled [![PyPI version](https://badge.fury.io/py/pwmled.svg)](https://badge.fury.io/py/pwmled)\n\n`python-pwmled` controls LEDs connected to a micro controller using pulse-width modulation. It supports one-color, RGB and RGBW leds driven by GPIOs of an Raspberry Pi or a PCA9685 controller.\n\n# Installation\n`python-pwmled` requires Python 3. It can be installed using pip:\n```bash\npip install pwmled\n```\n\nWhen directly controlling the GPIOs of a Raspberry Pi using the `GpioDriver`(see [below](#configuration)), the [pigpio C library](https://github.com/joan2937/pigpio) is required. It can be installed with the following commands:\n```bash\nwget abyz.co.uk/rpi/pigpio/pigpio.zip\nunzip pigpio.zip\ncd PIGPIO\nmake\nsudo make install\n```\nBesides the library, the `pigpiod` utility is installed, which starts `pigpio` as daemon. The daemon must be running when using the `GpioDriver`.\n```bash\nsudo pigpiod\n```\n\n# Usage\n### Configuration\n`python-pwmled` supports several possibilities for connecting LEDs to your micro controller:\n- GPIO: LEDs can be connected directly to the GPIOs of a Raspberry Pi.\n- PCA9885: A [PCA9685](https://cdn-shop.adafruit.com/datasheets/PCA9685.pdf) can be used as I2C-bus PWM controller.\n\n```python\nfrom pwmled.driver.gpio import GpioDriver\nfrom pwmled.driver.pca9685 import Pca9685Driver\n\n# GPIO driver, which controls pins 17, 22, 23\ndriver = GpioDriver([17, 22, 23])\ndriver = GpioDriver([17, 22, 23], freq=200)\n# To control the pigpio on a other machine use the host and port parameter\ndriver = GpioDriver([17, 22, 23], host='other.host', port=8889)\n\n# PCA9685 driver which controls pins 1, 2, 3\ndriver = Pca9685Driver([1, 2, 3])\ndriver = Pca9685Driver([1, 2, 3], freq=200, address=0x40)\n```\n\n### Control\nEach LED needs a separated driver, which controls the corresponding pins. The number and order of pins depends on the led type:\n- One-color: 1 pin\n- RGB: 3 pins (`[R, G, B]`)\n- RGBW: 4 pins (`[R, G, B, W]`)\n\nThe supported operations are shown in the following example:\n\n```python\nfrom pwmled import Color\nfrom pwmled.led import SimpleLed\nfrom pwmled.led.rgb import RgbLed\nfrom pwmled.led.rgbw import RgbwLed\nfrom pwmled.driver.gpio import GpioDriver\n\n# One-color led\ndriver = GpioDriver([C])\nled = SimpleLed(driver)\nled.on()\nled.brightness = 0.5\nled.transition(5, brightness=0)\nled.off()\n\n# RGB led\ndriver = GpioDriver([R, G, B])\nled = RgbLed(driver)\nled.on()\nled.color = Color(255, 0, 0)\nled.set(color=Color(0, 255, 0), brightness=0.5) # set two properties simultaneously\nled.transition(5, color=Color(0, 0, 255), brightness=1)\nled.off()\n\n# RGBW led\ndriver = GpioDriver([R, G, B, W])\nled = RgbwLed(driver)\n# RgbwLed has same interface as RgbLed\n```\n\n# Contributions\nPull-requests are welcome, especially for adding new drivers or led types.\n\n# License\nThis library is provided under [MIT license](https://raw.githubusercontent.com/soldag/python-pwmled/master/LICENSE.md).\n",
    'author': 'soldag',
    'author_email': 'soren.oldag@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/soldag/python-pwmled',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
