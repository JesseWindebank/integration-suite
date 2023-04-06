from extract.endpoints import extract_intacct_base
from transform.endpoints import transform_intacct_base
from load.endpoints import load_twocloudnine_acc_segments


def main():

    # intacct - departments > twocloudnine - acc_segments
    extract_intacct_base.extract_departments()
    transform_intacct_base.transform_departments()
    load_twocloudnine_acc_segments.load_departments()


if __name__ == "__main__":
    main()
