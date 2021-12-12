def encode(posting_list):
    append_zero = 4-len(posting_list) % 4
    if(append_zero == 4):
        append_zero = 0
    
    i = 0
    while(i < append_zero):
        posting_list.append(0)
        i += 1
    
    start = 0
    end = 4
    res = ""
    prev = 0
    while(end <= len(posting_list)):
        tag = ""
        ans = ""
        for posting in posting_list[start:end]:
            curr = posting - prev
            prev = posting
            count = 0
            if(posting == 0):
                curr = 0
            binStr = '{0:b}'.format(curr)
            while(len(binStr) > 8):
                ans += binStr[-8:]
                binStr = binStr[0:-8]
                count += 1
            if(len(binStr) > 0):
                temp = (8-len(binStr))*'0'
                ans += temp + binStr
                count += 1
            tag += '{0:02b}'.format(count-1)
        ans = tag + ans
        start = end
        end += 4
        res += ans

    return int(res, 2).to_bytes((len(res) + 7) // 8, byteorder='big')

def decode(encoded_list):
    decode_str = ''.join(format(byte, '08b') for byte in encoded_list)
    res = []
    reading_start = 0
    early_stop = False
    prev = 0
    while(reading_start < len(decode_str)):
        tag = decode_str[reading_start:reading_start+8]
        i = 0
        reading_start = reading_start+8
        while(i <= 6):
            reading_len = int(tag[i:i+2],2)+1
            gap_b = decode_str[reading_start: reading_start+reading_len*8]
            correct_order = "".join(reversed([gap_b[i:i+8] for i in range(0, len(gap_b), 8)]))
            gap_int = int(correct_order,2)
            ans = gap_int + prev
            res.append(ans)
            if(ans == prev and reading_start != 8):
                early_stop = True
                break
            prev = ans
            reading_start = reading_start+reading_len*8
            i += 2
        if(early_stop):
            res = res[0:-1]
            break
    
    return res


def evaluation(rel_list, total_rel_doc):
    retrived_docs = len(rel_list)
    rel_retrived = rel_list.count(1)
    relevant_docs = total_rel_doc
    recall = rel_retrived / relevant_docs
    precision = rel_retrived / retrived_docs
    f1 = 2*(recall*precision) / (recall+precision)

    sum_AP = 0
    count_retrived = 0
    count_rel_retrived = 0
    for indicator in rel_list:
        count_retrived += 1
        if(indicator == 1):
            count_rel_retrived += 1
            sum_AP += count_rel_retrived / count_retrived
        if(count_rel_retrived == rel_retrived):
            break
    mAP = sum_AP / total_rel_doc
    print(f1)
    print(mAP)


posting_list = [1, 2, 3, 4, 5, 4294967299]
encoded_list = encode(posting_list)
# print([bin(code)[2:].zfill(8)for code in encoded_list])
# encoded_list = bytearray(b'\x06\x01\x0f\xff\x01\xff\xff\x01')
decoded_list = decode(encoded_list)
print(decoded_list)

# rel_list = [1,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,1]
# total_rel_doc = 8
# evaluation(rel_list, total_rel_doc)