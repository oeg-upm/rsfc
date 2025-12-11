class CFFHarvester:
    
    def __init__(self, gh):
        self.cff_data = self.harvest_cff(gh.cff)
        
    
    def harvest_cff(self, cff):
        
        if cff != None:
            cff_info = {
                "license": None,
                "authors": None,
                "version": None,
                "identifiers": None,
                "preferred-citation": None
            }
            
            if "license" in cff:
                cff_info["license"] = cff["license"]
                
            if "authors" in cff:
                cff_info["authors"] = cff["authors"]
                
            if "version" in cff:
                cff_info["version"] = cff["version"]
                
            if "identifiers" in cff:
                cff_info["identifiers"] = cff["identifiers"]
                
            if "preferred-citation" in cff:
                cff_info["preferred-citation"] = cff["preferred-citation"]
                
            return cff_info
        else:
            return None