from hbutils.model import hasheq, asitems, get_repr_info


@hasheq()
@asitems(['package', 'clazz', 'filename'])
class JavaEntry:
    """
    Entry model of java source code.
    """

    def __init__(self, filename, package, clazz):
        """
        Constructor of :class:`jentry.model.entry.JavaEntry`.

        :param filename: Source code file name.
        :param package: Package name, ``None`` means the top package.
        :param clazz: Class name.
        """
        self.__filename = filename if filename else None
        self.__package = package if package else None
        self.__clazz = clazz

    @property
    def filename(self):
        """
        Source code file name
        """
        return self.__filename

    @property
    def package(self):
        """
        Package name, ``None`` means the top package.
        """
        return self.__package

    @property
    def clazz(self):
        """
        Class name.
        """
        return self.__clazz

    @property
    def full_name(self):
        """
        Full entry name.
        """
        if self.__package:
            return f'{self.__package}.{self.__clazz}'
        else:
            return f'{self.__clazz}'

    def __str__(self):
        """
        Formatted string.

        :return: Formatted string, the same as ``full_name``.
        """
        return self.full_name

    def __repr__(self):
        """
        Representation string.

        :return: Representation string.
        """
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('class', lambda: self.full_name),
                ('filename', lambda: repr(self.filename), lambda: self.filename),
            ]
        )
