import sys
from linkedList import LinkedList


TRANSLATION_CONST = int('0x1ff', 16)
PW_CONST = int('0x3ffff', 16)
FRAME_SIZE = 512
NUM_FRAMES = 1024
PM_SIZE = FRAME_SIZE*NUM_FRAMES

class VirtualMemoryManager():
    def __init__(self):
        # initialization
        self.PM = [0] * PM_SIZE
        self.D = [0] * PM_SIZE
        self.free_frames = LinkedList()

        for x in range(1, NUM_FRAMES):
            self.free_frames.insert(x)
        

    def fillPM(self, filename):
        """
        Given a filename in the working directory, parse that file to fill the PM array with PT and ST entries

        Files are formatted with 2 lines defining the ST and PT
           * for each tuple in line 1, call fillPT
           * for each tuple in line 2, call fillST
        """

        with open(filename, "r") as file:
            line1 = file.readline()
            line2 = file.readline()
        
        for s, z, f in self.format_triplets(line1):
            self.fillST(int(s), int(z), int(f))

        for s, p, f in self.format_triplets(line2):
            self.fillPT(int(s), int(p), int(f))

    def format_triplets(self, line):
        """
        (For easier parsing/formatting/processing): Given a line of numbers, format into a list of three-tuples
        """
        line = line.split()
        lst = []
        for i in range(0, len(line), 3):
            lst.append((line[i], line[i+1], line[i+2]))

        return lst

    def fillST(self, s, z, f):
        """
        Given a tuple (s,z,f), fills the PM with ST entry.

        PT of segment s resides in frame f. Length of segment s is z.
        """
        self.PM[2*s] = z
        self.PM[(2*s)+1] = f
        if f >= 0: 
            self.free_frames.remove(f)      # f no longer free


    def fillPT(self, s, p, f):
        """
        Given a tuple (s,p,f), fills the PM with PT entry

        Page p of segment s resides in frame f
        """
        if self.PM[(2*s)+1] >= 0:
            self.PM[(self.PM[(2*s)+1]*FRAME_SIZE)+p] = f
            if f >= 0:
                self.free_frames.remove(f)          # f no longer free
            
        else:
            b = abs(self.PM[(2*s)+1])
            self.D[b*FRAME_SIZE+p] = f


    def processInput(self, filename, outfile="output-no-dp.txt"):
        """
        Given a text file in the working directory, parse the file for VAs. 
        Translate each virtual address, and add to an output file
        """

        with open(filename, "r") as file:
            inputs = file.readline().split()

        with open(outfile, "w") as out:
            for i in inputs:
                PA = self.translate(int(i))
                out.write(f"{PA} ")

    def loadPT(self, s):
        # allocate free frame f1 using list of free frames
        PM = self.PM
        b = abs(PM[(2*s)+1])                # PT is in disk block b
        frame = self.free_frames.pop()      # update list of free frames

        self.read_block(b, frame*512)       # read disk block b into PM starting at location m=f1*512
        PM[(2*s)+1] = frame                 # replace -b with frame/update ST entry


    def loadPage(self, s, p):
        PM = self.PM
        frame = self.free_frames.pop()      # update list of free frames
        b = abs(PM[PM[(2*s)+1]*512+p]) 
        self.read_block(b, frame*512)
        PM[PM[(2*s)+1]*FRAME_SIZE + p] = frame
        
   
    def read_block(self, b, m):
        """
        Copies block D[b] into PM frame starting at location PM[m]
        """
        for i in range(FRAME_SIZE):
            self.PM[m + i] = self.D[b * FRAME_SIZE + i]


    def translate(self, address):
        """
        Given a 32-bit virtual address, return the physical address 

        Each (s,p,w) is 9 bits w/ leading 5 bits of VA unused.
        pw is (p w) combined in binary
        PA = PM[PM[2s+1]*512+p]*512+w
        """
        PM = self.PM

        
        s = address >> 18                       # s: right-shift by 18 bits
        pw = address & PW_CONST                 # pw: AND VA with 11 1111 1111 1111 1111 (3FFFF)
        p_temp = address >> 9                   # p: right shift VA by 9, then AND with 1 1111 1111 (1FF)
        p = p_temp & TRANSLATION_CONST  
        w = address & TRANSLATION_CONST         # w: AND address with 1 1111 1111 (1FF)

        # check if pw >= PM[2s] 
        if pw >= PM[2*s]:
            return -1           # error
        
        if PM[(2*s)+1] < 0:             # page fault: PT not resident
            self.loadPT(s)
    
        
        if PM[PM[(2*s)+1]*512 + p] < 0:     # page fault: page not resident
            self.loadPage(s, p)
        
        PA = self.PM[(self.PM[2*s+1]*FRAME_SIZE)+p]*FRAME_SIZE+w

        return PA

    def run(self, initFile, inputFile, outFile="output-dp.txt"):
        self.fillPM(initFile)
        self.processInput(inputFile, outFile)
    

if __name__ == "__main__":
    VM = VirtualMemoryManager()
    initFile = sys.argv[1]
    inputFile = sys.argv[2]

    VM.run(initFile, inputFile)



