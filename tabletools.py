# tabletools.py 

class LabeledList:
    def __init__(self, data=None, index=None):
        self.values = data
        if index == None:
            self.index=range(len(data))
        else:
            self.index = index
  
    def __str__(self):
        if len(self.values)==0:
            return ''
        res =""
        lenval=[]
        lenin =[]
        for i in self.values:
            lenval.append(len(str(i)))
        for i in self.index:
            lenin.append(len(str(i)))
        vals_max_len = max(lenval)
        vals_max_i= max(lenin)

        for val,ind in zip(self.values, self.index):
            res = res+ (f'{ind:>{vals_max_i}} {str(val):>{vals_max_len}}\n')
        return res

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key_list):
        temp_key=[]
        temp_val =[]
        if isinstance(key_list, LabeledList):
            for val,ind in zip(self.values,self.index):
                if ind in key_list:
                    temp_key.append(ind)
                    temp_val.append(val)
            return LabeledList(temp_val,temp_key)
        
        elif isinstance(key_list, list):
            if(isinstance(key_list[0], bool)):
                for val,ind,tf in zip(self.values,self.index,key_list):
                    if (tf==True):
                        temp_key.append(ind)
                        temp_val.append(val)
                return LabeledList(temp_val,temp_key) 
            else:
                for val,ind in zip(self.values,self.index):
                    if ind in key_list:
                        temp_key.append(ind)
                        temp_val.append(val)
                if (len(temp_val)!=1):
                    return LabeledList(temp_val,temp_key)
                else:
                    return temp_val[0]
        else: # just string
            for val,ind in zip(self.values,self.index):
                if ind in key_list:
                    temp_key.append(ind)
                    temp_val.append(val)
            if(len(temp_val)!=1):
                return LabeledList(temp_val,temp_key)
            else:
                return temp_val[0]
  
    def __iter__(self):
        self.n=0
        return self

    def __next__(self):
        if (self.n < len(self.values)):
            result = self.values[self.n]
            self.n+=1
            return result
        else:
            raise StopIteration
            
        
    def __eq__(self, scalar):
        tfvalues = [True if val == scalar else False for val in self.values]
        return LabeledList(tfvalues,self.index)

    def __ne__(self, scalar):
        tfvalues = [True if val != scalar else False for val in self.values]
        return LabeledList(tfvalues,self.index)

    def __gt__(self, scalar):
        tfvalues = [True if val > scalar else False for val in self.values]
        return LabeledList(tfvalues,self.index)

    def __lt__(self, scalar):
        tfvalues = [True if val < scalar else False for val in self.values]
        return LabeledList(tfvalues,self.index)

    def map(self, f):
        mapped=[]
        mapped=list(map(f, self.values))
        return LabeledList(mapped,self.index)


class Table:
    def __init__(self, data, index=None, columns=None):
        if (data==None):
            return None
    
        self.values=data
    
        if (index==None):
            self.index = range(len(data))
        else: 
            self.index= index

        if (columns==None):
            self.columns = range(len(data[0]))
        else: 
            self.columns =columns 


    def __str__(self):  
        if len(self.values)==0:
            return ''
        data=[]
        #row_pad =15
        #find number to pad rows
        # if (type(self.index)==range): 
        #     row_pad= len(str(len(self.index)))
        # else: 
        #     row_pad= max(self.index, key=len)
        rows= [str(i) for i in self.index]
        row_pad= len(max(rows, key=len))+1

        data+=self.columns
        for arr in self.values:
            data+=arr
    
        data =[str(i) for i in data]
        col_pad =len(max( data,key=len))+1

        first_row=""
        #first_row+=(f'{" ":>{col_pad}}')
        first_row+=(f'{" ":>{row_pad}}')

        for i in self.columns:
            first_row+= (f'{i:>{col_pad}}')

        res = first_row+'\n'

        for val,ind in zip(self.values, self.index):
        #add index header at first 
            res+= (f'{ind:>{row_pad}}')
            for ele in val:
                res+=(f'{ele:>{col_pad}}')
            res+='\n'

        return res

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, col_list):
        if isinstance(col_list,LabeledList):
            temp_data=[]
            get_indexes = lambda b, xs: [i for (target, i) in zip(xs, range(len(xs))) if b == target]
            col_index=[]
            new_columns=[]
            for col_name in col_list.values:
                col_index+= get_indexes(col_name,self.columns) # indexes with 'a'
                new_columns+= col_name
            for row in self.values:
                temp_row_val=[]# for row in self.values
                for tar_ind in col_index:
                    temp_row_val.append(row[tar_ind])
                temp_data.append(temp_row_val)
            return Table(temp_data, self.index,new_columns)
            
        if isinstance(col_list,list):
            if isinstance(col_list[0],bool):
                temp_data=[]
                new_index=[]
                for ind,tfval in enumerate(col_list):
                    if tfval == True:
#                         vals=[]
                        new_index.append(self.index[ind])
                        temp_data.append(self.values[ind])
#                         for ele in self.values[ind]:
#                             vals.append(ele)
#                         temp_data.append(vals)
                return Table(temp_data,new_index,self.columns)

            else:
                temp_data=[]
                get_indexes = lambda b, xs: [i for (target, i) in zip(xs, range(len(xs))) if b == target]
                col_index=[]
                new_columns=[]
                for ele in col_list:
                    if ele in self.columns:
                        new_columns.append(ele)
                for col_name in new_columns:
                    col_index+= get_indexes(col_name,self.columns) 
                
                for row in self.values:# for row in self.values
                    temp_row_val=[]
                    for tar_ind in col_index:
                        temp_row_val.append(row[tar_ind])
                    temp_data.append(temp_row_val)
                return Table(temp_data,self.index,new_columns)                

        else: #single value as col_list
            get_indexes = lambda b, xs: [i for (target, i) in zip(xs, range(len(xs))) if b == target]
            col_index=get_indexes(col_list,self.columns)
             # array of indexes of col_list columns 
            
            temp_val=[]
            if len(col_index)==1:
                target=col_index[0]
                for row in self.values:
                    temp_val.append(row[target])
                return LabeledList(temp_val,self.index)

            elif len(col_index)>1:
                new_columns=[col_list] * len(col_index)
                for tar in col_index:
                    target_row=[]
                    for row in self.values:
                        rowvals= row
                        target_row.append(rowvals[tar])
                    temp_val.append(target_row)
                return Table(temp_val,self.index,new_columns)

            else:
                return None





  
    def head(self, n):
        if n<=0:
            return None
        else:
            wanted= Table(self.values[0:n],self.index[0:n],self.columns)
        return wanted

    def tail(self, n):
        if n<=0:
            return None
        else:
            wanted= Table(self.values[-n:],self.index[-n:],self.columns)
        return wanted

    def shape(self): 
        return (len(self.values),len(self.values[0]))


def read_csv(fn):
    with open(fn) as f:
        file = f.read()
    file=file.strip()
    file = file.split('\n')
    first_row =file[0]
    headers = first_row.split(',')
    data=[]

    for row in file[1:]:
        row=row.strip()
        row=row.split(',')
        newrow = []
        for acol in row:
            try:
                acol=float(acol)
                new_row.append(acol)
            except:
                newrow.append(acol) 
        data.append(newrow)
    tableobj = Table(data,columns=headers)
    return tableobj

