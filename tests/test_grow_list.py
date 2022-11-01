from osdatahub.grow_list import GrowList


class TestGrowList:

    def test_extend(self):
        # Arrange
        gl = GrowList([1, 2, 3])

        # Act
        gl.extend([4, 5, 6])

        # Assert
        assert gl.values == [1, 2, 3, 4, 5, 6]

    def test_grown_true(self):
        # Arrange
        gl = GrowList([1, 2, 3])

        # Act
        gl.extend([4, 5, 6])

        # Assert
        assert gl.grown

    def test_grown_true_init(self):
        # Arrange
        gl = GrowList([1, 2, 3])

        # Assert
        assert gl.grown

    def test_grown_false(self):
        # Arrange
        gl = GrowList([1, 2, 3])
        gl.extend([])

        # Assert
        assert not gl.grown
