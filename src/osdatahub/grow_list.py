class GrowList:
    """
    GrowList is a convenience class that behaves similarly to a normal
    list, except that it stores its length changes whenever it is extended
    with the extend() function.
    """

    def __init__(self, values: list = None):
        self.values = values if values else []
        self.size = [len(self.values)]

    def __bool__(self):
        return bool(self.values)

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return repr(self.values)

    def __iter__(self):
        return iter(self.values)

    @property
    def grown(self):
        """Checks whether the GrowList has been expanded, or whether it has
        been extended with an empty list of values.

        Returns:
            bool: True suggests that the GrowList has recently grown, False
            suggests that it has been extended with an empty list
        """
        if len(self.size) == 1 or self.size[-1] > self.size[-2]:
            return True
        return False

    def __log_size(self):
        self.size.append(len(self.values))

    def extend(self, values: list):
        """Adds values onto the end of the GrowList

        Args:
            values (list): list of values to be added
        """
        self.values.extend(values)
        self.__log_size()
