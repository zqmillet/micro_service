def testcases():
    with open('./validations/text.txt', 'rb') as file:
        data = ''
        while True:
            part = file.read(10)
            data += part.decode('utf8')

            if not part:
                break

    print(data)

if __name__ == '__main__':
    testcases()
