import pandas as pd

a = pd.read_csv("player.csv") 
b = pd.read_csv("finish.csv")
c = pd.read_csv("jumpers.csv")
d = pd.read_csv("perdef.csv")
e = pd.read_csv("postdef.csv")
f = pd.read_csv("totals.csv")
g = pd.read_csv("types.csv")
#h = pd.read_csv("teams.csv")

end = a
for df in [b, c, d, e, f, g]:
    end = end.merge(df, on="ID")

end.to_csv('out.csv', index = False)
