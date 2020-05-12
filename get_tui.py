import os, logging, csv, collections, functools, traceback, json, array
logging.basicConfig(level=logging.DEBUG)

from tempfile import mkstemp
from os import remove, close

import sys
#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('UTF8')
# rely on PYTHONIOENCODING env variable to get around the above hack

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    return fh, abs_path

if __name__ == '__main__':
    terms = {
        "laboratory_procedure": "T059",
        "disease_or_syndrome": "T047",
        "diagnostic_procedure": "T060",
        "clinical_attribute": "T201",
        "intellectual_product": "T170",
        "finding": "T033",
        "therapeutic_or_preventive_procedure": "T061",
        "health_care_activity": "T058",
        "clinical_drug": "T200",
        "sign_or_symptom": "T184",
        "mental_or_behavioral_dysfunction": "T048",
        "pharmacologic_substance": "T121"
    }
    
    for name, tui in terms.items():
        file_name = "output/" + tui + "-" + name + ".csv"

        f, sparql = replace("get_tui.sparql", "<TUI>", tui)
        os.system('curl -G -v http://localhost:3030/umls/query --data-urlencode "query=`cat ' + sparql + ' `"  --header "Content-Type: application/sparql-query" --header "Accept: text/csv" --header "Timeout: 100000" > ' + file_name)

        remove(sparql)
