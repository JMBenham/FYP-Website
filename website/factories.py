import factory, factory.django
from . import models


hardwareNames = ['BBC Micro:Bit', 'Sphero', 'Modkit', 'Cubelets', 'LittleBits', 'Bee-bots']


class hardwareFactory(factory.Factory):
    """
    Hardware factory

    Create hardware objects with the names in hardwareNames list
    """
    class Meta:
        model = models.Hardware

    name = factory.Iterator(hardwareNames)