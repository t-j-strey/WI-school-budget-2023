import pandas as pd

def main():
    df1 = pd.DataFrame({'gen1': [1, 1, 1], 'gen2': [4, 5, 6], 'gen3': [1, 1, 1]})
    print(df1)
    df2 = pd.DataFrame({'gen1': [1, 1, 1], 'gen2': [4, 5, 6], 'gen4': [2, 2, 2]})
    print(df2)
    df3 = pd.DataFrame({'gen1': [1, 1, 1], 'gen2': [4, 5, 6, 7], 'gen5': [3, 3, 3]})
    out = pd.merge(df1,df2,on=['gen1', 'gen2'], how= 'outer')
    print(out)
    out2 = pd.merge(out,df3,on=['gen1','gen2'],how='outer')

    print(out2)
 #this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
    