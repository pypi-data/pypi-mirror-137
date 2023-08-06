import logging
logger = logging.getLogger('smartypes')
from datetime import datetime
import pandas
from dateutil import parser #not used 
from datetime import datetime
import os
import pandas as pd
from openpyxl import load_workbook
import itertools
from math import factorial
import re

import os
from jinja2 import Environment, FileSystemLoader,PackageLoader,ChoiceLoader
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
loader1 = FileSystemLoader(os.path.join(THIS_DIR, '../gen_ext_code/sql'))


TEMPLATE_SQL_CODE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=loader1,
    trim_blocks=True,
    lstrip_blocks=True)


#Learning environment variables 
maxItemCombi=20

def checkStr(xstr,testFloat=False):
    # checck what type are possible for a str input
    #TODO make it with learning for a given field or field group will first test the types in the best order 
    dateformats=['%Y-%m-%d','%d/%m/%Y %H:%M:%S','%d-%m-%Y %H:%M:%S','%d-%m-%Y','%d/%m/%Y']
    if type(xstr) is str :
        if testFloat:
            try :
                xval = float(xstr)
                logger.debug(f'float {xval} ')
                return xval
            except :
                logger.debug(f'not float {xval} ')
        for df in dateformats:
            try :
                xval=datetime.strptime(xstr,df)
                logger.debug(f'date {xval} ')
                return xval
            except :
                logger.debug(f'date format {df} not working')
        return xstr
    else :
        return xstr


def comb(n, k):
    nomin = factorial(n)
    denom = (factorial(k) * (factorial(n - k)))
    if denom > 0:
        return nomin / denom
    else:
        return 0

def all_combi_len(listA):
    n=len(listA)
    c = sum([comb(n,p) for p in range(n)])
    return  c

def all_combi(listA,p=None):
    # create all combination for a list
    if len(listA) == 0 :
        return []
    if len(listA) == 1 :
        return [listA]
        
    if len(listA)>maxItemCombi:
        logger.error(f'cannot generate all combinaison too many item in list : {len(listA)} max is {maxItemCombi}')
        raise ValueError(f'cannot generate all combinaison too many item in list : {len(listA)} max is {maxItemCombi}')
        return -1
    if len(listA)>maxItemCombi/2:
        logger.warning(f'start combi for {len(listA)} items ')
    list_all = list()
    if p is None :
        for i in  range(len(listA),0,-1)   :
            list_all = list_all+list(itertools.combinations(listA,i))
    else :
        list_all =  list(itertools.combinations(listA, p))
    return list_all


def all_combi_by_size(prev_all_combi,list_size=0,combi_size=0,listA=[]):
    #Assuming prev_all_combi contain all combinaison of size combi_size-1 
    # , return all combi of size combi_size
    # check size in prev_all_combi
    new_all_combi=list()
    new_all_combi_item=list()
    new_combi_item=[]
    
    if len(listA) > 0 :
        list_size = len(listA)
        gen_item = True
    else :
        gen_item =False 
        
    if combi_size==0:
        
        combi_size=len(prev_all_combi[0])+1
    for combi in prev_all_combi:
        if len(combi)!=combi_size -1 :
            logger.error(f'combi {combi} should ne of size {combi_size -1}')
            return {'new_all_combi':0, 'new_all_combi_item':0}
        max_cur=combi[combi_size-2]
        if max_cur <list_size-1:
            for i in range (max_cur+1,list_size):
                new_combi=combi.copy()
                new_combi.append(i)
                if gen_item :
                    new_combi_item = [listA[j] for j in new_combi]
                    new_all_combi_item.append(new_combi_item)
                new_all_combi.append(new_combi)
                
    return {'new_all_combi':new_all_combi, 'new_all_combi_item':new_all_combi_item}

def find_possible_combi(allcombi,data_table,target_field='expected',max_nb_found=None,observer=None,minlen=1000):

    collist=[]
    bestcollist=[]
    best_len=0
    logger.debug( f'len allcombi {len(allcombi)}')
    nb_found=0
    if observer :
        observer.notify(expected_complexity=len(allcombi))
    for collist in allcombi :
            if observer:
                observer.notify()
            #log.info(collist)
            if minlen>= len(collist):
                collistcopy=list(collist)
                logger.debug( collistcopy)
                testLen=len(data_table[collistcopy].drop_duplicates())
             
                testLen2=len(data_table[[*collistcopy,target_field]].drop_duplicates())
                #log.info(f'col1 {collist} {testLen} {testLen2} {testLen==testLen2}')
                if testLen==testLen2:
                    if minlen> len(collist):
                        bestcollist=[]
                        
                    minlen=len(collist)
                    bestcollist.append([collist])
                    logger.debug (f'col1 {collist} {testLen} {testLen2} {testLen==testLen2}')
                    if max_nb_found:
                        if len(bestcollist) > max_nb_found :
                            return bestcollist
    return bestcollist 

