"""
There is no way this would perform on a large dataset, but it was quick to 
write, and our data set is small.

python vcfcompare.py NA11881_bt2.capture-header.sorted.raw.vcf 
   ../homework1/NA11881.hapmap3.3.chr4.recode.vcf > matches.out

Steven Githens
sgithens@iupui.edu
"""

import sys

class Vcf(object):
    def __init__(self,variants):
        "Takes and array of Variant's"
        self.variants = variants

    def stats(self):
        """
        From looking through the sample file, it looks like everything we 
        have is either SNPS or INDELS
        """
        indels = 0
        snps = 0
        total = 0
        for v in self.variants:
            total += 1
            if v.info.find("INDEL") >= 0:
                indels += 1
            else:
                snps +=1
        print "Indels: %s SNPs: %s Total: %s" % (indels, snps, total)

class Variant(object):
    def __init__(self,chrome=4,pos=0,vid='',ref='',alt='',info='',src=''):
        self.chr = chrome
        self.pos = pos
        self.vid = vid
        self.ref = ref
        self.alt = alt
        self.info = info
        self.src = src

def parse_vcf(fname):
    f = open(fname)
    v = []
    for line in f.readlines():
        if not line.startswith("#"):
            p = line.strip().split("\t")
            v.append(
                Variant(chrome=p[0],pos=p[1],ref=p[3],
                        alt=p[4],info=p[7],src=line.strip()))
    return Vcf(v)

def compare(sample,hapmap):
    total = 0
    for v in sample.variants:
        spos = v.pos
        for v2 in hapmap.variants:
            hpos = v2.pos
            if spos == hpos:
                total += 1
                print "Match: %s" % (spos)
                print v.src[:40]
                print v2.src[:40]
    print "Total matches: %s" % (total)

def main():
    sample = parse_vcf(sys.argv[1])
    hapmap = parse_vcf(sys.argv[2])
    #sample.stats()
    compare(sample,hapmap)
    #print "Sample total: %s Hapmap total %s" % (len(sample.variants),len(hapmap.variants))

if __name__ == "__main__":
    main()
