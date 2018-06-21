import os
def getNotification(contains_text='中文'):
    messages = os.popen("adb shell dumpsys notification")
    print(messages.readlines())
    for line in messages.readlines():
        line = line.strip()
        print(line)
        if not len(line):
            continue
        if contains_text in line:
            print('true')
            return  True
        else:
            print('False')
            return  False


getNotification("")