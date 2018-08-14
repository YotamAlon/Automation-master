def main(a, b):
    print('a is of type ' + str(type(a)) + ' with value ' + str(a))
    print('and b is of type ' + str(type(b)) + ' with value ' + str(b))
    return a, b


if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])