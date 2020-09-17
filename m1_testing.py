from pyexpat import ExpatError
import lib.xmltodict as xmltodict
import json

with open('local.xml') as f:
    data = f.read()
    try:
        doc = xmltodict.parse(data)
        config = json.dumps(doc)
        config_dict = json.loads(config)
        if config_dict["config"]["global"]["resources"]["db"]["table_prefix"] == None:
            prefix = ""
        else:
            prefix = config_dict["config"]["global"]["resources"]["db"]["table_prefix"]
        # print(config_dict["config"]["global"]["resources"]["db"]["table_prefix"])
        # config_dict["config"]["global"]["resources"]["default_setup"]["connection"]["host"] = "testing"
        # print(config_dict["config"]["global"]["resources"]["default_setup"]["connection"]["host"])
        # print(xmltodict.unparse(config_dict, pretty=True))
        print(prefix)
    except ExpatError:
        doc = xmltodict.parse(data[2:])
        print(json.dumps(doc))
        config = json.dumps(doc)
