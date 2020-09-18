def simplify_asr(asr):
    streamlining_words = ["了", "哦", "啊", "呢", '吧', ' ']
    for i in range(len(streamlining_words)):
        asr = asr.replace(streamlining_words[i], '')
        i += 1
    return asr


if __name__ == '__main__':
    asr = "打开空调啊了"
    a = simplify_asr(asr)
    print(a)
