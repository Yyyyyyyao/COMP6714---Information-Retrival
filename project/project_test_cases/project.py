def decToBin(n):
    return bin(n).replace("0b", "")
def split_string_by_n_tag (n,binNum):
    return [binNum[  index : index+n] for index in range( 0,len(binNum),n)]
def split_string_by_n (n,binNum):
    return [binNum[ 0 if (index - 8<0) else index - 8 : index] for index in range(len(binNum), 0, -n)]
def split_list_by_n(n, posting_list):
    return [posting_list[i:i + n] for i in range(0, len(posting_list), n)]

def encode_32bits(small_list,prev):
    binList = []
    tags = ""
    new_posting_with_gap = []
    for p in small_list:
        new_posting_with_gap.append(p-prev)
        prev = p
    for num in new_posting_with_gap:
        binNum = decToBin(num);
        split_strings = split_string_by_n(8,binNum)
        if len(split_strings) == 1 :
            tags+="00"
        elif len(split_strings) == 2 :
            tags+="01"
        elif len(split_strings) == 3 :
            tags+="10"
        elif len(split_strings) == 4 :
            tags+="11"
        binNums = []
        for b in split_strings:
            binNums.append(int(b,2))
        binList+=binNums
    while (len(tags) != 8):
        tags += '0'
    binList.insert(0,int(tags,2))
    return binList;
def encode(posting_list):
    small_groups = split_list_by_n(4,posting_list)
    final_list = []
    prev = 0
    for group in  small_groups:
        final_list+=encode_32bits(group, prev)
        prev = group[-1]
        len_group = len(group)
        while (len_group < 4):
            final_list+= [int("00000000",2)]
            len_group+=1
    return bytearray(final_list)


def decode_small_group (small_encoded_list):
    tags_index = 0
    docID_list = []
    first_docId = -1;
    total_len = len(small_encoded_list);
    while (tags_index < total_len):
        tags = small_encoded_list[tags_index]
        total_length = len(small_encoded_list);
        tags = decToBin(tags).zfill(8)
        tag_list = split_string_by_n_tag(2, tags)
        current_idx = tags_index+1;
        
        for idx, sub_tag in enumerate(tag_list):
            if int( decToBin(small_encoded_list[current_idx]),2)==0:
                return docID_list            
            if (sub_tag == "00"):
                gap = int( decToBin(small_encoded_list[current_idx]).zfill(8),2)
                current_idx+=1
            elif (sub_tag == "01"):
                gap = int(decToBin(small_encoded_list[current_idx+1]).zfill(8) + decToBin(small_encoded_list[current_idx]).zfill(8),2)
                current_idx+=2
            elif (sub_tag == "10"):
                gap = int( decToBin(small_encoded_list[current_idx+2]).zfill(8)+decToBin(small_encoded_list[current_idx+1]).zfill(8) + decToBin(small_encoded_list[current_idx]).zfill(8),2)
                current_idx+=3
            elif (sub_tag == "11"):
                gap = int(decToBin(small_encoded_list[current_idx+3]).zfill(8)+ decToBin(small_encoded_list[current_idx+2]).zfill(8)+decToBin(small_encoded_list[current_idx+1]).zfill(8) + decToBin(small_encoded_list[current_idx]).zfill(8),2)
                current_idx+=4
            if (first_docId == -1):
                first_docId = gap
                docID_list.append(first_docId)
            else:
                docID_list.append(docID_list[-1] + gap)
        tags_index = current_idx
    return docID_list
        
def decode(encoded_list):
    dec_list = list(encoded_list)
    ret_list = []
    ret_list+=decode_small_group(dec_list)
    return ret_list


def evaluation(rel_list, total_rel_doc):
    total = len(rel_list)
    predict_rel = rel_list.count(1)
    F1 = 2* ( predict_rel/total * predict_rel/total_rel_doc)  / (predict_rel/total + predict_rel/total_rel_doc)
    sum = 0;
    for idx, pred in enumerate(rel_list):
        if (pred == 1):
            sum += ( rel_list[0:idx+1].count(1)/(idx+1))
    map_s =  (sum/total_rel_doc)
    return F1, map_s

