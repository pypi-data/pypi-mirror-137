__all__ = ['mealInfo', 'schoolInfo', 'schoolschedule']

from .mealInfo import get_meal_data
from .schoolInfo import get_school_data
from .schoolschedule import get_schedule_data


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
    def __init__(self, school_info, key=None):
        self.school_info = school_info
        self._key = key

    @classmethod
    def find(cls, region_code, school_code, key=None):
        """
        지역코드와 학교코드로 학교를 찾고 School객체를 리합니다.
        :param region_code: 지역코드
        :param school_code: 학교코드
        :param key: API 인증키
        :return: class School
        """
        school_data = get_school_data(region_code=region_code,
                                      school_code=school_code,
                                      key=key)[0]
        return School(school_data)

    def __str__(self):
        """
        :return: 학교명
        """
        return self.school_info.school_name

    def get_meal_info(self, meal_code=None, date=None, start_date=None, end_date=None, key=None,
                      pindex: int = 1, psize: int = 100):
        """
        신청주소: https://open.neis.go.kr/hub/mealServiceDietInfo
        신청제한횟수: 제한없음
        :param meal_code:식사코드
        :param date:급식일자
        :param start_date:급식시작일자
        :param end_date: 급식종료일자
        :param key: API 인증키
        :param pindex:페이지 위치
        :param psize:페이지 당 신청 숫자
        :return:검색된 모든 급식
        """

        key = self._key if self._key is not None else key

        return get_meal_data(
            region_code=self.school_info.region_code,
            school_code=self.school_info.school_code,
            meal_code=meal_code,
            date=date,
            start_date=start_date,
            end_date=end_date,
            key=key,
            pindex=pindex,
            psize=psize
        )

    def get_school_info(self):
        return self.school_info

    def get_schedule_info(self, dght_crse_sc_nm=None, schul_crse_sc_nm=None, date=None, start_date=None, end_date=None,
                          key=None,
                          pindex: int = 1, psize: int = 100):
        """
        신청주소: https://open.neis.go.kr/hub/SchoolSchedule
        신청제한횟수: 제한없음
        :param dght_crse_sc_nm: 주야과정명
        :param schul_crse_sc_nm: 학교과정명
        :param date: 학사일자
        :param start_date: 학사시작일자
        :param end_date: 학사종료일자
        :param key: API 인증키
        :param pindex: 페이지 위치
        :param psize: 페이지 당 신청 숫자 (필수)
        :return: 검색된 모든 학교 (필수)
        """

        key = self._key if self._key is not None else key

        return get_schedule_data(
            region_code=self.school_info.region_code,
            school_code=self.school_info.school_code,
            dght_crse_sc_nm=dght_crse_sc_nm,
            schul_crse_sc_nm=schul_crse_sc_nm,
            date=date,
            start_date=start_date,
            end_date=end_date,
            key=key,
            pindex=pindex,
            psize=psize
        )
