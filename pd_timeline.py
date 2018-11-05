#
# pd dataframe timeline test
# 

import pandas as pd
from twittercomments.models.tinydb.tweet import Tweet

def main():
    t = Tweet()
    res = t.get_all()
    reslist=[x.to_dict() for x in res]
    #print(reslist[0])
    
    df = pd.DataFrame(reslist)
    print(list(df.columns.values))
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    
    print(df.head(50))
    dft = df.resample("5T").count()
    dft1 = dft.truncate(before="2018-11-05")
    dft2 = dft1.between_time("09:10", "13:00")
    print(dft2.head(25))

if __name__=="__main__":
    # 
    main()

