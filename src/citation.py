class Citation:
    def __init__(self, citation_type, key, fields=None, keywords=None):
        if fields is None:
            fields = {}
        if keywords is None:
            keywords = []
        self.citation_type = citation_type
        self.key = key
        self.fields = fields
        self.keywords = keywords
    


    def __str__(self):
        result = f"@{self.citation_type}{{{self.key},\n"
        for key in self.fields.keys():
            if key == "author":
                result += f"    {key} = {{{" and ".join(self.fields[key])}}},\n"
            else:
                result += f"    {key} = {{{self.fields[key]}}},\n"
        result = result[:-2]
        result += "\n}"
        if self.keywords:
            result += f"% Keywords: {', '.join(self.keywords)}"
        return result
    