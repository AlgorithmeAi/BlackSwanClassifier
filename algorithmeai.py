import requests
import json

class BlackSwanClassifier():
    def __init__(self, filepath, target_index=0, excluded_features_index=[]):
        self.log = """###########################################################################
#                                                                         #
#   Algorithme.ai : proprietary technology developed on August 2025       #
#                                                                         #
#        author : Charles Dana   product : BlackSwanClassifier            #
#                                                                         #
###########################################################################
"""
        self.hash = 0
        if ".csv" in filepath:
            with open(filepath, "r") as f:
                lines = f.readlines()
            csv_txt = "".join(lines)
            ret = self.send_request({
            "csv_train" : csv_txt,
            "action" : "build",
            "target_index" : target_index,
            "excluded_features_index" : excluded_features_index
            })
            self.hash = ret["hash"]
            self.log = ret["log"]
            print(f"# Algorithme.ai : Code Built with hash {self.hash}")
        elif len(filepath) == 64 and not ".csv" in filepath and not ".json" in filepath:
            ret = self.send_request({
            "hash" : filepath,
            "action" : "ping"
                         })
            self.hash = ret["hash"]
            self.log = ret["log"]
        elif ".json" in filepath:
            with open(filepath, "r") as f:
                loaded_module = json.load(f)
            self.hash = loaded_module["hash"]
            self.log = loaded_module["log"]
    
    def send_request(self, payload):
        url = "https://g6xi2kghmcr6brrox7ec4bc2yu0nxpiy.lambda-url.us-east-1.on.aws/"
        response = requests.post(url, json=payload)
        print(f"# Algorithme.ai : Response Status {response.status_code}")
        return response.json()
        
    def improve(self):
        ret = self.send_request({"hash" : self.hash, "action" : "improve"})
        self.hash = ret["hash"]
        self.log = ret["log"]
        print(f"# Algorithme.ai : Code Improved with hash {self.hash}")
    
    def improvePrecision(self):
        ret = self.send_request({"hash" : self.hash, "action" : "improve-precision"})
        self.hash = ret["hash"]
        self.log = ret["log"]
        print(f"# Algorithme.ai : Code Improved Precision with hash {self.hash}")
        
    def improveRecall(self):
        ret = self.send_request({"hash" : self.hash, "action" : "improve-recall"})
        self.hash = ret["hash"]
        self.log = ret["log"]
        print(f"# Algorithme.ai : Code Improved Recall with hash {self.hash}")
    
    def make_population(self, filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
        csv_txt = "".join(lines)
        ret = self.send_request({
        "csv_test" : csv_txt,
        "action" : "make-population",
        "hash" : self.hash,
        })
        self.hash = ret["hash"]
        self.log = ret["log"]
        population = ret["population"]
        print(f"# Algorithme.ai : Returned population of size {len(population)} with hash {self.hash}")
        return population
    
    def get_auc(self, filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
        csv_txt = "".join(lines)
        ret = self.send_request({
        "csv_test" : csv_txt,
        "action" : "get-auc",
        "hash" : self.hash
                                })
        self.hash = ret["hash"]
        self.log = ret["log"]
        auc = ret["auc"]
        print(f"# Algorithme.ai : Returned auc {auc} over {filepath} with hash {self.hash}")
        return auc
        
    def get_auc_opt(self, filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
        csv_txt = "".join(lines)
        ret = self.send_request({
        "csv_test" : csv_txt,
        "action" : "get-auc-opt",
        "hash" : self.hash
                                })
        self.hash = ret["hash"]
        self.log = ret["log"]
        auc = ret["auc"]
        opt = ret["opt"]
        print(f"# Algorithme.ai : Returned auc {auc} with {opt} optimal threshold over {filepath} with hash {self.hash}")
        return auc, opt
    
    def get_global_feature_importance(self, filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
        csv_txt = "".join(lines)
        ret = self.send_request({
        "action" : "get-global-feature-importance",
        "csv_test" : csv_txt,
        "hash" : self.hash
                    })
        self.hash = ret["hash"]
        self.log = ret["log"]
        global_feature_importance = ret["global_feature_importance"]
        print(f"# Algorithme.ai : Got Global Feature Importance {global_feature_importance} with hash {self.hash}")
        return global_feature_importance
    
    def get_confidence(self, filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
        csv_txt = "".join(lines)
        ret = self.send_request({
        "csv_test" : csv_txt,
        "action" : "get-confidence",
        "hash" : self.hash
                                })
        self.hash = ret["hash"]
        self.log = ret["log"]
        confidence = ret["confidence"]
        print(f"# Algorithme.ai : Got confidence {confidence} with hash {self.hash}")
        return confidence
    
    def filter(self, filepath, opt=0.5):
        confidence = self.get_confidence(filepath)
        filter_index = sorted([int(t) for t in confidence if confidence[t] >= opt])
        print(f"# Algorithme.ai : Got filtered_index {filter_index} for {filepath} with hash {self.hash}")
        return filter_index
    
    def get_audit(self, item):
        ret = self.send_request({
        "item" : item,
        "action" : "get-item-audit",
        "hash" : self.hash
                                })
        audit = ret["audit"]
        self.hash = ret["hash"]
        self.log = ret["log"]
        print(f"# Algorithme.ai : Got audit {audit} for {item} with hash {self.hash}")
        return audit
    
    def get_feature_importance(self, item):
        ret = self.send_request({
        "item" : item,
        "action" : "get-item-feat",
        "hash" : self.hash
                                })
        feature_importance = ret["feature_importance"]
        self.hash = ret["hash"]
        self.log = ret["log"]
        print(f"# Algorithme.ai : Got feature importance {feature_importance} for item {item} with hash {self.hash}")
        return feature_importance
    
    def get_item_confidence(self, item):
        ret = self.send_request({
        "item" : item,
        "action" : "get-item-conf",
        "hash" : self.hash
                                })
        confidence = ret["confidence"]
        self.hash = ret["hash"]
        self.log = ret["log"]
        print(f"# Algorithme.ai : Got confidence {confidence} for item {item} with hash {self.hash}")
        return confidence
        
    def to_json(self, fileout="blackswan-api.json"):
        blackswan = {
            "log" : self.log,
            "hash" : self.hash
        }
        with open(fileout, "w") as f:
            f.write(json.dumps(blackswan, indent=2))
        print(f"# Algorithme.ai : Safely saved at {fileout}")
