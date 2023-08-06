import pandas as pd
from ..data_processing.data_processing_main import data_processing_main
import pkgutil
import csv
def input_dataset(flag=0):
    if flag==0:
        data_bytes = pkgutil.get_data(__package__, 'dataset.csv')

        data_csv = csv.reader(data_bytes.decode().splitlines(), delimiter=',')
        lines=list(data_csv)
        header,values=lines[0],lines[1:]
        data_dic={h:v for h,v in zip(header,zip(*values))}

        data=pd.DataFrame(data_dic)
        data=data.reset_index(drop=True)
        # data=data.drop("",axis=1)
        # data = pd.read_csv(r"./flx_data/dataset.csv")
    elif flag==1:
        # data = pd.read_csv(r"./flx_data/dataset_process.csv")

        data_bytes = pkgutil.get_data(__package__, 'dataset_process.csv')

        data_csv = csv.reader(data_bytes.decode().splitlines(), delimiter=',')
        lines=list(data_csv)
        header,values=lines[0],lines[1:]
        data_dic={h:v for h,v in zip(header,zip(*values))}
        data=pd.DataFrame(data_dic)
    elif flag==2:
        # file = './flx_data/FLX_CN-Ha2_FLUXNET2015_FULLSET_DD_2003-2005_1-4.csv'

        data_bytes = pkgutil.get_data(__package__, 'FLX_CN-Ha2_FLUXNET2015_FULLSET_DD_2003-2005_1-4.csv')

        data_csv = csv.reader(data_bytes.decode().splitlines(), delimiter=',')
        lines=list(data_csv)
        header,values=lines[0],lines[1:]
        data_dic={h:v for h,v in zip(header,zip(*values))}
        data=pd.DataFrame(data_dic)

        d = data_processing_main(data=data,
                                 time_add=1,
                                 lag_add=1,
                                 elim_SM_nan=1,
                                 drop_ir=1,
                                 drop_nan_feature=1,
                                 part=0.7,
                                 n_estimator=10,
                                 sbs=True)
        data, ss = d.total()
    return data