def dec_tree_to_table(decision_tree,level=0,pre_line='',line_nb=0):
        # input decision tree format : formula= {'cond_field':cond_field,'cond_value':valX,'then':sub_cond}
        table_dict=dict()
        continue_now =True
       
        if type(decision_tree) is dict :
            condition=f"{decision_tree['cond_field']}=={decision_tree['cond_value']}"
            if type(decision_tree['then']) is  list :
                table_dict=dict()
                if len(pre_line)>0:
                    line_id=f'{pre_line}.{str(line_nb)}'
                else :
                    line_id=str(line_nb)
                table_dict={line_id:{'cond_'+str(level):condition},
                    **(dec_tree_to_table(decision_tree['then'],level=level+1,pre_line=line_id,line_nb=0))}
                
                logger.debug('Handle list')
            else :
                if len(pre_line)>0:
                    line_id=f'{pre_line}.{str(line_nb)}'
                else :
                    line_id=str(line_nb)
                if type(decision_tree['then'] ) is dict :
                    then_type = list(decision_tree['then'].keys())[0]
                    val=decision_tree['then'][then_type]
                else :
                    val = decision_tree['then']
                table_dict={line_id:{'cond_'+str(level):condition,'value': val }}
        if type(decision_tree) is list :
            table_dict=dict()
            for line in decision_tree :
                table_dict={**table_dict,**(dec_tree_to_table(line,pre_line=pre_line,level=level,line_nb=line_nb))}
                line_nb=line_nb+1
                

        return  table_dict

def dec_tree_to_data_frame(decision_tree,with_id=True):
    resultDict = dec_tree_to_table(decision_tree)
    logger.debug(resultDict)
    return pandas.DataFrame.from_dict(resultDict,orient='index').sort_index()

def select_on_multi_fields(data_table,table_condition,value_field,one_only=True,default=None):
    # return a dat dataframe that is an extract of data_table 
    # base on the condition define in the table_condition data frame (column = value)
    # table_condition should be a data frame with 1 line and column that exist in data_table
    logger.debug(f'get into multi field table_condition {table_condition} field {value_field}' )
    if len(table_condition.columns & data_table.columns) != len(table_condition.columns ):
        logger.error('wrong condition field in {table_condition.columns}')
        return None
        
    res =pandas.merge(data_table,table_condition,on=list(table_condition.columns))
    logger.debug(f'result of select {res}')
    if one_only :
        if len(res)==1 :
            try:
                return res[value_field][0]
            except :
                return None
        if len(res)==0:
            return default
        else :
            return None
       
    else :
        return res[value_field]

def add_id_in_tree(rule_tree, parent=None, index=None):
    '''
    Add ID in tree (especially rule tree) to facilitate search of information and identify easily each node of the tree
    ID is in the form of X.Y where X is the ID of the parent node and X.Y ID of the current node
    '''
    logger.debug("Entering add_id_in_tree with rule tree: " + str(rule_tree))
    for item in rule_tree:
        if index is None:
            index = 1
        else:
            index += 1
        if parent is None:
            item['id'] = index
        else:
            item['id'] = '{0}.{1}'.format(parent, index)

        if type(item['then']) == type([]):
            add_id_in_tree(item['then'], item['id'], None)

    return rule_tree



def rule_tree_value_info(rule_tree, parent_id = ""):
    '''
    Create a simplify view of the rule tree that we can easily used to determine which
    element need to be lookup for group by or to be deleted
    '''
    logger.debug("Entering rule_tree_value_info with rule tree: " + str(rule_tree))
    final = dict()
    for elem in rule_tree:

        if type(elem['then']) == type({}):
            value = elem['then']['value']
        else:
            #Using hash to have separate list when there is child conditions
            value = "__HASH:"+str(hash(str(elem['then'])))
        
        cond_value = {elem['cond_value']:elem['id']}
        cond_field = elem['cond_field']
        new_value = str(parent_id)+"/"+value
        if cond_field not in final:
            final[cond_field] = dict()
        if new_value not in final[cond_field]:
            final[cond_field][new_value] = list()
        final[cond_field][new_value].append(cond_value)

        if type(elem['then']) == type([]):
            inter = rule_tree_value_info(elem['then'], elem['id'])
            for key in inter:
                if key not in final:
                    final[key] = inter[key]
                else:
                    final[key].update(inter[key])
            
    return final

