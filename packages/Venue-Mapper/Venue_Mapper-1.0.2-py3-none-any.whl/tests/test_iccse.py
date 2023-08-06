from tests.BaseRunner import BaseRunner


class TestICCSE(BaseRunner):

    def setUp(self):
        self.expected_venue = "ICCSE"

        self.correct_strings = {
            "ICCSE",
            "2016 11th International Conference on Computer Science \& Education (ICCSE)",
            "15th International Conference on Computer Science {\&} Education, {ICCSE} 2020, Delft, The Netherlands, August 18-22, 2020",
        }

        self.wrong_strings = {
        }
