import requests
from pandas import read_csv


# GraphQL endpoint
url = "https://api.platform.opentargets.org/api/v4/graphql"

# List of Ensembl gene IDs
ensembl_ids = read_csv("./genes.csv", header=None).values.ravel()

# GraphQL query
query = """
query getKnownDrugsAndPharmacogenomics($ensemblId: String!) {
  target(ensemblId: $ensemblId) {
    approvedSymbol
    knownDrugs {
      uniqueDrugs
      rows {
        drug {
          id
          name
          isApproved
          yearOfFirstApproval
          hasBeenWithdrawn
          blackBoxWarning
        }
        disease {
          id
          name
        }
        phase
        status
        ctIds
      }
    }
    pharmacogenomics {
      drugs {
        drugId
        drugFromSource
      }
      phenotypeText
      genotypeAnnotationText
      evidenceLevel
      pgxCategory
      studyId
    }
  }
}
"""

# Output file
with open("open_targets_summary.txt", "w", encoding="utf-8") as f:
    for ensembl_id in ensembl_ids:
        response = requests.post(url, json={"query": query, "variables": {"ensemblId": ensembl_id}})
        if response.status_code == 200:
            target_data = response.json()["data"]["target"]
            f.write(f"Target: {target_data.get('approvedSymbol', '')} ({ensembl_id})\n\n")

            f.write("Known Drugs:\n")
            for drug in target_data["knownDrugs"]["rows"]:
                f.write(f"- Drug: {drug['drug']['name']} ({drug['drug']['id']})\n")

            f.write("\nPharmacogenomics:\n")
            for entry in target_data["pharmacogenomics"]:
                f.write(f"- Drugs: {[drug['drugFromSource'] for drug in entry.get('drugs', [])]}\n")
                f.write(f"  Phenotype: {entry.get('phenotypeText', '')}\n")
                f.write(f"  Genotype: {entry.get('genotypeAnnotationText', '')}\n")
                f.write(f"  Evidence Level: {entry.get('evidenceLevel', '')}\n")
                f.write(f"  PGx Category: {entry.get('pgxCategory', '')}\n")
                f.write(f"  Study ID: {entry.get('studyId', '')}\n")
                f.write("-" * 40 + "\n")
            f.write("=" * 60 + "\n\n")
        else:
            f.write(f"Error retrieving data for {ensembl_id}: {response.status_code}\n\n")

print("Summary saved to 'open_targets_summary.txt'")