import serial
import threading
import time
import struct
import math

class NeoSpider:
    """
    네오스파이더 로봇 라이브러리
    """

    def __init__(self):
        self._is_start = False
        self._tone_table = {
            '도': 0,
            '도#': 1,
            '레': 2,
            '레#': 3,
            '미': 4,
            '파': 5,
            '파#': 6,
            '솔': 7,
            '솔#': 8,
            '라': 9,
            '라#': 10,
            '시': 11,
        }
        self._tone_map = {
            0: [33, 65, 131, 262, 523, 1046, 2093, 4186],
            1: [35, 69, 139, 277, 554, 1109, 2217, 4435],
            2: [37, 73, 147, 294, 587, 1175, 2349, 4699],
            3: [39, 78, 156, 310, 622, 1245, 2489, 4978],
            4: [41, 82, 165, 330, 659, 1319, 2637, 5274],
            5: [44, 87, 175, 349, 698, 1397, 2794, 5588],
            6: [46, 92, 185, 370, 740, 1480, 2960, 5920],
            7: [49, 98, 196, 392, 784, 1568, 3136, 6272],
            8: [52, 104, 208, 415, 831, 1661, 3322, 6645],
            9: [55, 110, 220, 440, 880, 1760, 3520, 7040],
            10: [58, 117, 233, 466, 932, 1865, 3729, 7459],
            11: [62, 123, 247, 494, 988, 1976, 3951, 7902],
        }
        self.__data_list = [[0] * 1 for _ in range(36)]
        self.__data_list[0][0] = 255
        self.__data_list[1][0] = 36
        self.__data_list[-1][0] = 10
        self.__gas_value = 0
        self.__cds_value = 0
        self.__temp_value = 0
        self.__vibe_value = 0
        self.__left_inf_value = 0
        self.__right_inf_value = 0
        self.__motion_value = 0
        self.__ultrasonic_value = 0

    def connect(self, comport: str, baudrate: int=115200):
        """
        : Comport 연결
        @params: comport -> str, baudrate=115200 -> int
        comport: ex) COM3
        baudrate: 보드레이트 설정. default=115200
        ex) connect('COM3') -> Comport3번과 연결
        """
        self._is_start = True
        self.comport = comport
        self.__ser = serial.Serial(comport, baudrate=baudrate)
        self.__ser.flushOutput()
        self.__ser.flushInput()
        self.__read_thread()
        print("{}에 {}속도로 연결되었습니다.".format(comport, baudrate))
    
    def move(self, direct: int):
        """
        : 네오스파이더 이동
        @params: direct -> int
        0: Stop, 정지
        1: Front, 앞으로
        2: Left, 왼쪽으로
        3: Right, 오른쪽으로
        4: Backward, 뒤로
        ex) move(1) -> 앞으로
        """
        direct = int(direct) if 0 < direct < 5 else 0
        self.__data_list[6][0] = direct
        self.__write_data()

    def stop(self):
        """
        : 네오스파이더 정지
        """
        self.__data_list[6][0] = 0
        self.__write_data()

    def tone(self, octave: int, note: str, duration: float):
        """
        : 음계 소리내기
        @params: octave -> int, note -> str, duration -> float
        octave: 옥타브
        note: 음계
        duration: 시간/s
        ex) tone(3, '도', 0.3) -> 3옥타브 도로 0.3초 연주
        """
        note_index = 0
        if isinstance(note, str):
            note_index = self._tone_table[note]
        elif isinstance(note, int):
            note_index = note if 0 <= note < 12 else 0

        octave = octave if 0 <= octave < 8 else 0
        duration = duration if duration > 0 else 0

        notes = self._tone_map[note_index][octave]
        self.__data_list[2][0] = notes >> 8
        self.__data_list[3][0] = notes & 255
        self.__write_data()
        time.sleep(duration)
        self.__data_list[2][0] = 0
        self.__data_list[3][0] = 0
        self.__write_data()

    def num_rgb_led(self, num: int, r: int=0, g: int=0, b: int=0):
        """
        : 선택 모듈 RGB LED 제어
        @params: num -> int, r=0 -> int, g=0 -> int, b=0 -> int
        num: 0~7 모듈 RGB LED 선택
        r: 0~255 빨강 (defulat=0)
        g: 0~255 초록 (defulat=0)
        b: 0~255 파랑 (defulat=0)
        """
        if 0 <= num < 8:
            num = int(num)
            self.__data_list[8 + 3 * num + 0][0] = r & 255
            self.__data_list[8 + 3 * num + 1][0] = g & 255
            self.__data_list[8 + 3 * num + 2][0] = b & 255
            self.__write_data()

    def all_rgb_led(self, r: int=0, g: int=0, b: int=0):
        """
        : 모든 모듈 RGB LED 제어
        @params: r=0 -> int, g=0 -> int, b=0 -> int
        r: 0~255 빨강 (defulat=0)
        g: 0~255 초록 (defulat=0)
        b: 0~255 파랑 (defulat=0)
        """
        for num in range(8):
            self.__data_list[8 + 3 * num + 0][0] = r & 255
            self.__data_list[8 + 3 * num + 1][0] = g & 255
            self.__data_list[8 + 3 * num + 2][0] = b & 255
        self.__write_data()

    def all_rgb_led_off(self):
        """
        : 모든 모듈 RGB LED OFF
        """
        for num in range(8):
            self.__data_list[8 + 3 * num + 0][0] = 0
            self.__data_list[8 + 3 * num + 1][0] = 0
            self.__data_list[8 + 3 * num + 2][0] = 0
        self.__write_data()

    def output_motor(self, d5: int=0, d6: int=0):
        """
        : 외부모터 제어 모듈
        @params: d5=0 -> int, d6=0 -> int
        d5: 디지털 5번 핀 PWM 0~255 (default=0)
        d6: 디지털 6번 핀 PWM 0~255 (default=0)
        """
        self.__data_list[-4][0] = d5 & 255
        self.__data_list[-3][0] = d6 & 255
        self.__write_data()

    def head_angle(self, angle: int=90):
        """
        : 고개 각도 설정
        @params: angle=90 -> int
        angle: 고개 각도 50~130 (default=90)
        """
        angle = max(angle, 50)
        angle = min(angle, 130)
        self.__data_list[7] = angle
        self.__write_data()

    def __check_sum(self, check_list):
        """
        : 데이터 검증[private]
        @params: check_list -> list
        check_list: 검증할 2차원 리스트 데이터
        """
        sum_value = 0
        for idx in range(2, len(check_list)-2):
            sum_value += check_list[idx][0]
        return sum_value & 255

    def __write_data(self):
        """
        : 데이터 송신[private]
        """
        if self.__ser:
            self.__data_list[-2][0] = self.__check_sum(self.__data_list)
            for data in self.__data_list:
                self.__ser.write(bytes(data))
            time.sleep(0.05) # 통신의 안전을 위해 추가
        else:
            print("연결이 되지 않았습니다.\n포트를 다시 확인해주세요.")

    def __init_data(self):
        """
        : 데이터 초기화[private]
        """
        self.__data_list = [[0] * 1 for _ in range(36)]
        self.__data_list[0][0] = 255
        self.__data_list[1][0] = 36
        self.__data_list[-1][0] = 10
        self.__write_data()

    def __read_data(self):
        """
        : 데이터 수신 - 상시 수신[private]
        """
        if self.__ser:
            while self._is_start:
                data_list = [[_] for _ in list(self.__ser.readline())]
                if len(data_list) >= 10:
                    if data_list[-1][0] == 10 and data_list[-2][0] == 13 and data_list[0][0] == 255 and data_list[1][0] == 16:
                        data_list = data_list[2:-2]
                        if data_list[0][0] == 1: # ANALOG
                            if len(data_list) == 12:
                                self.__gas_value = (data_list[1][0] << 8) + (data_list[2][0] & 255)
                                self.__cds_value = (data_list[3][0] << 8) + (data_list[4][0] & 255)
                                temp_value = (data_list[5][0] << 8) + (data_list[6][0] & 255)
                                temp_value = math.log((10240000 / temp_value) - 10000)
                                temp_value = 1 / (0.001129148 + (0.000234125 * temp_value) + (0.0000000876741 * temp_value * temp_value * temp_value))
                                self.__temp_value = round(temp_value - 273.15 - 4.0, 2) # Downsize temperature
                                self.__vibe_value = (data_list[7][0] << 8) + (data_list[8][0] & 255)
                                self.__left_inf_value = data_list[9][0]
                                self.__right_inf_value = data_list[10][0]

                        elif data_list[0][0] == 2: # ULTRASONIC
                            if len(data_list) == 6:
                                int_bits = data_list[4][0] << 24 | data_list[3][0] << 16 | data_list[2][0] << 8 | data_list[1][0]
                                pack_bits = struct.pack('>l', int_bits)
                                self.__ultrasonic_value = struct.unpack('>f', pack_bits)[0]
                        elif data_list[0][0] == 3: # MOTION
                            if len(data_list) == 6:
                                int_bits = data_list[4][0] << 24 | data_list[3][0] << 16 | data_list[2][0] << 8 | data_list[1][0]
                                pack_bits = struct.pack('>l', int_bits)
                                self.__motion_value = False if struct.unpack('>f', pack_bits)[0] == 0 else True

    def __read_thread(self):
        """
        : 데이터 수신 - Thread Daemon[private]
        """
        _read_thread = threading.Thread(target=self.__read_data, daemon=True)
        _read_thread.start()

    def get_gas_sensor(self):
        """
        : 가스 센서값 가져오기
        @return __gas_value
        """
        # print(self.__gas_value)
        return self.__gas_value

    def get_cds_sensor(self):
        """
        : 조도(CDS) 센서값 가져오기
        @return __cds_value
        """
        # print(self.__cds_value)
        return self.__cds_value

    def get_temp_sensor(self):
        """
        : 온도 센서값 가져오기
        @return __temp_value
        """
        # print(self.__temp_value)
        return self.__temp_value

    def get_vibe_sensor(self):
        """
        : 진동 센서값 가져오기
        @return __vibe_value
        """
        # print(self.__vibe_value)
        return self.__vibe_value

    def get_input_sensor(self):
        """
        : 외부 센서값 가져오기
        @return __gas_value
        """
        # print(self.__gas_value)
        return self.__gas_value

    def get_left_infared(self):
        """
        : 왼쪽 적외선 센서값 가져오기
        @return __left_inf_value
        """
        # print(self.__left_inf_value)
        return self.__left_inf_value

    def get_right_infared(self):
        """
        : 오른쪽 적외선 센서값 가져오기
        @return __right_inf_value
        """
        # print(self.__right_inf_value)
        return self.__right_inf_value

    def get_ultrasonic(self):
        """
        : 초음파 센서 거리값 가져오기
        @return __ultrasonic_value
        """
        self.__data_list[4][0] = 1
        self.__write_data()
        # print(round(self.__ultrasonic_value, 2))
        return round(self.__ultrasonic_value, 2)

    def get_motion(self):
        """
        : 모션 센서값 가져오기
        @return __motion_value
        """
        self.__data_list[5][0] = 1
        self.__write_data()
        # print(self.__motion_value)
        return self.__motion_value
    
    def close(self):
        """
        close(): 연결 닫기
        """
        if self.__ser:
            self._is_start = False
            self.__init_data()
            self.__ser.close()
            self.__ser = None
            print("연결이 해체되었습니다.")
