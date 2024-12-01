class Citation:
    def __init__(self, citation_type, key, fields = dict()):
        self.citation_type = citation_type
        self.key = key
        self.fields = fields
    

    def __str__(self):
        result = f"@{self.citation_type}{{{self.key},\n"
        for key in self.fields.keys():
            result += f"    {key} = {{{self.fields[key]}}},\n"
        result = result[:-2]
        result += "\n}"
        return result
        
