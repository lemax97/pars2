#User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36


from collections import namedtuple

InnerBlock = namedtuple('Block', 'title, price, currency, date, url')

class Block(InnerBlock):
    def __str__(self):
        return f'{self.title}\t{self.price} {self.currency}\t{self.date}\t{self.url}'

x = InnerBlock(title='title', price='100.0', currency='200.0', date='11.02.2020', url='xxx.com')
print(x)

x = Block(title='title', price='100.0', currency='200.0', date='11.02.2020', url='xxx.com')
print(x)