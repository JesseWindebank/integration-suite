from extract.endpoints import extract_intacct_base
from transform.endpoints import transform_intacct_base
from load.endpoints import load_twocloudnine_payroll


def main():
    extract_intacct_base.extract_departments()
    print('completed department extraction...')

    transform_intacct_base.transform_departments()
    print('completed department transformation...')

    load_twocloudnine_payroll.load_departments()
    print('completed department load...')


if __name__ == "__main__":
    main()
