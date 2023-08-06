import pandas as pd


class exModifDB():
    def __init__(self):
        self.data = None

    def get_mod_properties(self, mod_code):
        pass

class exModifDataFrame(exModifDB):
    def __init__(self):
        super().__init__()

        self.data = {'code': [], 'mass': [], 'ext_cf': [], 'formula+': [], 'formula-': []}

        self.data['code'].append('5Phos')
        self.data['mass'].append(80.)
        self.data['ext_cf'].append(0)
        self.data['formula+'].append('')
        self.data['formula-'].append('')

        self.data['code'].append('iFluorT')
        self.data['mass'].append(816.7)
        self.data['ext_cf'].append(13700)
        self.data['formula+'].append('')
        self.data['formula-'].append('')

        self.data['code'].append('+m')
        self.data['mass'].append(0)
        self.data['ext_cf'].append(0)
        self.data['formula+'].append('C2H2O')
        self.data['formula-'].append('')

        self.data['code'].append('LNA')
        self.data['mass'].append(0)
        self.data['ext_cf'].append(0)
        self.data['formula+'].append('CO')
        self.data['formula-'].append('')

        self.data['code'].append('tio')
        self.data['mass'].append(0)
        self.data['ext_cf'].append(0)
        self.data['formula+'].append('S')
        self.data['formula-'].append('O')

        self.data = pd.DataFrame(self.data)
        self.data = self.data.set_index('code')

        self.data['in_base'] = [True for i in self.data['mass']]

    def get_mod_properties(self, mod_code):
        if mod_code in self.data.index:
            return self.data.loc[mod_code].to_dict()
        else:
            return {'mass': 0, 'formula+': '', 'formula-': '', 'in_base': False}


def test():
    db = exModifDataFrame()
    print(db.data.loc['5Phos'].to_dict())
    print(db.get_mod_properties('5Phos'))

if __name__ == '__main__':
    test()