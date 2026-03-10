import xml.etree.ElementTree as ET
import glob
import json
import os

def analyze_stability(path):
    class_counts = {}
    total_elements = 0

    if not os.path.exists(path):
        print(f"BŁĄD: Ścieżka {path} nie istnieje!")
        return

    for file in glob.glob(path + "/**/*.xml", recursive=True):
        try:
            tree = ET.parse(file)
            for elem in tree.iter():
                # Czyścimy nazwę klasy (usuwamy namespace jeśli jest)
                class_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
                total_elements += 1
        except:
            continue

    if total_elements == 0:
        print("Nie znaleziono żadnych elementów do analizy.")
        return

    report = {
        "metrics": {},
        "verdict": "LOW_RISK",
        "warnings": []
    }

    threshold = 0.5  # 50% - próg krytyczny

    for cls, count in class_counts.items():
        percentage = round((count / total_elements) * 100, 2)
        report["metrics"][cls] = f"{percentage}% ({count} objects)"
        
        if percentage > (threshold * 100):
            report["verdict"] = "HIGH_RISK"
            report["warnings"].append(f"Class '{cls}' dominates UI ({percentage}%). Avoid By.className!")

    with open('stability_report.json', 'w') as f:
        json.dump(report, f, indent=4)

    print(f"--- Audit Complete ---")
    print(f"Verdict: {report['verdict']}")
    if report["warnings"]:
        for warning in report["warnings"]:
            print(f"WARNING: {warning}")
    print(f"Full report saved to stability_report.json")

analyze_stability("../Artefakt02/decompiled_apk/res/layout")