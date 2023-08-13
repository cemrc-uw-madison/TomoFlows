#!/usr/bin/python3

'''
Represent an mdoc file and descriptive fields.
Parse from text file.
'''

import argparse

class FrameSet:
    ''' Represent a FrameSet entry of mdoc '''
    Index = 0
    ''' Use a python dictionary to flexibly capture MDoc data '''
    nameVal = {}

    def getString(self):
        ''' get a printable representation '''
        lines = []
        lines.append('[FrameSet = ' + str(self.Index) + ']\n')

        for key in self.nameVal:
            line = key + ' = ' + self.nameVal[key] + '\n'
            lines.append(line)

        # Concatenate and return 
        return ''.join(lines)

class MDoc:
    ''' Represent an mdoc metadata file '''
    nameVal = {}

    ''' Frameset entries '''
    framesets = []

    @staticmethod
    def parse(filename):
        ''' parse a filename to create an MDoc (field = value) '''
        rv = MDoc()

        currentFrameSet = None

        # Parse header or FrameSet information
        with open(filename) as file:
            for line in file.readlines():
                ''' Parse a line '''
                line = line.strip()
                if line.startswith('['):
                    ''' May be the start of a new FrameSet entry '''
                    currentFrameSet = FrameSet()
                    rv.framesets.append(currentFrameSet)
                    
                elif line:
                    ''' Split and get the parts '''
                    parts = line.split(' = ')

                    ''' If there are two parts, we'll store values '''
                    if len(parts) > 1:
                        ''' Get the field and value '''
                        field = parts[0]
                        value = parts[1]

                        if currentFrameSet:
                            currentFrameSet.nameVal[field] = value
                        else:
                            rv.nameVal[field] = value
        return rv
                

    def getString(self):
        ''' get a printable representation '''
        lines = []
        
        for key in self.nameVal:
            line = key + ' = ' + self.nameVal[key] + '\n'
            lines.append(line)

        lines.append('\n')
        for fs in self.framesets:
            lines.append(fs.getString())
            lines.append('\n')

        # Concatenate and return 
        return ''.join(lines)


def main():
    # 1. Provide a command-line arguments
    parser = argparse.ArgumentParser(description='Read an mdoc file')
    parser.add_argument('--mdoc', help='mdoc location', required=True)
    args = parser.parse_args()

    # 2. Run : test parsing
    mdoc = MDoc.parse(args.mdoc)

    print(mdoc.getString())

if __name__ == "__main__":
    main()