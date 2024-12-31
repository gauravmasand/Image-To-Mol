import sys, os

# Add the parent directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DECIMER import predict_SMILES
from db.operations import add_processing_request  # Importing DB operation

from DECIMER import predict_SMILES

def run_decimer(image_dir: str, output_file: str) -> list:
    """
    Process all images in a directory using DECIMER and save the results to a text file.
    
    Args:
        image_dir (str): Path to the directory containing input images.
        output_file (str): Path to the output file where results will be saved.
    
    Returns:
        list: A list of tuples where each tuple contains the image name and its predicted SMILES.
    """
    results = []

    # Don't start from beginning if a benchmark run aborted for some reason
    already_processed = []
    if os.path.exists(output_file):
        with open(output_file, "r") as output:
            lines = output.readlines()
            already_processed = [line.split("\t")[0] for line in lines]

    for image_name in os.listdir(image_dir):
        if image_name not in already_processed:
            image_path = os.path.join(image_dir, image_name)
            smiles = predict_SMILES(image_path)
            results.append((image_name, smiles))
            with open(output_file, "a") as output:
                output.write(f"{image_name}\t{smiles}\n")
            print(f"Processed: {image_name}")
    
    print("The result which we get is this ", results)

    return results


