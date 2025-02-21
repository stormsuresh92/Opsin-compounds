import requests
import json
import csv

# List of compound CIDs (Example: Aspirin (2244), Methanol (3123), Glucose (5793))
cids = ["2244", "3123", "5793"]  

# PubChem API URL for multiple compounds
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{','.join(cids)}/JSON"

# Make the API request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    data = response.json()

    # Define output CSV file
    csv_filename = "all_compounds.csv"

    # Open CSV file for writing
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write header row
        writer.writerow([
            "CID", "IUPAC Name (Allowed)", "Molecular Formula", "Molecular Weight",
            "InChI", "InChIKey", "SMILES Absolute", "SMILES Canonical", "SMILES Isomeric"
        ])

        # Loop through all compounds
        for compound in data["PC_Compounds"]:
            cid = compound["id"]["id"]["cid"]
            iupac_name = molecular_formula = molecular_weight = inchi = inchikey = ""
            smiles_absolute = smiles_canonical = smiles_isomeric = ""

            # Extract properties
            for prop in compound["props"]:
                label = prop["urn"].get("label", "")
                name = prop["urn"].get("name", "")
                value = prop["value"].get("sval", "")

                if label == "IUPAC Name" and name == "Allowed":
                    iupac_name = value
                elif label == "Molecular Formula":
                    molecular_formula = value
                elif label == "Molecular Weight":
                    molecular_weight = value
                elif label == "InChI" and name == "Standard":
                    inchi = value
                elif label == "InChIKey" and name == "Standard":
                    inchikey = value
                elif label == "SMILES" and name == "Absolute":
                    smiles_absolute = value
                elif label == "SMILES" and name == "Canonical":
                    smiles_canonical = value
                elif label == "SMILES" and name == "Isomeric":
                    smiles_isomeric = value

            # Write compound data to CSV
            writer.writerow([
                cid, iupac_name, molecular_formula, molecular_weight,
                inchi, inchikey, smiles_absolute, smiles_canonical, smiles_isomeric
            ])

    print(f"All compounds have been saved in '{csv_filename}'.")

else:
    print(f"Error: Failed to fetch data (Status Code: {response.status_code})")