def intersection(lst1, lst2): 
  
    # Use of hybrid method 
    return set(lst1).intersection(lst2) 


def cover_set_optim(data_set, subset_dict):
    #select and orer the subset thta can cover best the daat_set with fewer set
    logger.debug(f'eneter cover_set_optim {subset_dict}')

    if isinstance(subset_dict,dict) :
        subset_dict = [(k,v) for k,v in subset_dict.items()]

    data_to_cover = set(data_set)
    subset_opt_list=list()
    cur_subset_list = subset_dict
    while len(data_to_cover)>0 and len(cur_subset_list)>0:
        
        best_subset=[0,[]]
        tmp_subset_list=list()
        for subset_k in cur_subset_list:
            inter_data = intersection(subset_k[1], data_to_cover)
            if len(inter_data)>len(best_subset[1]) :
                best_subset = [subset_k[0],inter_data]
                logger.debug(f'best subset is {best_subset}')
            tmp_subset_list.append ( [subset_k[0],inter_data] )
    
        subset_opt_list.append(best_subset)
        clean_subsets = list()
        data_to_cover = data_to_cover - set(best_subset[1])
        for subset_k  in tmp_subset_list :
            inter_data = set(subset_k[1]) - set(best_subset[1])
            if len(inter_data)>0  :
                clean_subsets.append( [ subset_k[0] , inter_data])
        logger.debug(f'new clean_subsets {clean_subsets}')

        cur_subset_list = clean_subsets

    return (subset_opt_list , data_to_cover)


def get_all_learningenv_to_local(self,learningEnv) :
    # assign all the  varioable LP_PARAM if it is in the learning prama dict
    i=0

    for param_name in learningEnv:
        if hasattr(self, param_name) :
            setattr(self, param_name, learningEnv[param_name])
            logger.debug(f'assigne {param_name} with value {learningEnv[param_name]}')
            i=+1
    logger.info(f' {i} local parameter assigned ')


def generate_path_filename_datetime(path_filename, add_on = ""):
    return os.path.dirname(path_filename) + "/" + os.path.splitext(os.path.basename(path_filename))[0] + \
            add_on + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + os.path.splitext(os.path.basename(path_filename))[1]


def xls_file_to_dict(xls_file, xls_sheets = None):
    '''
    Create and return a dictionary from an excel file.
    Will read all sheets of the excel file if none is provided in xls_sheets.
    xls_sheets can be a single sheet or a list of sheet.
    '''
    alldict = dict()


    if isinstance( xls_file,  pandas.io.excel._base.ExcelFile)  :
        xls = xls_file
    else:
        xls = pd.ExcelFile(xls_file,engine='openpyxl')


    if not xls_sheets:
        xls_sheets = xls.sheet_names[0:]
    else:
        if isinstance(xls_sheets, str):
            xls_sheets = {xls_sheets}
        else:
            xls_sheets = set(xls_sheets)

    for sheet_name in xls_sheets:
        if sheet_name in xls.sheet_names[0:]:
            sheet = pd.read_excel(io=xls_file,engine='openpyxl',  skiprows=0, sheet_name=sheet_name)
            dict_json = sheet.to_dict(orient="records")
            alldict[sheet_name] = dict_json
        else:
            logger.info(sheet_name + "do not exist in " + xls_file)
    return alldict


def merge_dict(dict_list, key, acceptDuplicateDict = True):
    '''
    Merge a list of dict together for a given key and create a new entry in the
    final dict if 2 sub_keys are similar in 2 dict
    '''
    all_dict = dict()
    for source_dict in dict_list:
        list_dict = source_dict.get(key, {})
        for dico_name in list_dict:
            if dico_name in all_dict:
                if acceptDuplicateDict is True:
                    all_dict[dico_name+"_"] = list_dict[dico_name]
                    logger.info("Adding " + dico_name + " with _ since already existing")
                else:
                    logger.info("Not adding " + dico_name + " since already existing")
            else:
                all_dict[dico_name] = list_dict[dico_name]

    return all_dict

def _to_float(x):
    '''
    convert content of variable to float it string or list
    '''
    if isinstance(x,str):
        return float (x.replace(',',''))
    elif  isinstance(x,int) or isinstance(x,float) :
        return x
    else :
        raise ValueError



def to_float(xlist):
    '''
    convert content of variable to float it string or list
    '''
    if isinstance(xlist , str ):
        return _to_float(xlist)
    try :
        return [_to_float(y) for y in xlist]
    except TypeError :
        return _to_float(xlist)

