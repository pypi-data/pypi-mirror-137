__all__ = ['mealInfo', 'schoolInfo', 'schoolschedule']

from .mealInfo import get_meal_data
from .schoolInfo import get_school_data
from .schoolschedule import get_schedule_data
from .exceptions import *


class Region:
    """
    SEOUL : B10\n
    BUSAN : C10\n
    DAEGU : D10\n
    INCHEON : E10\n
    GWANGJU : F10\n
    DAEJEON : G10\n
    ULSAN : H10\n
    SEJONG : I10\n
    GYEONGGI : J10\n
    GANGWON : K10\n
    CHUNGBUK : M10\n
    CHUNGNAM : N10\n
    JEONBUK : P10\n
    JEONNAM : Q10\n
    GYEONGBUK : R10\n
    GYEONGNAM : S10\n
    JEJU : T10\n
    FORIENGER : V10\n
    """
    SEOUL = "B10"
    BUSAN = "C10"
    DAEGU = "D10"
    INCHEON = "E10"
    GWANGJU = "F10"
    DAEJEON = "G10"
    ULSAN = "H10"
    SEJONG = "I10"
    GYEONGGI = "J10"
    GANGWON = "K10"
    CHUNGBUK = "M10"
    CHUNGNAM = "N10"
    JEONBUK = "P10"
    JEONNAM = "Q10"
    GYEONGBUK = "R10"
    GYEONGNAM = "S10"
    JEJU = "T10"
    FORIENGER = "V10"


class School:
    def __init__(self, school_info):
        self.school_info = school_info

    @classmethod
    def find(cls, region_code, school_code):
        """
        지역코드와 학교코드로 학교를 찾고 School객체를 리합니다.
        :param region_code: 지역코드
        :param school_code: 학교코드
        :return: class School
        """
        school_data = get_school_data(region_code=region_code,
                                      school_code=school_code)[0]
        return School(school_data)

    def __str__(self):
        """
        :return: 학교명
        """
        return self.school_info.school_name

    def get_meal_info(self, year, month, day):
        return get_meal_data(region_code=self.school_info.region_code,
                             school_code=self.school_info.school_code,
                             date=f"{int(year)}{int(month):02}{int(day):02}")

    def get_school_info(self):
        return self.school_info

    def get_schedule_info(self, year, month, day):
        return get_schedule_data(region_code=self.school_info.region_code,
                                 school_code=self.school_info.school_code,
                                 date=f"{int(year)}{int(month):02}{int(day):02}")
