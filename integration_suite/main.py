from extract.endpoints import extract_sage_intacct
from transform.endpoints import transform_sage_intacct


def main():
    extract_sage_intacct.extract_departments()
    transform_sage_intacct.transform_departments()


if __name__ == "__main__":
    main()
