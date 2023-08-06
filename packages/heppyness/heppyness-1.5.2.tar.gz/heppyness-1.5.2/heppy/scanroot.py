import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

# Generator of all paths to non-directories in the file
# Copied from Andy Buckley, http://pastebin.com/GebcyHY9
def path_generator(d, basepath='/'):
    for key in d.GetListOfKeys():
        kname = key.GetName()
        if key.IsFolder() and 'TDirectory' in key.GetClassName():
            for i in path_generator(d.Get(kname), basepath+kname+'/'):
                yield i
        else:
            yield basepath + kname #, d.Get(kname)



def string_contains_all(string, all):
    for a in all:
        if not a in string:
            return False
    return True



def string_contains_some(string, some):
    if not some:
        return True
    for s in some:
        if s in string:
            return True
    return False



def string_contains_none(string, none):
    for n in none:
        if n in string:
            return False
    return True



# Get list of all histogram paths in a ROOT file that pass filters:
# @param include     list of strings that paths need to contain to be considered
# @param exclude     list of strings that paths may not contain to be considered  
def get_keys(fpath, all=[], some=[], none=[]):
    rootfile = ROOT.TFile(fpath, 'r')
    rootfile.cd()
    paths = []
    for path in path_generator(rootfile):
        if string_contains_all(path, all) and string_contains_some(path, some) and string_contains_none(path, none):
            paths.append(path)
    return paths
