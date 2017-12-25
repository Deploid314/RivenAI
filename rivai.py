from crawler import Crawler

crawler = Crawler()
rivenList = crawler.getItemsForSale()
file = open("writefile.txt","w")
header = str(len(rivenList))+",8,weapon,stat1,stat2,stat3,stat4,statname1,statname2,statname3,statname4,price"
file.write(header)
for riven in rivenList:
    listing = riven.weapon + ","

    for stat in riven.calculated_stats:
        print(stat)
        listing = listing + str(stat) + ","

    for i in range(4,8):
        listing = listing + riven.stats[i] + ","

    listing = listing + riven.price
    file.write("\n")
    file.write(listing)
    print(riven.weapon,riven.stats,riven.calculated_stats,riven.price)

file.close()
"""
list = ["abcd", "acc", "acb"]
list2 = []
for i in list:
    word = i.replace('c', '')
    list2.append(word)
print(list2)
"""
