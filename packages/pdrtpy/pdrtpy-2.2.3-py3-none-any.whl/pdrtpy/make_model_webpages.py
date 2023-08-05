from pdrtpy.modelset import ModelSet
from pdrtpy.plot.modelplot import ModelPlot
import os

class Page():

    def make_page(self):
        success = True
        # check all models.tab files and existence of all therein
        t = ModelSet.all_sets()
        failed = list()
        for n,z,md,m in zip(list(t["name"]),list(t["z"]),list(t["medium"]),list(t["mass"])):
            print(n,z,md,m)
            ms = ModelSet(name=n,z=z,medium=md,mass=m)
            mp = ModelPlot(ms)
            print(f'Making page for {n,z,md,m}')
            if m is not None:
                dir = f'{n}_{z}_{md}_{m}'
            else:
                dir = f'{n}_{z}'
            print(dir)
            for r in ms.table["ratio"]:
                try:
                    model = ms.get_model(r)
                    #mp.plot(r)
                except Exception as e:
                    success = False
                    failed.append(str(e))
            if not success:
                print("Couldn't open these models:",failed)

if __name__ == '__main__':
    p = Page()
    p.make_page()
