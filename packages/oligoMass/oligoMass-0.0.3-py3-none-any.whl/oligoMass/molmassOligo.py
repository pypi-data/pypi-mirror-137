import molmass as mm
import pandas as pd

import oligoMass.dna as dna
import oligoMass.exModifications as exMod

class oligoModifications():
    def __init__(self):
        self.modRead = False
        self.mod_formula = None
        self.mod_list = None

    def _add_mod(self, letter):
        pass

class oligoNAModifications(oligoModifications):
    def __init__(self):
        super().__init__()

        self.__set_modifications()
        self.exModDB = exMod.exModifDataFrame()

    def __set_modifications(self):
        self.mod_alphabet = '+ * m r'.split(' ')
        self.br_alphabet = '/ [ ] { }'.split(' ')
        self.ex_mod = {}
        self.ex_mod_key = ''
        self.last_mod = ''

        self.mod_formula = {}
        self.mod_formula['+'] = ['CO', '']
        self.mod_formula['*'] = ['S', 'O']
        self.mod_formula['m'] = ['OCH2', '']
        self.mod_formula['r'] = ['O', '']

        self.mod_list = {}
        for k in self.mod_formula.keys():
            self.mod_list[k] = 0

    def reset_modif(self, df):
        #add prefix modifications
        self.mod_list, self.ex_mod = {}, {}
        for m in df[df['prefix'] != '']['prefix']:
            if m in self.mod_alphabet:
                if m in list(self.mod_list.keys()):
                    self.mod_list[m] += 1
                else:
                    self.mod_list[m] = 1
            else:
                m = m[1:-1]
                if m in list(self.ex_mod.keys()):
                    self.ex_mod[m] += 1
                else:
                    self.ex_mod[m] = 1
        # add suffix modifications
        for m in df[df['suffix'] != '']['suffix']:
            if m in list(self.mod_list.keys()):
                self.mod_list[m] += 1
            else:
                self.mod_list[m] = 1


    def _add_mod(self, letter):
        if not self.modRead:
            if letter in self.mod_alphabet:
                self.modRead = False
                self.mod_list[letter] += 1
                self.last_mod = letter

            elif letter in self.br_alphabet:
                self.modRead = True
                self.ex_mod_key = ''
        else:
            if letter in self.br_alphabet:
                self.modRead = False
                if self.ex_mod_key in list(self.ex_mod.keys()):
                    self.ex_mod[self.ex_mod_key] += 1
                else:
                    self.ex_mod[self.ex_mod_key] = 1
                self.last_mod = f'[{self.ex_mod_key}]'
            else:
                self.ex_mod_key += letter


    def _get_mod_formula(self, formula):
        f_mod, f_ = '', ''
        for k in self.mod_list.keys():
            if self.mod_list[k] > 0:
                f_mod += f'({self.mod_formula[k][0]}){self.mod_list[k]}'
                if self.mod_formula[k][1] != '':
                    f_ += f'({self.mod_formula[k][1]}){self.mod_list[k]}'
        if len(list(self.ex_mod)) > 0:
            for key in self.ex_mod.keys():
                mass = int(round(self.ex_mod[key]*self.exModDB.get_mod_properties(key)['mass'], 0))
                if mass > 0:
                    delta = int(round(0.007941*mass, 0))
                    f_mod += f'(H){mass - delta}'
                    #print(f_mod, mass, delta, 0.007941*mass)
        if f_ != '':
            return (mm.Formula(formula) + mm.Formula(f_mod) - mm.Formula(f_)).empirical
        else:
            return (mm.Formula(formula) + mm.Formula(f_mod)).empirical

class oligoSequence():
    def __init__(self, sequence):
        self.init_seq = sequence
        self.sequence = sequence
        self.seq = None
        self.alphabet = None

    def sequence_parser(self):
        return self.init_seq

    def size(self):
        if self.seq != None:
            return len(self.seq)

