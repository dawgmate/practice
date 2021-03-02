class ContentBox:
    
    def __init__(self, date, content, link):
        self.date = date
        self.content = content
        self.link = link
    
    def input(self, date, content, link):
        self.date.append(date)
        self.content.append(content)
        self.link.append(link)

    def getDate(self):
        return self.date
    
    def getContent(self):
        return self.content
        
    def getLink(self):
        return self.link