def compare_str_as_float(x,y):
    try :
        return _to_float(x) == _to_float(y)
    except  :
        return False

def compare_str_as_date(x,y):
    try :
        return pd.to_datetime(x) == pd.to_datetime(y)
    except  :
        return False


def pd_read_excel(*args,**kargs):
    kargs['engine']='openpyxl'
    clean_columns =  kargs.pop('clean_columns', True)
    tdf = pd.read_excel(*args,**kargs)
    if clean_columns:
            return clean_excel_columns(tdf)
    else :
        return tdf



def clean_excel_columns(tdf):
    ## clean header after load of excel (due to pb with opnpyxl
    raw_cols =  tdf.columns
    new_cols=list()
    for i in range(len(raw_cols)):
        if raw_cols[i] is None :
            new_cols.append(f'Unnamed_col_{i}')
        else :

            new_cols.append(raw_cols[i])
    tdf.columns = new_cols
    return tdf

def safe_keys(source_dict):
    ## check the type of the dictionary key, if not all the same replace by str
    if len (source_dict)<2 :
        return source_dict
    keys_list = source_dict.keys()
    first_type = None
    for i in keys_list :
        if first_type is None :
            first_type=type(i)
            continue
        if type(i) != first_type :
            new_dict = {str(k):v for k,v in source_dict.items()}
            return new_dict
    return source_dict

def split_form(form,remove_df=False):
    eq_split = form.split("=")
    if len(eq_split) >2 :
        raise (f"formulat cannot have more than one = error in {form}")
    elif len(eq_split) == 2 :
        clean_form = eq_split[1]
    else :
        clean_form = form
    clean_form = clean_form.replace(' ','')
    return split_form_clean(clean_form,remove_df=remove_df)

def split_form_clean(form,remove_df=False,replace_dict=None):
    tree = ()
    if form.find(')')>=0 :
        c= '('
        i =form.find(')')
        j = form.rfind('(',0,i)
        in_parent_form = form[j + 1:i ]
        before_parent = form[:j ]
        last_funct=re.split("[\+,\-,/,\*]", before_parent)[-1]
        if len(last_funct)>0 :
            funct_args=in_parent_form.split(',')
            new_form = before_parent[:-len(last_funct)] + '@' + form[i + 1:]
            tuple_args = tuple ( [ split_form_clean(a, remove_df=remove_df, replace_dict=replace_dict) for a in funct_args ])
            tree_p = (last_funct,tuple_args)
            if new_form == "@":
                tree = tree_p
            else :
                tree = split_form_clean(new_form, remove_df=remove_df, replace_dict={'@': tree_p})
        else :
            new_form = before_parent +'@' +form[i+1: ]
            tree_p =  split_form_clean(in_parent_form,remove_df=remove_df,replace_dict=replace_dict)
            tree = split_form_clean(new_form,remove_df=remove_df,replace_dict={'@':tree_p})

    elif form.find('+')>= 0 :
        c = '+'
        i =form.find(c)
        tree = (c, (split_form_clean(form[:i],remove_df=remove_df,replace_dict=replace_dict), split_form_clean(form[i + 1:],remove_df=remove_df,replace_dict=replace_dict) ))
    elif form.find('-') >= 0:
        c = '-'
        i = form.find(c)
        tree = (c, (split_form_clean(form[:i],remove_df=remove_df,replace_dict=replace_dict), split_form_clean(form[i + 1:],remove_df=remove_df,replace_dict=replace_dict)))
    elif form.find('*') >= 0:
        c = '*'
        i = form.find(c)
        tree = (c, (split_form_clean(form[:i],remove_df=remove_df,replace_dict=replace_dict), split_form_clean(form[i + 1:],remove_df=remove_df,replace_dict=replace_dict)))
    elif form.find('/') >= 0:
        c = '/'
        i = form.find(c)
        tree = (c, (split_form_clean(form[:i],remove_df=remove_df,replace_dict=replace_dict), split_form_clean(form[i + 1:],remove_df=remove_df,replace_dict=replace_dict)))
    elif remove_df and form.find('[') >= 0 :
        i = form.find('[')
        j = form.find(']')
        tree = form[i+1:j].replace("\'","")

    if isinstance(tree, str):
        return  tree

    if len(tree) > 0  :
        if replace_dict is not None :
            if tree[1][1] in replace_dict:
                tree = (tree[0],(tree[1][0], replace_dict[tree[1][1]] ))
            elif tree[1][0] in replace_dict:
                tree = (tree[0], (replace_dict[tree[1][0]],  tree[1][1] ))


        return (tree)

    return (form)
