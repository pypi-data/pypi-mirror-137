# krx-hj3415

krx-hj3415는 https://kind.krx.co.kr 에서 종목에 대한 정보를 받아서 데이터베이스에 저장한다.(krx.db)

## Installation

[pip](https://pip.pypa.io/en/stable/) 를 사용하여 설치한다.

```bash
pip install krx-hj3415
```

## Usage

```python
from krx_hj3415 import krx

MIN_REFRESH_DAY = 10

# krx 데이터베이스를 refresh 한다.
krx.make_db()

# 데이터베이스가 MIN_REFRESH_DAY 보다 오래되었는지 확인한다.
krx.is_old_krx()

# 전체 코드를 리스트로 반환한다.
krx.get_codes()

# 전체 코드를 키로하고 종목명을 값으로 하는 딕셔너리를 반환한다.
krx.get_name_codes()

# 삼성전자를 반환한다.
krx.get_name(code='005930')

# 전체 종목코드의 1/10을 날짜베이스로 반환한다.(dart 에서 사용한다.)
krx.get_parts()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)