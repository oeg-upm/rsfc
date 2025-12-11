class CodemetaHarvester:
    
    def __init__(self, gh):
        self.codemeta_data = self.harvest_codemeta(gh.codemeta)
        
    
    def harvest_codemeta(self, codemeta):
        if codemeta != None:
            codemeta_info = {
                "license": None,
                "author": None,
                "contributor": None,
                "identifier": None,
                "referencePublication": None,
                "version": None
            }
            
            if "license" in codemeta:
                codemeta_info["license"] = codemeta["license"]
                
            if "identifier" in codemeta:
                codemeta_info["identifier"] = codemeta["identifier"]
                
            if "referencePublication" in codemeta:
                codemeta_info["referencePublication"] = codemeta["referencePublication"]
                
            if "author" in codemeta:
                codemeta_info["author"] = codemeta["author"]
                
            if "contributor" in codemeta:
                codemeta_info["contributor"] = codemeta["contributor"]
                
            if "version" in codemeta:
                codemeta_info["version"] = codemeta["version"]
                
            return codemeta_info
        else:
            return None
            