import pywordsegment

seg = pywordsegment.WordSegmenter()
seg.load()

for i in range(10000):
    seg.segment('whatiswrittenhereisbad')