class oligoNASequence(oligoSequence):
    def __init__(self, sequence):
        super().__init__(sequence)
        self.is_mixed = False
        self.alphabet = 'A G C T U a g c t u R Y M K ' \
                        'S W H B V D N'.split(' ')
        self.mixed_alphabet = 'R Y M K ' \
                        'S W H B V D N'.split(' ')

        self.modifications = oligoNAModifications()
        self.sequence_parser()

        self.dnaDB = dna.deoxynusleosideDB()

    def set_mixed_na(self):
        self.mixed_na = {}
        self.mixed_na['R'], self.mixed_na['Y'] = ['A', 'G'], ['C', 'T']
        self.mixed_na['M'], self.mixed_na['K'] = ['A', 'C'], ['G', 'T']
        self.mixed_na['S'], self.mixed_na['W'] = ['C', 'G'], ['A', 'T']
        self.mixed_na['H'], self.mixed_na['B'] = ['A', 'C', 'T'], ['C', 'G', 'T']
        self.mixed_na['V'], self.mixed_na['D'] = ['A', 'C', 'G'], ['A', 'G', 'T']
        self.mixed_na['N'] = ['A', 'C', 'T', 'G']

    def __getSeqFromTab(self):
        seq = ''
        if not self._seqtab.empty:
            for p in self._seqtab.values:
                seq += p[0]
                seq += p[1]
                seq += p[2]
        return seq

    def sequence_parser(self):
        self._seqtab = {'prefix': [],
                        'nt': [],
                        'suffix': [],
                        'index': []}
        seq_list = list(self.init_seq)
        self.seq = ''
        index = 1
        for letter in seq_list:
            if letter in self.alphabet and not self.modifications.modRead:
                if letter in self.mixed_alphabet:
                    self.is_mixed = True
                self.seq += letter.upper()
                self._seqtab['nt'].append(self.seq[-1])
                self._seqtab['suffix'].append('')
                self._seqtab['prefix'].append(self.modifications.last_mod)
                self._seqtab['index'].append(index)
                self.modifications.last_mod = ''
                index += 1
            else:
                self.modifications._add_mod(letter)
                if self.modifications.last_mod in ['*']:
                    self._seqtab['suffix'][-1] = self.modifications.last_mod
                    self.modifications.last_mod = ''

        self._seqtab = pd.DataFrame(self._seqtab)
        self._seqtab.set_index('index', inplace=True)
        self.sequence = self.__getSeqFromTab()

        self.modifications.reset_modif(self._seqtab)
        return self.sequence

    def __call__(self):
        return self.sequence

    def getPrefix(self, index):
        seq = ''
        if index < self._seqtab.shape[0]:
            for i in range(1, index + 1):
                seq += self._seqtab['prefix'].loc[i] + self._seqtab['nt'].loc[i] + self._seqtab['suffix'].loc[i]
        return oligoNASequence(seq)

    def getSuffix(self, index):
        seq = ''
        if index < self._seqtab.shape[0]:
            for i in range(index + 1, self._seqtab.shape[0] + 1):
                seq += self._seqtab['prefix'].loc[i] + self._seqtab['nt'].loc[i] + self._seqtab['suffix'].loc[i]
        return oligoNASequence(seq)

    def reset_modifications(self):
        self.modifications.reset_modif(self._seqtab)

    def getMolecularFormula(self):
        f = ''
        if not self.is_mixed:
            for n in self.seq:
                f += self.dnaDB(n).seqformula
            if len(self.seq) > 1:
                f += f'(HPO2){len(self.seq) - 1}H2'
            return self.modifications._get_mod_formula(f)
        else:
            return f

    def getMonoMass(self):
        if not self.is_mixed:
            return mm.Formula(self.getMolecularFormula()).isotope
        else:
            return 0

    def getAvgMass(self):
        if not self.is_mixed:
            return mm.Formula(self.getMolecularFormula()).mass
        else:
            return 0


def test():
    olig1 = oligoNASequence('+a+c*grT*mTTuUrurU')
    print(olig1.seq)
    print(olig1.modifications.mod_list)
    print(olig1.getMolecularFormula())
    print(olig1.getAvgMass())

    sequence = '+A*AAUut+tcrgmG*'

    olig2 = oligoNASequence(sequence)
    print(olig2.seq)
    print(olig2.modifications.mod_list)
    print(olig2.getMolecularFormula())
    #print(olig2.getMonoMass())
    print(olig2.getAvgMass())

    seq = dna.oligoSeq(sequence)
    print(seq.getBruttoFormula())
    print(seq.getMolMass())

    print(seq.getMolMass() - olig2.getAvgMass())

    o1 = oligoNASequence('GTA/iFluorT/G')
    print(o1.getMolecularFormula())
    print(o1.getAvgMass())
    print(o1.modifications.ex_mod)

    o2 = oligoNASequence('GTAG')
    print(o2.getMolecularFormula())
    print(o2.getAvgMass())
    print(o2.modifications.ex_mod)

    print(o1.getAvgMass() - o2.getAvgMass())

def test2():
    o1 = oligoNASequence('+G*TrCmA+TTTGGG{iFluorT}CC*++AA*')

    print(o1._seqtab)
    print(o1.sequence)
    print(o1.init_seq)
    print(o1.seq)

    print(o1.getAvgMass())
    print(o1.modifications.mod_list)
    o1.reset_modifications()
    print(o1.modifications.mod_list)
    print(o1.getAvgMass())

def test3():
    o1 = oligoNASequence('AG+TrCATTT/iFluorT/GGGC')
    print(o1())
    for i in range(1, o1.size()):
        p = o1.getPrefix(i)
        s = o1.getSuffix(i)
        print(p(), s(), p.getAvgMass(), s.getAvgMass())




if __name__ == '__main__':
    test3()