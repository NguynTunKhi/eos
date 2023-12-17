class AQIDataType:
    ADJUST = 2
    RAW = 3

    def arr(self):
        return [
            self.RAW,
            self.ADJUST,
        ]


class AQIReportLevel:
    LEVEL1 = [0, 50]
    LEVEL2 = [50, 100]
    LEVEL3 = [100, 150]
    LEVEL4 = [150, 200]
    LEVEL5 = [200, 300]
    LEVEL6 = [300]
    RANGE_TEXT_LEVEL1 = "0-50"
    RANGE_TEXT_LEVEL2 = "51-100"
    RANGE_TEXT_LEVEL3 = "101-150"
    RANGE_TEXT_LEVEL4 = "151-200"
    RANGE_TEXT_LEVEL5 = "201-300"
    RANGE_TEXT_LEVEL6 = "300->"

    def arr(self):
        return [
            self.LEVEL1,
            self.LEVEL2,
            self.LEVEL3,
            self.LEVEL4,
            self.LEVEL5,
            self.LEVEL6,
        ]
