import csv
import sys


def get_optimum_or_lb(csv_path, target_instance):
    """
    Attempts to obtain the optimum (or lower bound) of a JSSP instance from a
    CSV file with the format:
        name,jobs,machines,optimum
    If there is no optimum for the instance, an error message is printed and
    the function exits.

    :param csv_path: path to the CSV file
    :param target_instance: name of the instance to be searched
    """
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["name"] == target_instance:
                optimum = row.get("optimum", "").strip()

                if optimum:
                    print(f"✅ Optimum of the instance '{target_instance}': {optimum}")
                else:
                    print(f"❌ No known solution for '{target_instance}'.")
                return

        print(f"❌ Instance '{target_instance}' not found in the CSV.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\n❌ Incorrect usage.")
        print("👉 Correct format: python optimum.py <instance_name>\n")
        print("🔍 Example: python optimum.py abz5")
        sys.exit(1)

    target_instance = sys.argv[1].strip()

    if not target_instance:
        print("⚠️ Instance name cannot be empty.")
        sys.exit(1)

    get_optimum_or_lb("responses.json", target_instance)
